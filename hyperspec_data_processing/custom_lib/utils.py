import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
import colorsys


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    diff = np.abs(value - array[idx])
    return idx, array[idx], diff


def get_ndvi(hyper, wavelength):
    """
    Compute ndvi from data
    data[0]: wavelength 1xn
    data[1]: hyperspectral data hxwxn
    """
    # hyper = data[1].astype(np.float)
    # wavelength = data[0]
    nir = 800
    red = 680
    diff_thresh = 50
    idx_nir, wl_nir, diff_nir = find_nearest(wavelength, nir)
    idx_red, wl_red, diff_red = find_nearest(wavelength, red)
    if diff_nir < diff_thresh and diff_red < diff_thresh:
        rho_nir = hyper[:, :, idx_nir]
        rho_red = hyper[:, :, idx_red]
        numerator = rho_nir - rho_red
        denominator = rho_nir + rho_red
        with np.errstate(divide='ignore', invalid='ignore'):
            ndvi = numerator / denominator
            ndvi = np.nan_to_num(ndvi)
            ndvi[ndvi > 1] = 1
            ndvi[ndvi < -1] = -1

        cm = plt.get_cmap('viridis')
        ndvi_out = cm((ndvi+1)/2)[:, :, :3]
        ndvi_out = ndvi_out * 255
        ndvi_out = ndvi_out.astype(np.uint8)
        return ndvi, ndvi_out
    else:
        return None


def get_ndre(hyper, wavelength):
    """
    Compute ndre from data
    data[0]: wavelength 1xn
    data[1]: hyperspectral data hxwxn
    """
    # hyper = data[1].astype(np.float)
    # wavelength = data[0]
    wl1 = 800
    wl2 = 720
    diff_thresh = 50
    idx1, wl_1, diff_1 = find_nearest(wavelength, wl1)
    idx2, wl_2, diff_2 = find_nearest(wavelength, wl2)
    if diff_1 < diff_thresh and diff_2 < diff_thresh:
        rho_1 = hyper[:, :, idx1]
        rho_2 = hyper[:, :, idx2]
        numerator = rho_1 - rho_2
        denominator = rho_1 + rho_2
        with np.errstate(divide='ignore', invalid='ignore'):
            ndre = numerator / denominator
            ndre = np.nan_to_num(ndre)
            ndre[ndre > 1] = 1
            ndre[ndre < -1] = -1


        cm = plt.get_cmap('PiYG')
        ndre_out = cm((ndre+1)/2)[:, :, :3]
        ndre_out = ndre_out * 255
        ndre_out = ndre_out.astype(np.uint8)
        return ndre, ndre_out
    else:
        return None
# reference for wavelegth: https://www.researchgate.net/publication/259360047_Use_of_the_Canopy_Chlorophyl_Content_Index_CCCI_for_Remote_Estimation_of_Wheat_Nitrogen_Content_in_Rainfed_Environments
# reference for range: https://www.tandfonline.com/doi/pdf/10.1080/22797254.2018.1527661#:~:text=The%20NDRE%20values%20range%20between,the%20level%20of%20chlorophyll%20content.

# Modified according to paper
def get_ccci(hyper, wavelength):
    """
    Compute ccci from data
    data[0]: wavelength 1xn
    data[1]: hyperspectral data hxwxn
    """
    ndre, _ = get_ndre(hyper, wavelength)
    # hyper = data[1].astype(np.float)
    # wavelength = data[0]
    nir = 800
    # diff_thresh = 50
    # idx_nir, wl_nir, diff_nir = find_nearest(wavelength, nir)
    # if diff_nir < diff_thresh:
    # rho_nir = hyper[:, :, idx_nir]
    # rho_nir /= np.max(rho_nir)
    numerator = ndre - np.min(ndre)
    denominator = np.max(ndre) - np.min(ndre)
    with np.errstate(divide='ignore', invalid='ignore'):
        ccci = numerator / denominator
        ccci = np.nan_to_num(ccci)
        ccci[ccci > 1] = 1
        ccci[ccci < 0] = 0

        cm = plt.get_cmap('PiYG')
        ccci_out = cm((ccci+1)/2)[:, :, :3]
        ccci_out = ccci_out * 255
        ccci_out = ccci_out.astype(np.uint8)
        return ccci, ccci_out
    # else:
    #     return None
# https://www.sciencedirect.com/science/article/pii/S1161030121001179

