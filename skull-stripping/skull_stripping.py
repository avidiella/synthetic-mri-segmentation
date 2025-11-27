import os
import subprocess

def skull_stripping(input_path):
    """
    Applies HD-BET to multiple MRI scans.

    This function scans the input path to find all the nii.gz files and generates
    a command to be executed for each MRI file. It produces a new nii.gz file after
    performing the brain extraction in the subject directory.

    :param input_path: Path to subject directories.
    :return: Several strings updating on the skull-stripping process.
    """
    # Scan files and folders
    for root, dirs, files in os.walk(input_path):
        for file in files:
            # Identify nii.gz files
            if file.endswith(".nii.gz"):
                # Generate hd-bet argument --input_path
                input_path = os.path.join(root, file)
                # Generate hd-bet argument --output_path
                output_path = os.path.join(root, file.replace(".nii.gz", "_stripped.nii.gz"))

                # Generate command and run
                print(f"Processing: {input_path}")
                cmd = f'hd-bet -i "{input_path}" -o "{output_path}"'
                subprocess.run(cmd, shell=True)
                print(f"Done: {output_path}")