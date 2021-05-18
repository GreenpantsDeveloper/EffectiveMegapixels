import os, sys
from PIL import Image, ImageOps

from util import compute_effective_mp


if __name__ == '__main__':
    # Ensure there is a file
    if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
        print("Error: this script requires the path to one file as argument. Exiting...")
        sys.exit(0)
    
    # Get the file
    filepath = sys.argv[1]
    print("File: \t\t\t%s" % filepath)

    # Open the file
    try:
        img = Image.open(filepath)
    except OSError:
        print("Error: file extension is not supported. Exiting..." % filepath)
        sys.exit(0)
    
    # Grayscale
    img = ImageOps.grayscale(img)
    w, h = img.size
    true_mp = w*h/1000000
    print("Actual resolution: \t%.1f MP (%dx%d pixels)\n" % (true_mp, w, h))

    effective_mp = compute_effective_mp(img)

    if effective_mp is not None:
        print("\nEffective Megapixels: \t%.1f E-MP" % effective_mp)
    else:
        print("\nNo significant sharpness differences could be found; try again with a different image")
