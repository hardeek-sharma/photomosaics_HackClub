from PIL import Image
from PIL import ImageDraw

tile_size = 50

def resize_img(image):
    init_width = image.width
    init_height = image.height
    extra_height = init_height % tile_size
    extra_width = init_width % tile_size
    if extra_width != 0 or extra_height != 0:
        image = image.resize((init_width - extra_width, init_height - extra_height))
        return image
    return image


def get_average_color(square):
    r_holder = 0
    g_holder = 0
    b_holder = 0
    for color in square:
        r, g, b = color
        r_holder += r
        g_holder += g
        b_holder += b

    r_holder = round(r_holder / (tile_size ** 2))
    g_holder = round(g_holder / (tile_size ** 2))
    b_holder = round(b_holder / (tile_size ** 2))

    return r_holder, g_holder, b_holder


def get_average_tiled_image(pixel_list):
    average_pixel_list_holder = []
    for i in range(height_tiles):
        row_holder = []
        for j in range(width_tiles):
            square = []
            for k in range(tile_size):
                for l in range(tile_size):
                    square.append(pixel_list[(i * tile_size) + k][(j * tile_size) + l])
            average_square = get_average_color(square)
            row_holder.append(average_square)
        average_pixel_list_holder.append(row_holder)
    return average_pixel_list_holder



def get_pixels(image):
    pixels_holder = []
    for x in range(height):
        row = []
        for y in range(width):
            pixel = img.getpixel((y, x))
            row.append(pixel)
        pixels_holder.append(row)
    return pixels_holder


def show_pixelated_image(pixel_list):
    new_image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(new_image)
    for i in range(height_tiles):
        for j in range(width_tiles):
            coordinates = (j * tile_size, i * tile_size, (j+1) * tile_size, (i+1) * tile_size)
            draw.rectangle(coordinates, pixel_list[i][j])
            print(coordinates)
    new_image.show()


with Image.open("Bruno.png") as img:
    img = resize_img(img)
    img = img.convert("RGB")
    width, height = img.size
    width_tiles = int(width/tile_size)
    height_tiles = int(height/tile_size)
    pixels = get_pixels(img)
    average_pixels = get_average_tiled_image(pixels)
    show_pixelated_image(average_pixels)

