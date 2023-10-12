# # Library to interact with TERN APIs
#
# This file defines classes and functions, which can be used within a Jupyter Notebook to interact with CoESRA.

import asyncio
import requests
from datetime import datetime, timezone, timedelta
import paramiko
from tqdm.autonotebook import tqdm
import pathlib
import os
import functools
import io
import tempfile
import subprocess
import base64
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import ipywidgets 
import threading
import time


class TqdmUpTo(tqdm):
    
    def update_to(self, progress):
        return self.update(progress - self.n)


class TERNApi:
    
    def __init__(self, apikey, env="test"):
        self.apikey = apikey
        
        self._ssh_key = None
        
        self.services = {
            "apikey": "https://auth.tern.org.au/apikey/api",
            "ssh": "https://coesra-api.tern.org.au/ssh/api",
            "jobs": "https://coesra-api.tern.org.au/jobs/api",
            "groups": "https://coesra-api.tern.org.au/groups/api",
            "desktop": "https://coesra-api.tern.org.au/desktop/api",
            "guacamole": "https://coesra-desktop.tern.org.au",
            "images": "https://ecoimages.tern.org.au/api",
            "login": "coesra-login.tern.org.au",
        }
        
    @property
    def session(self):
        session = requests.Session()
        # self._session.auth = ("apikey", self.apikey)
        session.headers.update({
            "X-API-Key": self.apikey,
            "User-Agent": "TERN Api client",
        })
        return session
    
    @functools.cache
    def whoami(self, service="ssh"):
        with self.session as session:
            res = session.get(f"{self.services[service]}/whoami")
            res.raise_for_status()
            return res.json()
    
    def gen_ssh_key(self):
        # check if we have a key, and whether it's still valid
        if self._ssh_key and ((self._ssh_key["not_after"] - datetime.now().astimezone(timezone.utc)) > timedelta(minutes=5)):
            return self._ssh_key
        with self.session as session:
            res = session.post(
                f"{self.services['ssh']}/v1.0/key/generate",
                # json={"validity": 3600},
                json={"validity": 86400},
            )
            res.raise_for_status()
            key_result = res.json()
            key_result["not_after"] = datetime.fromisoformat(key_result["not_after"])
            self._ssh_key = key_result
            return key_result
        
    def get_desktop_config(self):
        with self.session as session:
            res = session.get(f"{self.services['desktop']}/v1.0/config")
            res.raise_for_status()
            return res.json()
    
    def start_desktop(self):
        with self.session as session:
            res = session.post(
                f"{self.services['desktop']}/v1.0/desktop",
                json={ "flavour": "default", "jobcpu": 4, "jobhour": 120, "jobmemory": 8 },
            )
            res.raise_for_status()
            return res.json()
    
    def stop_desktop(self, did):
        with self.session as session:
            res = session.delete(
                f"{self.services['desktop']}/v1.0/desktop/{did}"
            )
            res.raise_for_status()
            return res.json()
    
    def get_desktop(self, auto_start=False):
        data = []
        with self.session as session:
            res = session.get(
                f"{self.services['desktop']}/v1.0/desktop",
                json={},
            )
            res.raise_for_status()
            data = res.json()
        desktops = []
        for dt in data['desktops']:
            # import pprint
            # pprint.pprint(data)
            if dt['state']['id'] in ('FAILED', 'STOPPED'):
                # skip it
                continue
            # state CANCELLED disappears by itself .. .state FAILED stays ?
            desktops.append({
                'id': dt['id'],
                'url': dt['desktop_url'],
                'state': dt['state']['id'],
            })
        if not desktops and auto_start:
            # no desktop in active state ... start a new one 
            self.start_desktop()
            desktops = self.get_desktop(False)
        return desktops
    
    def desktop_widget(self):
        """A CoESRA desktop widgget."""
        return DesktopWidget(self)
    
    def _create_dest_path(self, sftp, dest_path):
        # 1. walk up tree until folder exists 
        cur_path = dest_path
        paths_to_create = []
        while cur_path:
            try:
                sftp.stat(str(cur_path))
            except FileNotFoundError:
                paths_to_create.append(cur_path)
                cur_path = cur_path.parent
                continue 
            # cur_path exits
            break
        for new_path in reversed(paths_to_create):
            # print("MKDIR:", new_path)
            sftp.mkdir(str(new_path))

    def sftp(self, source, dest, leave=False):
        # TODO: - multi threaded upload of files ... i.e. upload more than one thread at a time ...
        #         ... need concurrency check for folders ?
        #       - multi part upload ... sftp can do chunked uploading to same file at different offsets
        #         ... improve large file upload e.g.: https://stackoverflow.com/a/66163763
        uname = self.whoami()['claims']['coesra_uname']
        sshkeys = self.gen_ssh_key()
        source_path = pathlib.Path(source)
        pbar1 = tqdm(total=0, dynamic_ncols=False, leave=leave, display=not source_path.is_file())
        pbar2 = TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, dynamic_ncols=False, leave=leave)
        with paramiko.SSHClient() as ssh:
            ssh_key = paramiko.RSAKey.from_private_key(io.StringIO(sshkeys["private_key"]))
            ssh_key.load_certificate(sshkeys["cert_key"])
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.services["login"], username=uname, port=22, pkey=ssh_key, look_for_keys=False)
            with ssh.open_sftp() as sftp:
                dest = pathlib.Path(dest)
                if dest.parts[0] == "~":
                    # adjust home tilde expansion on remote side
                    sftp.chdir('.')
                    sftp_home = pathlib.Path(sftp.getcwd())
                    # print("CWD", sftp_home)
                    # replace "~" with sftp_home
                    dest = sftp_home / dest.relative_to("~")
                # get list of source_files
                source_path = pathlib.Path(source)
                if source_path.is_file():
                    source_files = [source_path]
                else:
                    source_files = list(pathlib.Path(source).glob("**/*"))
                pbar1.reset(total=len(source_files))
                pbar1.set_description(f"Upload {source} to {dest}")
                for fname in source_files:
                    pbar1.update()
                    pbar2.reset(total=fname.stat().st_size)
                    pbar2.set_description(str(fname.name))
                    # pbar2.description
                    if not fname.is_file():
                        continue
                    if source_path.is_file():
                        dfname = pathlib.Path(dest) / fname
                    else:
                        dfname = pathlib.Path(dest) / fname.relative_to(source)
                    # check if dest dir exists:
                    try:
                        sftp.stat(str(dfname.parent))
                    except FileNotFoundError:
                        self._create_dest_path(sftp, dfname.parent)
                    # print("PUT:", fname, dfname)
                    def progress_callback(done, total):
                        pbar2.update_to(done)
                        # pbar2.total = total
                    attrs = sftp.put(str(fname), str(dfname), callback=progress_callback)
                    # ensure we set progress bar to uploaded bytes (in case upload was too fast for callback)
                    pbar2.update_to(attrs.st_size)
                # ensurp pbars update at the end
                pbar1.refresh()
                pbar2.refresh()
        pbar2.close()
        pbar1.close()

    def scp(self, src, dest):
        uname = self.whoami()['claims']['coesra_uname']
        sshkeys = self.gen_ssh_key()

        # TODO: use as context manager ... or even better implement one based on this one to run ssh commands
        with tempfile.TemporaryDirectory() as tmpdir:
            # little opener help to set posix permissions on new files 
            def opener(path, flags):
                return os.open(path, flags, mode=0o600)
    
            tmppath = pathlib.Path(tmpdir)
            with open(tmppath / "id_rsa-cert.pub", mode="w", opener=opener) as fd:
                fd.write(sshkeys['cert_key'])
            with open(tmppath / "id_rsa.pub", mode="w", opener=opener) as fd:
                fd.write(sshkeys['public_key'])
            with open(tmppath / "id_rsa", mode="w", opener=opener) as fd:
                fd.write(sshkeys['private_key'])
        
            # cmd = ['ssh', '-i', str(tmppath / "id_rsa"), '-o', 'PubkeyAcceptedKeyTypes=+ssh-rsa-cert-v01@openssh.com', 
            #        '{}@203.101.231.113'.format(uname), 'ls', '-la']
    
            cmd = [
                'scp', 
                '-i', str(tmppath / "id_rsa"), 
                '-o', 'PubkeyAcceptedKeyTypes=+ssh-rsa-cert-v01@openssh.com',
                '-o', 'StrictHostKeyChecking=no',
                '-r',
                # '~/projects/464_testg/1_task-of-2022-08-08t23-14-43-866z/assets/',
                # os.path.expanduser('~/projects/464_testg/1_task-of-2022-08-08t23-14-43-866z/assets/'),
                os.path.expanduser(src),
                f"{uname}@{self.services['login']}:{dest}"
            ]
    
            subprocess.check_call(cmd)
        
    def download_tern_data(self, url, dest):
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
            
        dest = pathlib.Path(dest).expanduser()
        dest.mkdir(parents=True, exist_ok=True)
                 
        table = soup.find(attrs={"summary": "Directory Listing"})
        links = table.find_all('a')
        pbar1 = tqdm(total=len(links))
        pbar2 = tqdm(unit='B', unit_scale=True, unit_divisor=1024, dynamic_ncols=False)
        for link in links:
            pbar1.update()
            if link.get("href") == "../":
                continue
            dl_url = urljoin(url, link.get("href"))
            # TODO: we know urls are relative so we can use href directly
            dest_file = dest / link.get("href")
            with self.session.get(dl_url, stream=True) as r:
                    
                r.raise_for_status()
                try:
                    pbar2.reset(total=int(r.headers.get("Content-Length")))
                except:
                    pbar2.reset(total=0)
                pbar2.set_description(str(dest_file.name))
                    
                with dest_file.open('wb') as f:
                    for chunk in r.iter_content(chunk_size=1024 * 64): 
                        # If you have chunk encoded response uncomment if
                        # and set chunk_size parameter to None.
                        #if chunk: 
                        f.write(chunk)
                        pbar2.update(len(chunk))
            pbar1.refresh()
            pbar2.refresh()


