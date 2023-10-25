#!/usr/bin/python3

import argparse
import json

from PIL import Image, ImageDraw, ImageFont

from config import (
    BANNER_HEIGHT_INITIAL,
    BANNER_WIDTH_INITIAL,
    FONT_NAME_DEFAULT,
    FONT_SIZE,
    INPUT_FILENAME_DEFAULT,
    LINE_SPACING,
    OUTPUT_FILENAME_DEFAULT,
    RESIZE_DIMENSIONS,
    X_START_POSITION,
    Y_START_POSITION,
)


def hex_to_rgb(value: str) -> tuple:
    """Convert a string in format "XXXXXX" to an RGB tuple."""
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate banners with gradient backgrounds."
    )
    parser.add_argument(
        "rgb_start",
        type=lambda s: hex_to_rgb(s.upper()),
        help='Starting RGB color of the gradient in hex format (e.g., "FFFFFF").',
    )
    parser.add_argument(
        "rgb_end",
        type=lambda s: hex_to_rgb(s.upper()),
        help='Ending RGB color of the gradient in hex format (e.g., "FF00FF").',
    )
    return parser.parse_args()


def load_json_config(filename: str) -> dict:
    with open(filename, "r") as file:
        return json.load(file)


def generate_horizontal_gradient(start_color: tuple, end_color: tuple) -> Image:
    gradient = Image.new("RGB", (BANNER_WIDTH_INITIAL, BANNER_HEIGHT_INITIAL))
    draw = ImageDraw.Draw(gradient)

    for x in range(BANNER_WIDTH_INITIAL):
        r = int(
            start_color[0] * (1 - x / BANNER_WIDTH_INITIAL)
            + end_color[0] * (x / BANNER_WIDTH_INITIAL)
        )
        g = int(
            start_color[1] * (1 - x / BANNER_WIDTH_INITIAL)
            + end_color[1] * (x / BANNER_WIDTH_INITIAL)
        )
        b = int(
            start_color[2] * (1 - x / BANNER_WIDTH_INITIAL)
            + end_color[2] * (x / BANNER_WIDTH_INITIAL)
        )
        draw.line((x, 0, x, BANNER_HEIGHT_INITIAL), fill=(r, g, b))

    return gradient


def get_font(font_size: int) -> ImageFont:
    try:
        return ImageFont.truetype(FONT_NAME_DEFAULT, font_size)
    except IOError:
        return ImageFont.load_default()


def create_banner(gradient_image: Image, text_lines: dict) -> Image:
    draw = ImageDraw.Draw(gradient_image)
    font = get_font(FONT_SIZE)

    y_position = Y_START_POSITION
    x_position = X_START_POSITION

    for line_label in sorted(text_lines.keys()):
        line = text_lines[line_label]
        draw.text((x_position, y_position), line, font=font, fill="white")
        y_position += LINE_SPACING

    return gradient_image


def save_banner(banner: Image, filename: str) -> None:
    banner = banner.resize(RESIZE_DIMENSIONS)
    banner.save(filename)


if __name__ == "__main__":
    args = parse_arguments()
    gradient_image = generate_horizontal_gradient(args.rgb_start, args.rgb_end)
    banner_texts = load_json_config(INPUT_FILENAME_DEFAULT)
    banner_image = create_banner(gradient_image, banner_texts)
    save_banner(banner_image, OUTPUT_FILENAME_DEFAULT)