def get_npci(hyper, wavelength):
    """
    Compute npci from data
    data[0]: wavelength 1xn
    data[1]: hyperspectral data hxwxn
    """
    # hyper = data[1].astype(np.float)
    # wavelength = data[0]
    wl1 = 680
    wl2 = 430
    diff_thresh = 50
    idx1, wl_1, diff_1 = find_nearest(wavelength, wl1)
    idx2, wl_2, diff_2 = find_nearest(wavelength, wl2)
    if diff_1 < diff_thresh and diff_2 < diff_thresh:
        rho_1 = hyper[:, :, idx1]
        rho_2 = hyper[:, :, idx2]
        numerator = rho_1 - rho_2
        denominator = rho_1 + rho_2
        with np.errstate(divide='ignore', invalid='ignore'):
            npci = numerator / denominator
            npci = np.nan_to_num(npci)
            npci[npci > 1] = 1
            npci[npci < -1] = -1

        cm = plt.get_cmap('PiYG')
        npci_out = cm((npci+1)/2)[:, :, :3]
        npci_out = npci_out * 255
        npci_out = npci_out.astype(np.uint8)
        return npci, npci_out
    else:
        return None


def get_psri(hyper, wavelength):
    """
    Compute psri from data
    data[0]: wavelength 1xn
    data[1]: hyperspectral data hxwxn
    """
    # hyper = data[1].astype(np.float)
    # wavelength = data[0]
    wl1 = 680
    wl2 = 531
    wl3 = 800
    diff_thresh = 50
    idx1, wl_1, diff_1 = find_nearest(wavelength, wl1)
    idx2, wl_2, diff_2 = find_nearest(wavelength, wl2)
    idx3, wl_3, diff_3 = find_nearest(wavelength, wl3)
    if diff_1 < diff_thresh and diff_2 < diff_thresh and diff_2 < diff_thresh:
        rho_1 = hyper[:, :, idx1]
        rho_2 = hyper[:, :, idx2]
        rho_3 = hyper[:, :, idx3]
        numerator = rho_1 - rho_2
        denominator = rho_3
        with np.errstate(divide='ignore', invalid='ignore'):
            psri = numerator / denominator
            psri = np.nan_to_num(psri)
            psri[psri >1] = 1
            psri[psri <-1] =-1


        cm = plt.get_cmap('PiYG')
        psri_out = cm((psri+1)/2)[:, :, :3]
        psri_out = psri_out * 255
        psri_out = psri_out.astype(np.uint8)

        return psri, psri_out
    else:
        return None


def get_pri(hyper, wavelength):
    """
    Compute pri from data
    data[0]: wavelength 1xn
    data[1]: hyperspectral data hxwxn
    """
    # hyper = data[1].astype(np.float)
    # wavelength = data[0]
    wl1 = 531
    wl2 = 570
    diff_thresh = 50
    idx1, wl_1, diff_1 = find_nearest(wavelength, wl1)
    idx2, wl_2, diff_2 = find_nearest(wavelength, wl2)
    if diff_1 < diff_thresh and diff_2 < diff_thresh:
        rho_1 = hyper[:, :, idx1]
        rho_2 = hyper[:, :, idx2]
        numerator = rho_1 - rho_2
        denominator = rho_1 + rho_2
        with np.errstate(divide='ignore', invalid='ignore'):
            pri = numerator / denominator
            pri = np.nan_to_num(pri)
            pri[pri > 1] = 1
            pri[pri < -1] = -1

        cm = plt.get_cmap('PiYG')
        pri_out = cm((pri+1)/2)[:, :, :3]
        pri_out = pri_out * 255
        pri_out = pri_out.astype(np.uint8)
        return pri, pri_out
    else:
        return None

def get_sr(hyper, wavelength):
    """
    Compute sr from data
    data[0]: wavelength 1xn
    data[1]: hyperspectral data hxwxn
    SR = NIR / RED
    """
    # hyper = data[1].astype(np.float)
    # wavelength = data[0]
    nir = 800
    red = 680
    diff_thresh = 50
    idx_nir, wl_nir, diff_nir = find_nearest(wavelength, nir)
    idx_red, wl_red, diff_red = find_nearest(wavelength, red)
    if diff_nir < diff_thresh and diff_red < diff_thresh:
        rho_nir = hyper[:, :, idx_nir]
        rho_red = hyper[:, :, idx_red]
        with np.errstate(divide='ignore', invalid='ignore'):
            sr = rho_nir / rho_red
            sr = np.nan_to_num(sr)
            sr[sr > 30] = 30
            sr[sr < 0] = 0

        cm = plt.get_cmap('viridis')
        sr_out = cm((sr+1)/2)[:, :, :3]
        sr_out = sr_out * 255
        sr_out = sr_out.astype(np.uint8)
        return sr, sr_out
    else:
        return None


