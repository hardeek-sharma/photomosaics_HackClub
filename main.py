import json
from pathlib import Path
from PIL import Image, ImageDraw, UnidentifiedImageError
import math
import random


def resize_image_to_grid(image):
    original_width, original_height = image.size
    remainder_height = original_height % TILE_SIZE
    remainder_width = original_width % TILE_SIZE
    if remainder_width != 0 or remainder_height != 0:
        new_width = original_width - remainder_width
        new_height = original_height - remainder_height
        image = image.resize((new_width, new_height))
        return image
    return image


def get_average_color(square, size):
    total_red = 0
    total_green = 0
    total_blue = 0
    total_pixels = size ** 2
    for color in square:
        r, g, b = color[:3]
        total_red += r
        total_green += g
        total_blue += b
    return (
        round(total_red / total_pixels),
        round(total_green / total_pixels),
        round(total_blue / total_pixels)
    )


def get_mosaic_color_grid(pixel_list, width_tiles, height_tiles):
    mosaic_grid = []

    for tile_row in range(height_tiles):
        row_averages = []
        for tile_column in range(width_tiles):
            tile_pixels = []

            for i in range(TILE_SIZE):
                for j in range(TILE_SIZE):
                    pixel_y = (tile_row * TILE_SIZE) + i
                    pixel_x = (tile_column * TILE_SIZE) + j
                    tile_pixels.append(pixel_list[pixel_y][pixel_x])

            average_color = get_average_color(tile_pixels, TILE_SIZE)
            row_averages.append(average_color)

        mosaic_grid.append(row_averages)

    return mosaic_grid


def get_pixel_matrix(image):
    width, height = image.size
    pixel_matrix = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(image.getpixel((j, i)))
        pixel_matrix.append(row)
    return pixel_matrix


def show_pixelated_image(pixel_list):
    pixelated_image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(pixelated_image)
    for i in range(height_tiles):
        for j in range(width_tiles):
            box_coordinates = (j * TILE_SIZE, i * TILE_SIZE, (j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE)
            tile_color = pixel_list[i][j]
            draw.rectangle(box_coordinates, tile_color)
            print(box_coordinates)

    pixelated_image.show()


def get_json_to_dict():
    with open("colors.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def get_closest_color_path(target_color, color_key):
    best_color_paths = ""
    best_distance = None

    target_red, target_green, target_blue = target_color

    for color, paths in color_key.items():
        if type(color) == type(""):
            # Color is given as a string, "(1, 2, 3)" rather than a tuple
            # So it strips the "()" separates each number be ", " and makes it back into a tuple
            color = (int(x) for x in str(color.strip("()")).split(", "))
            # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        key_red, key_green, key_blue = color
        distance = math.sqrt(
            (target_red - key_red) ** 2 + (target_green - key_green) ** 2 + (target_blue - key_blue) ** 2)

        if best_distance is None or distance < best_distance:
            best_color_paths = paths
            best_distance = distance

    return random.choice(best_color_paths)


def get_images_matrix(pixel_matrix, color_key):
    file_matrix = []
    for row in pixel_matrix:
        file_row = []
        for pixel in row:
            file_row.append(get_closest_color_path(pixel, color_key))
        file_matrix.append(file_row)
    return file_matrix


def create_photomosaic(file_matrix):
    num_rows = len(file_matrix)
    num_cols = len(file_matrix[0])

    canvas_width = num_cols * IMAGE_SIZE
    canvas_height = num_rows * IMAGE_SIZE

    canvas = Image.new("RGB", (canvas_width, canvas_height), (0, 0, 0))

    for i in range(num_rows):
        for j in range(num_cols):
            with Image.open(file_matrix[i][j]) as image:
                image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
                x_offset = j * IMAGE_SIZE
                y_offset = i * IMAGE_SIZE

                canvas.paste(image, (x_offset, y_offset))
    print(canvas_width, canvas_height)
    canvas.show()


def get_input_image():
    while True:
        try:
            input_image = Path(input("Enter in the file path for an image to make a mosaic of: "))
            with Image.open(input_image) as file:
                file.verify()
            return input_image
        except FileNotFoundError:
            print("\033[31m File Not Found \033[0m")
            print("\033[31m Make sure path is typed correctly and file exists \033[0m")
        except (UnidentifiedImageError, IsADirectoryError):
            print("\033[31m File Is Not An IMAGE FILE \033[0m")
            print("\033[31m Enter an IMAGE FILE \033[0m")


def get_parse_size():
    print("  The square is the block that breaks up each image into tiles\n"
          "  so a size of 1 with convert each pixel of the image to an image\n"
          "  a size of make a 50x50 square and make every 2500 pixels into an image\n"
          "  basically lower number is high quality, high number is low quality.")
    while True:
        try:
            parse_size = input("Enter a size for the square (Default: 50): ")
            if parse_size == "":
                return 50
            parse_size = int(parse_size)
            if parse_size <= 0 or parse_size > width or parse_size > height:
                print("\033[31m Square cannot be less than 1 or more than image width/height \033[0m")
                continue
            return parse_size
        except ValueError:
            print("\033[31m Enter a NUMBER \033[0m")


def get_tile_size():
    print("  The tile size determines how big each image that makes up the photomosaic will be")
    while True:
        try:
            tile_size = input("Enter a size for the tiles (Default 50): ")
            if tile_size == "":
                return 50
            tile_size = int(tile_size)
            if tile_size <= 0:
                print("\033[31m Tile cannot be 0 pixels \033[0m")
                continue
            return tile_size
        except ValueError:
            print("\033[31m Enter a NUMBER \033[0m")


if __name__ == '__main__':
    img_file = get_input_image()
    with Image.open(img_file) as img:
        width, height = img.size

        TILE_SIZE = get_parse_size()
        IMAGE_SIZE = get_tile_size()

        img = resize_image_to_grid(img)
        img = img.convert("RGB")

        width, height = img.size
        width_tiles = width // TILE_SIZE
        height_tiles = height // TILE_SIZE

        pixels = get_pixel_matrix(img)
        average_pixels = get_mosaic_color_grid(pixels, width_tiles, height_tiles)

        # show_pixelated_image(average_pixels)
        # image_matrix = get_images_matrix(average_pixels, get_color_to_images_dict("./square_images"))
        image_matrix = get_images_matrix(average_pixels, get_json_to_dict())

        create_photomosaic(image_matrix)
