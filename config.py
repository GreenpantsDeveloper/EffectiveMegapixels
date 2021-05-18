# The low resolution at which practically every image should be considered sharp (works best for non-panorama images)
# Recommended value: 200
MIN_RESOLUTION_WIDTH = 200

# Number of times the input image is downscaled up to the MIN_RESOLUTION_WIDTH. The higher the number, the more accurate the results, up to a certain number over 40 where the knee cannot accuracy be determined. A higher number also takes longer to compute.
# Recommended value: between 20 and 40
NUM_DOWNSCALES = 20

# Whether the downscaling resolutions should be exponential (computing with more high-res than low-res samples, thus higher accuracy for high E-MP images).
# Recommended value: True
DOWNSCALE_EXPONENTIALLY = False

# Whether to show the plot of the computed sharpness/contrast values per downscaled image. Useful for inspecting correctness.
# Recommended: True, at least when starting out
SHOW_PLOT = True
