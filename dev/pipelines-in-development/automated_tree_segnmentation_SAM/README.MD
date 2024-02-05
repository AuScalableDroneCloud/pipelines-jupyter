This pipeline requires GPU to run, so make sure to be on an image with GPU access.


# Workflow

1. **Drone Captured Image**
   - The initial input is an image captured by a drone.

2. **DeepForest**
   - The drone-captured image is processed using the DeepForest model to identify trees.

3. **Bounding Boxes for Trees**
   - From the processed image, bounding boxes are created around the identified trees.

4. **SAM (Segment Anything Model)**
   - The bounding boxes are then used with the SAM model to segment the trees.

5. **Tree Masks**
   - The output from SAM is used to create masks for individual trees.

6.1 **Average Greenness (or other indices if appropriate bands are available)**
   - Calculate average greenness or other vegetative indices if the necessary spectral bands are available.

6.2 **Projected Tree Area**
   - Calculate the projected area of the trees from the drone imagery.

This flow represents the sequence of steps from image capture to tree area calculation.
