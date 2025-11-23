from lab2im.image_generator import ImageGenerator
from lab2im import utils
import time
import os

def generate_synthetic_images(mask_input, result_dir, n_examples):
    """
    Generate as many synthetic images as desired from a segmentation mask.

    :param mask_input: (str) Path to segmentation mask in nii.gz to be used as ground truth.
    :param result_dir: (str) Directory where the output must be generated.
    :param n_examples: (int) Number of synthetic MRI scans and masks to be generated.

    :return: Prints progress messages for each processed file, also announces when a batch
    is done.
    """
    # Ignore GPUs for CUDA compatibility
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    # Iterate for n_examples
    for n in range(1, n_examples + 1):
        # Start timer
        start = time.time()

        # Generate synthetic MRI and segmentation mask
        brain_generator = ImageGenerator(mask_input)
        im, lab = brain_generator.generate_image()

        # Convert to NIfTI and save
        utils.mkdir(result_dir)
        utils.save_volume(im, brain_generator.aff, brain_generator.header,
                          os.path.join(result_dir, "brain_%s.nii.gz" % n))
        utils.save_volume(lab, brain_generator.aff, brain_generator.header,
                          os.path.join(result_dir, "labels_%s.nii.gz" % n))

        # End timer
        end = time.time()
        print("Generation {0:d} took {1:.01f}s".format(n, end - start))
    print("Batch is done!")

def generate_synth_images_batch(subjects_dir, result_dir, n_examples):
    """
    Generate as many synthetic images as desired from a segmentation mask.

    This function assumes the default file hierarchy in a Freesurfer project, searches
    for file `processed_mask.nii.gz` generated with `preprocessing_masks` module and
    implements function `generate_synthetic_images` for each subject, creating a folder
    with `n_examples` synthetic MRI scans and segmentation masks.

    :param subjects_dir: A standard FreeSurfer subject directory.
    :param result_dir: Directory where folders per subject with synthetic MRI scans and
    segmentation tasks will be generated.
    :param n_examples: Number of synthetic MRI scans and masks to be generated.
    :return: Prints progress messages for each processed file, also announces when a batch
    is done.
    """
    # To generate as many images as needed from a batch of segmentation masks
    inventory_list = os.listdir(subjects_dir)

    # Iterate through all subjects and create preprocessed mask
    for i in inventory_list:
        dirs = os.path.join(subjects_dir, i, "mri", "processed_mask.nii.gz")

        # Create directory per subject in inventory
        subject_out = os.path.join(result_dir, f"{i}_synth")
        os.makedirs(subject_out, exist_ok=True)

        # Generate synthetic images
        generate_synthetic_images(dirs, subject_out, n_examples)