def get_sipi(hyper, wavelength):
    """
    Compute sipi from data
    data[0]: wavelength 1xn
    data[1]: hyperspectral data hxwxn
    """
    # hyper = data[1].astype(np.float)
    # wavelength = data[0]
    wl1 = 800
    wl2 = 445
    wl3 = 680
    diff_thresh = 50
    idx1, wl_1, diff_1 = find_nearest(wavelength, wl1)
    idx2, wl_2, diff_2 = find_nearest(wavelength, wl2)
    idx3, wl_3, diff_3 = find_nearest(wavelength, wl3)
    if diff_1 < diff_thresh and diff_2 < diff_thresh and diff_2 < diff_thresh:
        rho_1 = hyper[:, :, idx1]
        rho_2 = hyper[:, :, idx2]
        rho_3 = hyper[:, :, idx3]
        numerator = rho_1 - rho_2
        denominator = rho_1 - rho_3
        with np.errstate(divide='ignore', invalid='ignore'):
            sipi = numerator / denominator
            sipi = np.nan_to_num(sipi)
            sipi[sipi >2] = 2
            sipi[sipi < 0] = 0


        cm = plt.get_cmap('PiYG')
        sipi_out = cm((sipi+1)/2)[:, :, :3]
        sipi_out = sipi_out * 255
        sipi_out = sipi_out.astype(np.uint8)

        return sipi, sipi_out
    else:
        return None

# in dip
def get_rgr(hyper, wavelength):
    """
    Compute rgr from data
    data[0]: wavelength 1xn
    data[1]: hyperspectral data hxwxn
    """
    # hyper = data[1].astype(np.float)
    # wavelength = data[0]
    wl1 = 490
    wl2 = 570
    wl3 = 640
    wl4 = 760
    diff_thresh = 50

    idx1, wl_1, diff_1 = find_nearest(wavelength, wl1)
    idx2, wl_2, diff_2 = find_nearest(wavelength, wl2)
    idx3, wl_3, diff_3 = find_nearest(wavelength, wl3)
    idx4, wl_4, diff_4 = find_nearest(wavelength, wl4)

    if diff_1 < diff_thresh and diff_2 < diff_thresh and diff_2 < diff_thresh:

        sum_green = hyper[:, :, idx1]
        green_t = 0
        for itr in range(idx1+1,idx2+1):
            sum_green = sum_green + hyper[:, :, itr]
            green_t += 1
        mean_green = sum_green/green_t

        sum_red = hyper[:, :, idx3]
        red_t = 0
        for itr in range(idx3+1,idx4+1):
            sum_red = sum_red + hyper[:, :, itr]
            red_t += 1
        mean_red = sum_red/red_t


        numerator = mean_red
        denominator = mean_green
        with np.errstate(divide='ignore', invalid='ignore'):
            rgr = numerator / denominator
            rgr = np.nan_to_num(rgr)
            rgr[rgr > 8] = 8
            rgr[rgr < 0.1] = 0.1


        cm = plt.get_cmap('PiYG')
        rgr_out = cm((rgr+1)/2)[:, :, :3]
        rgr_out = rgr_out * 255
        rgr_out = rgr_out.astype(np.uint8)

        return rgr, rgr_out
    else:
        return None

# in dip
def get_cri1(hyper, wavelength):
    """
    Compute cri1 from data
    data[0]: wavelength 1xn
    data[1]: hyperspectral data hxwxn
    """
    # hyper = data[1].astype(np.float)
    # wavelength = data[0]
    wl1 = 510
    wl2 = 550
    diff_thresh = 50
    idx1, wl_1, diff_1 = find_nearest(wavelength, wl1)
    idx2, wl_2, diff_2 = find_nearest(wavelength, wl2)
    if diff_1 < diff_thresh and diff_2 < diff_thresh:
        rho_1 = hyper[:, :, idx1]
        rho_2 = hyper[:, :, idx2]
        with np.errstate(divide='ignore', invalid='ignore'):
            cri1 = (1/rho_1) - (1/rho_2)
            cri1 = np.nan_to_num(cri1)
            cri1[cri1 > 15] = 15
            cri1[cri1 < 0] = 0

        cm = plt.get_cmap('PiYG')
        cri1_out = cm((cri1+1)/2)[:, :, :3]
        cri1_out = cri1_out * 255
        cri1_out = cri1_out.astype(np.uint8)
        return cri1, cri1_out
    else:
        return None



