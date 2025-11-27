import argparse
from skull_stripping import skull_stripping

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic MRI images.")

    parser.add_argument("input_path", type=str, help="Path to subject directories")
    args = parser.parse_args()

    skull_stripping(args.input_path)