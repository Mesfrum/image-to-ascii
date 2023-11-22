import cv2
import pygame
from PIL import Image

# ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", " ", " "]
ASCII_CHARS = [
    "@",
    "#",
    "S",
    "%",
    "?",
    "*",
    "+",
    ";",
    ":",
    ",",
    ".",
    "o",
    "i",
    "!",
    "|",
    "(",
    ")",
    "[",
    "]",
    "{",
    "}",
    "^",
    "<",
    ">",
    "~",
    "_",
    " ",
    " ",
    " ",
]


def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = float(height) / float(width)
    new_height = int(aspect_ratio * new_width * 0.55)
    resized_image = image.resize((new_width, new_height))
    return resized_image


def grayscale(image):
    return image.convert("L")


def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ""
    for pixel_value in pixels:
        ascii_str += ASCII_CHARS[pixel_value // 10]

    return ascii_str


def convert_frame_to_ascii(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(frame)
    pil_image = resize_image(pil_image)
    pil_image = grayscale(pil_image)
    ascii_str = pixels_to_ascii(pil_image)

    img_width = pil_image.width
    ascii_str_len = len(ascii_str)
    ascii_img = ""
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i : i + img_width] + "\n"

    return ascii_img


cap = cv2.VideoCapture(0)

pygame.init()

font = pygame.font.SysFont("Courier", 12)
line_height = font.get_linesize()

width, height = 800, 600  # Adjust these values as needed
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("ASCII Video")

clock = pygame.time.Clock()

running = True
while running:
    ret, frame = cap.read()
    if not ret:
        break

    ascii_art = convert_frame_to_ascii(frame)
    ascii_lines = ascii_art.split("\n")  # Split the ASCII art into individual lines

    screen.fill((0, 0, 0))

    # Render each line of ASCII art separately and position them line by line
    for i, line in enumerate(ascii_lines):
        text_surface = font.render(line, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10 + i * line_height))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(30)  # Adjust the frame rate as needed

cap.release()
pygame.quit()