def get_cri2(hyper, wavelength):
    """
    Compute cri2 from data
    data[0]: wavelength 1xn
    data[1]: hyperspectral data hxwxn
    """
    # hyper = data[1].astype(np.float)
    # wavelength = data[0]
    wl1 = 510
    wl2 = 700
    diff_thresh = 50
    idx1, wl_1, diff_1 = find_nearest(wavelength, wl1)
    idx2, wl_2, diff_2 = find_nearest(wavelength, wl2)
    if diff_1 < diff_thresh and diff_2 < diff_thresh:
        rho_1 = hyper[:, :, idx1]
        rho_2 = hyper[:, :, idx2]
        with np.errstate(divide='ignore', invalid='ignore'):
            cri2 = (1/rho_1) - (1/rho_2)
            cri2 = np.nan_to_num(cri2)
            cri2[cri2 > 15] = 15
            cri2[cri2 < 0] = 0

        cm = plt.get_cmap('PiYG')
        cri2_out = cm((cri2+1)/2)[:, :, :3]
        cri2_out = cri2_out * 255
        cri2_out = cri2_out.astype(np.uint8)
        return cri2, cri2_out
    else:
        return None

# in dip
def get_ari1(hyper, wavelength):
    """
    Compute ari1 from data
    data[0]: wavelength 1xn
    data[1]: hyperspectral data hxwxn
    """
    # hyper = data[1].astype(np.float)
    # wavelength = data[0]
    wl1 = 550
    wl2 = 700
    diff_thresh = 50
    idx1, wl_1, diff_1 = find_nearest(wavelength, wl1)
    idx2, wl_2, diff_2 = find_nearest(wavelength, wl2)
    if diff_1 < diff_thresh and diff_2 < diff_thresh:
        rho_1 = hyper[:, :, idx1]
        rho_2 = hyper[:, :, idx2]
        with np.errstate(divide='ignore', invalid='ignore'):
            ari1 = (1/rho_1) - (1/rho_2)
            ari1 = np.nan_to_num(ari1)
            ari1[ari1 > 0.2] = 0.2
            ari1[ari1 < 0] = 0

        cm = plt.get_cmap('PiYG')
        ari1_out = cm((ari1+1)/2)[:, :, :3]
        ari1_out = ari1_out * 255
        ari1_out = ari1_out.astype(np.uint8)
        return ari1, ari1_out
    else:
        return None

# in dip    
def get_ari2(hyper, wavelength):
    """
    Compute ari2 from data
    data[0]: wavelength 1xn
    data[1]: hyperspectral data hxwxn
    """
    # hyper = data[1].astype(np.float)
    # wavelength = data[0]
    wl1 = 550
    wl2 = 700
    wl3 = 800
    diff_thresh = 50
    idx1, wl_1, diff_1 = find_nearest(wavelength, wl1)
    idx2, wl_2, diff_2 = find_nearest(wavelength, wl2)
    idx3, wl_3, diff_3 = find_nearest(wavelength, wl3)
    if diff_1 < diff_thresh and diff_2 < diff_thresh:
        rho_1 = hyper[:, :, idx1]
        rho_2 = hyper[:, :, idx2]
        rho_3 = hyper[:, :, idx3]
        with np.errstate(divide='ignore', invalid='ignore'):
            ari2 = (1/rho_1) - (1/rho_2)
            ari2 = rho_3 * ari2
            ari2 = np.nan_to_num(ari2)
            ari2[ari2 > 0.2] = 0.2
            ari2[ari2 < 0] = 0

        cm = plt.get_cmap('PiYG')
        ari2_out = cm((ari2+1)/2)[:, :, :3]
        ari2_out = ari2_out * 255
        ari2_out = ari2_out.astype(np.uint8)
        return ari2, ari2_out
    else:
        return None
    
    
def get_rndvi(hyper, wavelength):
    """
    Compute ndvi from data
    data[0]: wavelength 1xn
    data[1]: hyperspectral data hxwxn
    """
    # hyper = data[1].astype(np.float)
    # wavelength = data[0]
    nir = 750
    red = 705
    diff_thresh = 50
    idx_nir, wl_nir, diff_nir = find_nearest(wavelength, nir)
    idx_red, wl_red, diff_red = find_nearest(wavelength, red)
    if diff_nir < diff_thresh and diff_red < diff_thresh:
        rho_nir = hyper[:, :, idx_nir]
        rho_red = hyper[:, :, idx_red]
        numerator = rho_nir - rho_red
        denominator = rho_nir + rho_red
        with np.errstate(divide='ignore', invalid='ignore'):
            ndvi = numerator / denominator
            ndvi = np.nan_to_num(ndvi)
            ndvi[ndvi > 1] = 1
            ndvi[ndvi < -1] = -1

        cm = plt.get_cmap('viridis')
        ndvi_out = cm((ndvi+1)/2)[:, :, :3]
        ndvi_out = ndvi_out * 255
        ndvi_out = ndvi_out.astype(np.uint8)
        return ndvi, ndvi_out
    else:
        return None
    
    
