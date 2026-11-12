import glob
from PIL import Image
from pathlib import Path
import json


def delete_files(dir_path):
    for file_path in dir_path.iterdir():
        if file_path.is_file():
            file_path.unlink()


def square_images(dir_path):
    for file_path in glob.glob(dir_path):
        with Image.open(file_path) as img:
            width, height = img.size
            crop_size = min(width, height)

            left = (width - crop_size) // 2
            top = (height - crop_size) // 2
            right = left + crop_size
            bottom = top + crop_size

            box = (left, top, right, bottom)
            cropped_img = img.crop(box)
            filename_split = img.filename.split("/")
            name = filename_split[-1]
            cropped_img.save(f"{output_dir}/{name}")


def get_input_dir():
    while True:
        try:
            input_dir_path = Path(input("Enter in the file path for your folder of images: "))
            has_files = any(item.is_file() for item in input_dir_path.iterdir())
            if has_files:
                return input_dir_path
            else:
                print("\033[31m Folder does not have any files in it \033[0m")
                print("\033[31m Please add images \033[0m")
        except FileNotFoundError:
            print("\033[31m Folder Not Found \033[0m")
            print("\033[31m Make sure path is typed correctly and folder exists \033[0m")


def get_output_dir():
    while True:
        try:
            print("(Default is 'square_images')")
            output_dir_path = input("Enter a folder for the square images to go: ")
            if output_dir_path == "":
                output_dir_path = Path("./square_images")
            else:
                output_dir_path = Path(output_dir_path)
            output_dir_path.mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            print("\033[31m A FILE exists with that name, Delete that file or make a new name \033[0m")
        else:
            return output_dir_path


def get_pixel_matrix(image):
    width, height = image.size
    pixel_matrix = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(image.getpixel((j, i)))
        pixel_matrix.append(row)
    return pixel_matrix


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


def get_color_to_images_dict(output_dir_path):
    color_to_images_map = {}
    for file_path in glob.glob(output_dir_path):
        with Image.open(file_path) as ref_img:
            ref_img = ref_img.convert("RGB")
            ref_img_size = ref_img.width

            pixel_matrix = get_pixel_matrix(ref_img)
            flat_pixels = [pixel for row in pixel_matrix for pixel in row]

            average_color = str(get_average_color(flat_pixels, ref_img_size))
            # print(average_color)

            if average_color not in color_to_images_map:
                color_to_images_map[average_color] = []
            color_to_images_map[average_color].append(file_path)

    return color_to_images_map


def make_color_to_images_json(dictionary):
    json_file = Path("./colors.json")
    if not json_file.is_file():
        json_file.touch()

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(dictionary, file, indent=4)


if __name__ == '__main__':
    # output_dir = Path("./square_images")
    output_dir = get_output_dir()
    input_dir = get_input_dir()

    delete_files(output_dir)

    contains_subfolders = any(item.is_dir() for item in input_dir.iterdir())
    print("Doing Stuff...")
    if contains_subfolders:
        square_images(f"{input_dir}/*/*")
    else:
        square_images(f"{input_dir}/*")

    make_color_to_images_json(get_color_to_images_dict(f"{output_dir}/*"))
