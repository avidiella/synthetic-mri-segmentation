import argparse
from preprocess_real import real_mri_preprocessing
from preprocess_synth import synthetic_mri_preprocessing

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["real", "synth"], required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    if args.mode == "real":
        real_mri_preprocessing(args.input, args.output)

    else:
        synthetic_mri_preprocessing(args.input, args.output)


if __name__ == "__main__":
    main()
