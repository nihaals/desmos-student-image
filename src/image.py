from typing import Iterator

from PIL import Image as PILImage

import config
from typed_desmos import Point

# Coordinates grid
# DESMOS_MIN_X = -20
# DESMOS_MAX_X = 20
# DESMOS_MIN_Y = -20
# DESMOS_MAX_Y = 20
# DESMOS_SIZE_BETWEEN_PIXEL = 0.045

# Sketch
DESMOS_MIN_X = -1
DESMOS_MAX_X = 1
DESMOS_MIN_Y = -0.75
DESMOS_MAX_Y = 0.75
DESMOS_SIZE_BETWEEN_PIXEL = 0.002

assert DESMOS_MAX_X > DESMOS_MIN_X
assert DESMOS_MAX_Y > DESMOS_MIN_Y

DESMOS_RESOLUTION = (
    int(abs(DESMOS_MIN_X) + abs(DESMOS_MAX_X) // DESMOS_SIZE_BETWEEN_PIXEL),
    int(abs(DESMOS_MIN_Y) + abs(DESMOS_MAX_Y) // DESMOS_SIZE_BETWEEN_PIXEL),
)


def convert_to_desmos_coordinates(x: int, y: int) -> tuple[float, float]:
    """Convert pixel (x, y) to Desmos sketch (x, y)."""
    x_perc = x / DESMOS_RESOLUTION[0]
    y_perc = y / DESMOS_RESOLUTION[1]

    x_range = DESMOS_MAX_X - DESMOS_MIN_X
    y_range = DESMOS_MAX_Y - DESMOS_MIN_Y

    x_out = (x_perc * x_range) + DESMOS_MIN_X
    y_out = DESMOS_MAX_Y - (y_perc * y_range)

    x_out = round(x_out, 4)
    y_out = round(y_out, 4)

    return x_out, y_out


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def remove_transparency(im, bg_colour=(255, 255, 255)):
    # Only process if image has transparency (http://stackoverflow.com/a/1963146)
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):

        # Need to convert to RGBA if LA format due to a bug in PIL (http://stackoverflow.com/a/1963146)
        alpha = im.convert("RGBA").split()[-1]

        # Create a new background image of our matt color.
        # Must be RGBA because paste requires both images have the same format
        # (http://stackoverflow.com/a/8720632 and http://stackoverflow.com/a/9459208)
        bg = PILImage.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg

    else:
        return im


class Image:
    def __init__(self) -> None:
        image = PILImage.open(config.image_path)
        if config.preserve_aspect_ratio is True:
            ratio = min(
                DESMOS_RESOLUTION[0] / image.size[0],
                DESMOS_RESOLUTION[1] / image.size[1],
            )
            resized_image = image.resize(tuple(int(ratio * i) for i in image.size))
            image = PILImage.new("RGBA", DESMOS_RESOLUTION, (255, 255, 255, 255))
            image.paste(resized_image)
        else:
            image = image.resize(DESMOS_RESOLUTION)
        image = remove_transparency(image)
        image = image.convert("RGB")
        self.pixels = image.load()
        self.size = image.size

    def get_points(self) -> Iterator[Point]:
        """Converts image to Desmos API points."""
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                desmos_coordinates = convert_to_desmos_coordinates(x, y)
                colour = rgb_to_hex(*self.pixels[x, y])
                point: Point = {
                    "color": colour,
                    "coords": {
                        "x": desmos_coordinates[0],
                        "y": desmos_coordinates[1],
                    },
                }
                yield point
