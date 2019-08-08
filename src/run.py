#!/usr/bin/env python
"""Command line tool to find lights in an image"""
# Standard Imports
import argparse

# Local Imports
from light_detect.detectors import LightDetector


def parse_args():
    """Parse the arguments.

    Returns:
        argparse.Namespace: The command line arguments.
    """
    parser = argparse.ArgumentParser(description="Find the lights in an image.")
    parser.add_argument(
        "-i",
        default=None,
        dest="image_path",
        help="Path to the image file.",
        type=str,
    )
    parser.add_argument(
        "-l",
        default=5,
        dest="blur_length",
        help="Kernel edge length to use when blurring the image. Must be odd.",
        type=int,
    )
    parser.add_argument(
        "-t",
        default=210,
        dest="threshold",
        help="The value to threshold the image on. Must be in (0, 255).",
        type=int,
    )
    parser.add_argument(
        "-p",
        action="store_true",
        dest="print_points",
        help="If set, the (x, y) locations of the lights will be printed.",
    )
    args = parser.parse_args()

    try:
        if not args.image_path:
            raise TypeError("The path to an image must be specified.")

        if args.threshold <= 0 or args.threshold >= 255:
            raise TypeError("The threshold must be in range (0, 255).")

    except TypeError as error:
        print(error)
        print("\nUse the -h switch to see usage information.\n")
        exit()
    return args


def main():
    """Detect the lights in an image."""
    args = parse_args()

    try:
        light_detector = LightDetector(
            args.image_path,
            blur_length=args.blur_length,
            threshold=args.threshold,
        )
        if args.print_points:
            print("Centers:")
            for count, center in enumerate(light_detector.light_centers):
                print(f"{count}: {center}")
        else:
            light_detector.show_lights()

    except FileNotFoundError as error:
        print(error)


if __name__ == "__main__":
    main()