def get_npqi(hyper, wavelength):
    """
    Compute ndvi from data
    data[0]: wavelength 1xn
    data[1]: hyperspectral data hxwxn
    """
    # hyper = data[1].astype(np.float)
    # wavelength = data[0]
    nir = 415
    red = 430
    diff_thresh = 50
    idx_nir, wl_nir, diff_nir = find_nearest(wavelength, nir)
    idx_red, wl_red, diff_red = find_nearest(wavelength, red)
    if diff_nir < diff_thresh and diff_red < diff_thresh:
        rho_nir = hyper[:, :, idx_nir]
        rho_red = hyper[:, :, idx_red]
        numerator = rho_nir - rho_red
        denominator = rho_nir + rho_red
        with np.errstate(divide='ignore', invalid='ignore'):
            ndvi = numerator / denominator
            ndvi = np.nan_to_num(ndvi)
            ndvi[ndvi > 1.5] = 1.5
            ndvi[ndvi < 0.5] = 0.5

        cm = plt.get_cmap('viridis')
        ndvi_out = cm((ndvi+1)/2)[:, :, :3]
        ndvi_out = ndvi_out * 255
        ndvi_out = ndvi_out.astype(np.uint8)
        return ndvi, ndvi_out
    else:
        return None



def wavelength_to_rgb(wavelength, gamma=0.8):
    '''This converts a given wavelength of light to an
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    '''

    wavelength = float(wavelength)
    # if wavelength < 380:
    #     wavelength = 380
    # elif wavelength > 750:
    #     wavelength = 750
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    # R *= 255
    # G *= 255
    # B *= 255
    return [R, G, B]


def RGBToPyCmap(rgbdata):
    nsteps = rgbdata.shape[0]
    stepaxis = np.linspace(0, 1, nsteps)

    rdata = [];
    gdata = [];
    bdata = []
    for istep in range(nsteps):
        r = rgbdata[istep, 0]
        g = rgbdata[istep, 1]
        b = rgbdata[istep, 2]
        rdata.append((stepaxis[istep], r, r))
        gdata.append((stepaxis[istep], g, g))
        bdata.append((stepaxis[istep], b, b))

    mpl_data = {'red': rdata,
                'green': gdata,
                'blue': bdata}

    return mpl_data


def save_disparity(savename, data, max_disp):
    turbo_colormap_data = get_color_map()
    mpl_data = RGBToPyCmap(turbo_colormap_data)
    plt.register_cmap(name='turbo', data=mpl_data, lut=turbo_colormap_data.shape[0])
    plt.imshow(data, cmap='turbo', vmin=0, vmax=max_disp)
    plt.colorbar()
    plt.savefig(savename)
    plt.close()
    # plt.show()
    # plt.imsave(savename, data, vmin=0, vmax=max_disp, cmap='turbo')


def show_disparity(data, max_disp, min_disp, colorname):
    # turbo_colormap_data = get_color_map()
    # mpl_data = RGBToPyCmap(turbo_colormap_data)
    # plt.register_cmap(name=colorname, data=mpl_data, lut=turbo_colormap_data.shape[0])
    plt.imshow(data, cmap=colorname, vmin=min_disp, vmax=max_disp)
    plt.colorbar()
    plt.show()

def transfer_hyper_color(data, max=None):
    if max is not None:
        data = data / max
    # data = data/np.max(data)
    cm = plt.get_cmap('gray')
    data_out = cm(data)[:,:,:3]
    data_out = data_out*255
    data_out = data_out.astype(np.uint8)

    return data_out

def transfer_hyper_color_wl(data, wavelength):
    # cm = plt.get_cmap('plasma')
    # data_out = cm(data)[:,:,:3]
    # data_out = data_out*255
    # data_out = data_out.astype(np.uint8)

    if wavelength >= 380 and wavelength <= 750:
        row, col = np.shape(data)
        v = cv2.convertScaleAbs(data)

        r, g, b = wavelength_to_rgb(wavelength)
        h, s, _ = colorsys.rgb_to_hsv(r, g, b)
        h = int(h * 255)
        s = int(s * 255)
        data_out = np.ones((row, col, 3), dtype=np.uint8)
        data_out[:, :, 0] *= h
        data_out[:, :, 1] *= s
        data_out[:, :, 2] = v
        data_out = cv2.cvtColor(data_out, cv2.COLOR_HSV2RGB)
        return data_out
    else:
        return np.zeros((np.shape(data)[0], np.shape(data)[1], 3), dtype=np.uint8)