class DesktopWidget(ipywidgets.VBox):
    """An iPyWidget to manage CoESRA Desktop."""
    
    def __init__(self, api):
        super(DesktopWidget, self).__init__()
        self.api = api
        
        # main label for textual output / heading
        self.label_format = '<h1 style="margin: 5px">{}</h1>'
        self.label = ipywidgets.HTML(value=self.label_format.format("Configure Desktop:"))
        # progress bar to show start / stop desktop progress
        #    min / max, description, bar_style, style={'bac_color': maroon}
        self.progress = ipywidgets.IntProgress(min=0, orientation='horizontal')
        # flavour selector
        self.flavour = ipywidgets.Dropdown(description="Flavour")
        # job params
        self.jobcpu = ipywidgets.Dropdown(description="CPUs")
        self.jobmemory = ipywidgets.Dropdown(description="RAM")
        self.jobhour = ipywidgets.Dropdown(description="Hours")
        # start button 
        self.start_button = ipywidgets.Button(
            description="Start Desktop",
            button_style='success',
            icon="play"
        )
        self.access_button = ipywidgets.HTML()
        # stop button
        self.stop_button = ipywidgets.Button(
            description="Stop Desktop",
            button_style='danger',
            icon="stop"
        )
        # debug area
        self.output = ipywidgets.Output()
        
        # define layouts
        self.configuration_layout = [
            self.label,
            self.flavour, self.jobcpu, self.jobmemory, self.jobhour, 
            self.start_button, self.output
        ]
        self.starting_layout = [
            self.label, self.progress, self.stop_button, self.output
        ]
        self.stopping_layout = [
            self.label, self.progress, self.output
        ]
        self.ready_layout = [
            self.label, ipywidgets.HBox([self.access_button, self.stop_button]), self.output,
        ]
        
        
        # hook up events 
        self.flavour.observe(self._update_dropdowns, names='value', type='change')
        self.start_button.on_click(self._start_desktop)
        self.stop_button.on_click(self._stop_desktop)
        
        # init widget 
        self._desktop_poller = None
        self._desktop = None
        self._config = None
        self._init()
        
    def _init(self):
        # load config and configure widgets 
        self._config = self.api.get_desktop_config()
        self.flavour.options = [(item["label"], key) for (key, item) in self._config["flavours"].items()]
        self.flavour.value = "default"
                
        self.desktop = self.api.get_desktop(auto_start=False)
        
    def _debug(self, *msg_parts):
        # hepler method to append messages to output section ... mainly useful for debugging
        if False:
            self.output.append_stdout(' '.join(str(s) for s in msg_parts))
            self.output.append_stdout("\n")
        
    @property 
    def desktop(self):
        return self._desktop
    
    @desktop.setter 
    def desktop(self, value):
        self._debug("Update desktop state:", value)
        self._desktop = value
        if value:
            # we have a desktop .... 
            if value[0]['state'] != 'READY':
                # if not ready we need a poller thread to update widgets 
                if (not self._desktop_poller) or self._desktop_poller.done():
                    # state is not READY, and poller is not running.
                    # start background thread so that widget will update with state changes.
                    loop = asyncio.get_event_loop()
                    self._desktop_poller = loop.run_in_executor(None, self._poll_desktop, self.output, loop)
            if value[0]['state'].startswith('STOP'):
                # we are shutting down 
                states = {"STOP_REQUESTED": 1, "STOPPING": 2, "gone": 3}
                self.children = self.stopping_layout 
                self.label.value = self.label_format.format(f"Stopping Desktop ...")
                self.progress.max = 3
                self.progress.value = states.get(value[0]['state'], 0)
            elif value[0]['state'] != 'READY':
                # we are starting up
                states = {"REQUESTED": 1, "PENDING": 2, "STARTING": 3, "SETUP": 4, "ready": 5}
                self.children = self.starting_layout 
                self.label.value = self.label_format.format(f"Starting Desktop ...")
                self.progress.max = 5
                self.progress.value = states.get(value[0]['state'], 0)
            else:
                # it's ready 
                self.children = self.ready_layout
                self.label.value = self.label_format.format("Desktop ready")
                self.access_button.value = f'<a class="jupyter-button widget-button mod-success" href="{value[0]["url"]}" target="_blank"><i class="fa fa-play"></i>Access Desktop</a>' 
        else:
            # no desktop active -> offer to configure and start one
            self.children = self.configuration_layout
            self.label.value = self.label_format.format("Configure Desktop")
            
    def _poll_desktop(self, output, loop):
        self._debug("Poll Thread started.")
        try:
            while True:
                desktop = self.api.get_desktop(auto_start=False)

                # this is important otherwise UI does not update
                loop.call_soon_threadsafe(lambda x: setattr(self, "desktop", x), desktop)

                if not desktop:
                    # no desktop ... exit 
                    break 
                if desktop[0]['state'] == 'READY':
                    # we are done 
                    break
                # sleep a bit and try again
                time.sleep(5)
        except Exception as e:
            self._debug("Poll Thread error:", e)
        self._debug("Poll Thread exited:", self.desktop)
        
    def _start_desktop(self, widget):
        # callback to start desktop
        self._debug("Start Desktop:", widget)
        result = self.api.start_desktop()
        self.desktop = [{'id': result['desktop_id'], 'state': 'SUBMITTED'}]
        widget.disable = True
        self._debug("Starting?:", widget, result)

    def _stop_desktop(self, widget):
        # callback to start desktop
        self._debug("Stop Desktop:", widget)
        result = self.api.stop_desktop(self._desktop[0]['id'])
        self.desktop = [{'id': self._desktop[0]['id'], 'state': 'STOP_REQUESTED'}]
        # self.desktop = self.api.get_desktop(auto_start=False)
        widget.disable = True
        self._debug("Stopping?:", widget, result)
            
    def _update_dropdowns(self, change):
        new_value = change['new']
        f_conf = self._config["flavours"][new_value]["config"]
        self.jobcpu.options = [x for x in range(f_conf["jobcpu"]["minimum"], f_conf["jobcpu"]["maximum"]+1)]
        self.jobcpu.value = f_conf["jobcpu"]["default"]
        self.jobmemory.options = [x for x in range(f_conf["jobmemory"]["minimum"], f_conf["jobmemory"]["maximum"]+1)]
        self.jobmemory.value = f_conf["jobmemory"]["default"]
        self.jobhour.options = [x for x in range(f_conf["jobhour"]["minimum"], f_conf["jobhour"]["maximum"]+1)]
        self.jobhour.value = f_conf["jobhour"]["default"]


