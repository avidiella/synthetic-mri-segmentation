# Image pre-processing
This folder contains a program designed to pre-process synthetic MRI images and segmentation masks.

## 1. About the program

The contents of the module are the following:

* File `main.py`, which executes the program.
* File `preprocess_real.py`, the module dedicated to pre-processing real MRI images.
* File `preprocess_synth.py`, the module dedicated to pre-processing synthetic MRI images and its segmentation masks.
* File `requirements.txt`, contains libraries needed to execute the program.
* File `README.md`, contains information about the program and how to execute it.

For real MRI images, the pre-processing steps, the pre-processing steps applied are:
1. Resize images to 256x256x256 by zero-padding
2. Extract brain mask to remove background
3. Clip and normalize intensities inside the brain

For synthetic MRI images and segmentation masks, the pre-processing steps applied are:
1. Reorient segmentation mask from LIA to RAS
2. Create brain mask by merging labels 1 = GM, 2 = WM, 3 = CSF.
3. Reorient synthetic MRI from LIA to RAS
4. Apply brain mask to extract brain and remove background
5. Clip and normalize intensities inside the brain

## 2. How to execute the program

Before executing the program, be sure to install the necessary libraries from requirements.txt. In developing this program, the python version used was 3.12.12.

``pip install -r requirements.txt``

## 3. Steps to execute main.py

To execute this program, the main.py file should be called specifying the following arguments:

* `mode`: To select if the user wants to pre-process real or synthetic images. Takes two values, `real` or `synth`.
* `input`: The directory containing different subject's folders.
* `output`: The directory where the pre-processed images will be saved.

``python main.py --mode --input --output``

## 4. Outputs
Running this program will output several strings providing information about the image pre-processing progress and save the pre-processed images (real MRI or synthetic MRI and synthetic masks) into the chosen path.

See an example of the pre-processing results:

![Pre-processing results](pre-processing_results.png "Pre-processing results")