def get_color_map():
    return np.array([[0.18995, 0.07176, 0.23217],
                     [0.19483, 0.08339, 0.26149],
                     [0.19956, 0.09498, 0.29024],
                     [0.20415, 0.10652, 0.31844],
                     [0.20860, 0.11802, 0.34607],
                     [0.21291, 0.12947, 0.37314],
                     [0.21708, 0.14087, 0.39964],
                     [0.22111, 0.15223, 0.42558],
                     [0.22500, 0.16354, 0.45096],
                     [0.22875, 0.17481, 0.47578],
                     [0.23236, 0.18603, 0.50004],
                     [0.23582, 0.19720, 0.52373],
                     [0.23915, 0.20833, 0.54686],
                     [0.24234, 0.21941, 0.56942],
                     [0.24539, 0.23044, 0.59142],
                     [0.24830, 0.24143, 0.61286],
                     [0.25107, 0.25237, 0.63374],
                     [0.25369, 0.26327, 0.65406],
                     [0.25618, 0.27412, 0.67381],
                     [0.25853, 0.28492, 0.69300],
                     [0.26074, 0.29568, 0.71162],
                     [0.26280, 0.30639, 0.72968],
                     [0.26473, 0.31706, 0.74718],
                     [0.26652, 0.32768, 0.76412],
                     [0.26816, 0.33825, 0.78050],
                     [0.26967, 0.34878, 0.79631],
                     [0.27103, 0.35926, 0.81156],
                     [0.27226, 0.36970, 0.82624],
                     [0.27334, 0.38008, 0.84037],
                     [0.27429, 0.39043, 0.85393],
                     [0.27509, 0.40072, 0.86692],
                     [0.27576, 0.41097, 0.87936],
                     [0.27628, 0.42118, 0.89123],
                     [0.27667, 0.43134, 0.90254],
                     [0.27691, 0.44145, 0.91328],
                     [0.27701, 0.45152, 0.92347],
                     [0.27698, 0.46153, 0.93309],
                     [0.27680, 0.47151, 0.94214],
                     [0.27648, 0.48144, 0.95064],
                     [0.27603, 0.49132, 0.95857],
                     [0.27543, 0.50115, 0.96594],
                     [0.27469, 0.51094, 0.97275],
                     [0.27381, 0.52069, 0.97899],
                     [0.27273, 0.53040, 0.98461],
                     [0.27106, 0.54015, 0.98930],
                     [0.26878, 0.54995, 0.99303],
                     [0.26592, 0.55979, 0.99583],
                     [0.26252, 0.56967, 0.99773],
                     [0.25862, 0.57958, 0.99876],
                     [0.25425, 0.58950, 0.99896],
                     [0.24946, 0.59943, 0.99835],
                     [0.24427, 0.60937, 0.99697],
                     [0.23874, 0.61931, 0.99485],
                     [0.23288, 0.62923, 0.99202],
                     [0.22676, 0.63913, 0.98851],
                     [0.22039, 0.64901, 0.98436],
                     [0.21382, 0.65886, 0.97959],
                     [0.20708, 0.66866, 0.97423],
                     [0.20021, 0.67842, 0.96833],
                     [0.19326, 0.68812, 0.96190],
                     [0.18625, 0.69775, 0.95498],
                     [0.17923, 0.70732, 0.94761],
                     [0.17223, 0.71680, 0.93981],
                     [0.16529, 0.72620, 0.93161],
                     [0.15844, 0.73551, 0.92305],
                     [0.15173, 0.74472, 0.91416],
                     [0.14519, 0.75381, 0.90496],
                     [0.13886, 0.76279, 0.89550],
                     [0.13278, 0.77165, 0.88580],
                     [0.12698, 0.78037, 0.87590],
                     [0.12151, 0.78896, 0.86581],
                     [0.11639, 0.79740, 0.85559],
                     [0.11167, 0.80569, 0.84525],
                     [0.10738, 0.81381, 0.83484],
                     [0.10357, 0.82177, 0.82437],
                     [0.10026, 0.82955, 0.81389],
                     [0.09750, 0.83714, 0.80342],
                     [0.09532, 0.84455, 0.79299],
                     [0.09377, 0.85175, 0.78264],
                     [0.09287, 0.85875, 0.77240],
                     [0.09267, 0.86554, 0.76230],
                     [0.09320, 0.87211, 0.75237],
                     [0.09451, 0.87844, 0.74265],
                     [0.09662, 0.88454, 0.73316],
                     [0.09958, 0.89040, 0.72393],
                     [0.10342, 0.89600, 0.71500],
                     [0.10815, 0.90142, 0.70599],
                     [0.11374, 0.90673, 0.69651],
                     [0.12014, 0.91193, 0.68660],
                     [0.12733, 0.91701, 0.67627],
                     [0.13526, 0.92197, 0.66556],
                     [0.14391, 0.92680, 0.65448],
                     [0.15323, 0.93151, 0.64308],
                     [0.16319, 0.93609, 0.63137],
                     [0.17377, 0.94053, 0.61938],
                     [0.18491, 0.94484, 0.60713],
                     [0.19659, 0.94901, 0.59466],
                     [0.20877, 0.95304, 0.58199],
                     [0.22142, 0.95692, 0.56914],
                     [0.23449, 0.96065, 0.55614],
                     [0.24797, 0.96423, 0.54303],
                     [0.26180, 0.96765, 0.52981],
                     [0.27597, 0.97092, 0.51653],
                     [0.29042, 0.97403, 0.50321],
                     [0.30513, 0.97697, 0.48987],
                     [0.32006, 0.97974, 0.47654],
                     [0.33517, 0.98234, 0.46325],
                     [0.35043, 0.98477, 0.45002],
                     [0.36581, 0.98702, 0.43688],
                     [0.38127, 0.98909, 0.42386],
                     [0.39678, 0.99098, 0.41098],
                     [0.41229, 0.99268, 0.39826],
                     [0.42778, 0.99419, 0.38575],
                     [0.44321, 0.99551, 0.37345],
                     [0.45854, 0.99663, 0.36140],
                     [0.47375, 0.99755, 0.34963],
                     [0.48879, 0.99828, 0.33816],
                     [0.50362, 0.99879, 0.32701],
                     [0.51822, 0.99910, 0.31622],
                     [0.53255, 0.99919, 0.30581],
                     [0.54658, 0.99907, 0.29581],
                     [0.56026, 0.99873, 0.28623],
                     [0.57357, 0.99817, 0.27712],
                     [0.58646, 0.99739, 0.26849],
                     [0.59891, 0.99638, 0.26038],
                     [0.61088, 0.99514, 0.25280],
                     [0.62233, 0.99366, 0.24579],
                     [0.63323, 0.99195, 0.23937],
                     [0.64362, 0.98999, 0.23356],
                     [0.65394, 0.98775, 0.22835],
                     [0.66428, 0.98524, 0.22370],
                     [0.67462, 0.98246, 0.21960],
                     [0.68494, 0.97941, 0.21602],
                     [0.69525, 0.97610, 0.21294],
                     [0.70553, 0.97255, 0.21032],
                     [0.71577, 0.96875, 0.20815],
                     [0.72596, 0.96470, 0.20640],
                     [0.73610, 0.96043, 0.20504],
                     [0.74617, 0.95593, 0.20406],
                     [0.75617, 0.95121, 0.20343],
                     [0.76608, 0.94627, 0.20311],
                     [0.77591, 0.94113, 0.20310],
                     [0.78563, 0.93579, 0.20336],
                     [0.79524, 0.93025, 0.20386],
                     [0.80473, 0.92452, 0.20459],
                     [0.81410, 0.91861, 0.20552],
                     [0.82333, 0.91253, 0.20663],
                     [0.83241, 0.90627, 0.20788],
                     [0.84133, 0.89986, 0.20926],
                     [0.85010, 0.89328, 0.21074],
                     [0.85868, 0.88655, 0.21230],
                     [0.86709, 0.87968, 0.21391],
                     [0.87530, 0.87267, 0.21555],
                     [0.88331, 0.86553, 0.21719],
                     [0.89112, 0.85826, 0.21880],
                     [0.89870, 0.85087, 0.22038],
                     [0.90605, 0.84337, 0.22188],
                     [0.91317, 0.83576, 0.22328],
                     [0.92004, 0.82806, 0.22456],
                     [0.92666, 0.82025, 0.22570],
                     [0.93301, 0.81236, 0.22667],
                     [0.93909, 0.80439, 0.22744],
                     [0.94489, 0.79634, 0.22800],
                     [0.95039, 0.78823, 0.22831],
                     [0.95560, 0.78005, 0.22836],
                     [0.96049, 0.77181, 0.22811],
                     [0.96507, 0.76352, 0.22754],
                     [0.96931, 0.75519, 0.22663],
                     [0.97323, 0.74682, 0.22536],
                     [0.97679, 0.73842, 0.22369],
                     [0.98000, 0.73000, 0.22161],
                     [0.98289, 0.72140, 0.21918],
                     [0.98549, 0.71250, 0.21650],
                     [0.98781, 0.70330, 0.21358],
                     [0.98986, 0.69382, 0.21043],
                     [0.99163, 0.68408, 0.20706],
                     [0.99314, 0.67408, 0.20348],
                     [0.99438, 0.66386, 0.19971],
                     [0.99535, 0.65341, 0.19577],
                     [0.99607, 0.64277, 0.19165],
                     [0.99654, 0.63193, 0.18738],
                     [0.99675, 0.62093, 0.18297],
                     [0.99672, 0.60977, 0.17842],
                     [0.99644, 0.59846, 0.17376],
                     [0.99593, 0.58703, 0.16899],
                     [0.99517, 0.57549, 0.16412],
                     [0.99419, 0.56386, 0.15918],
                     [0.99297, 0.55214, 0.15417],
                     [0.99153, 0.54036, 0.14910],
                     [0.98987, 0.52854, 0.14398],
                     [0.98799, 0.51667, 0.13883],
                     [0.98590, 0.50479, 0.13367],
                     [0.98360, 0.49291, 0.12849],
                     [0.98108, 0.48104, 0.12332],
                     [0.97837, 0.46920, 0.11817],
                     [0.97545, 0.45740, 0.11305],
                     [0.97234, 0.44565, 0.10797],
                     [0.96904, 0.43399, 0.10294],
                     [0.96555, 0.42241, 0.09798],
                     [0.96187, 0.41093, 0.09310],
                     [0.95801, 0.39958, 0.08831],
                     [0.95398, 0.38836, 0.08362],
                     [0.94977, 0.37729, 0.07905],
                     [0.94538, 0.36638, 0.07461],
                     [0.94084, 0.35566, 0.07031],
                     [0.93612, 0.34513, 0.06616],
                     [0.93125, 0.33482, 0.06218],
                     [0.92623, 0.32473, 0.05837],
                     [0.92105, 0.31489, 0.05475],
                     [0.91572, 0.30530, 0.05134],
                     [0.91024, 0.29599, 0.04814],
                     [0.90463, 0.28696, 0.04516],
                     [0.89888, 0.27824, 0.04243],
                     [0.89298, 0.26981, 0.03993],
                     [0.88691, 0.26152, 0.03753],
                     [0.88066, 0.25334, 0.03521],
                     [0.87422, 0.24526, 0.03297],
                     [0.86760, 0.23730, 0.03082],
                     [0.86079, 0.22945, 0.02875],
                     [0.85380, 0.22170, 0.02677],
                     [0.84662, 0.21407, 0.02487],
                     [0.83926, 0.20654, 0.02305],
                     [0.83172, 0.19912, 0.02131],
                     [0.82399, 0.19182, 0.01966],
                     [0.81608, 0.18462, 0.01809],
                     [0.80799, 0.17753, 0.01660],
                     [0.79971, 0.17055, 0.01520],
                     [0.79125, 0.16368, 0.01387],
                     [0.78260, 0.15693, 0.01264],
                     [0.77377, 0.15028, 0.01148],
                     [0.76476, 0.14374, 0.01041],
                     [0.75556, 0.13731, 0.00942],
                     [0.74617, 0.13098, 0.00851],
                     [0.73661, 0.12477, 0.00769],
                     [0.72686, 0.11867, 0.00695],
                     [0.71692, 0.11268, 0.00629],
                     [0.70680, 0.10680, 0.00571],
                     [0.69650, 0.10102, 0.00522],
                     [0.68602, 0.09536, 0.00481],
                     [0.67535, 0.08980, 0.00449],
                     [0.66449, 0.08436, 0.00424],
                     [0.65345, 0.07902, 0.00408],
                     [0.64223, 0.07380, 0.00401],
                     [0.63082, 0.06868, 0.00401],
                     [0.61923, 0.06367, 0.00410],
                     [0.60746, 0.05878, 0.00427],
                     [0.59550, 0.05399, 0.00453],
                     [0.58336, 0.04931, 0.00486],
                     [0.57103, 0.04474, 0.00529],
                     [0.55852, 0.04028, 0.00579],
                     [0.54583, 0.03593, 0.00638],
                     [0.53295, 0.03169, 0.00705],
                     [0.51989, 0.02756, 0.00780],
                     [0.50664, 0.02354, 0.00863],
                     [0.49321, 0.01963, 0.00955],
                     [0.47960, 0.01583, 0.01055]])


def plot_color_gradients(cmap_name, size):
    gradient = np.linspace(0, 1, size[0])
    gradient = np.tile(gradient, (size[1], 1))
    cm = plt.get_cmap(cmap_name)
    out = cm(gradient)[:, :, :3]
    out = out * 255
    out = out.astype(np.uint8)
    font = cv2.FONT_ITALIC
    fontScale = 0.5
    fontColor = (255, 255, 255)
    lineType = 2
    # cv2.putText(out, '-1',
    #             (10, 20),
    #             font,
    #             fontScale,
    #             fontColor,
    #             lineType)
    #
    # cv2.putText(out, '1',
    #             (size[0]-10, 20),
    #             font,
    #             fontScale,
    #             fontColor,
    #             lineType)

    return out