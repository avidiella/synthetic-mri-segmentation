import argparse
from preprocessing_masks import process_masks
from image_generation import generate_synth_images_batch

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic MRI images.")

    parser.add_argument("freesurfer_directory", type=str, help="Path of a standard FreeSurfer subject directory")
    parser.add_argument("file_output", type=str, help="Directory where images will be generated")
    parser.add_argument("n_examples", type=int, help="Number of synthetic images to create per mask/subject")

    args = parser.parse_args()

    process_masks(args.freesurfer_directory)
    generate_synth_images_batch(args.freesurfer_directory, args.file_output, args.n_examples)