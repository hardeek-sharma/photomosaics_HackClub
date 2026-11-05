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
            cropped_img.save(f"{output_dir_path}/{name}")

output_dir_path = Path("./square_images")
delete_files(output_dir_path)
square_images("./DIV2K_valid_HR/*.png")