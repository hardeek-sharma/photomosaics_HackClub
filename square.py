import glob
from PIL import Image
from pathlib import Path


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


if __name__ == '__main__':
    # output_dir = Path("./square_images")
    output_dir = get_output_dir()
    input_dir = get_input_dir()

    delete_files(output_dir)
    square_images(input_dir)