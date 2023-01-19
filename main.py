from PIL import Image
import sys
import os


def add_char(i, j, brightness):
    part_number = brightness//(256//len_char)-1
    if (j == 0):
        f.write('\n')
    f.write(charSet[part_number % len_char])


def merge_sq(i, j):
    average_pixel_brightness = 0

    for row in range(i, i+boundary):
        if (row > height-1):
            row = height-1
        for col in range(j, j+boundary):
            if col > width-1:
                col = width-1

            r, g, b = sample_image_1.getpixel((col, row))
            brightness = int(sum([r, g, b])/3)
            average_pixel_brightness += brightness
    average_pixel_brightness = average_pixel_brightness//(boundary*boundary)
    add_char(i, j, average_pixel_brightness)


boundary = 50

charSet = r'$@%&#*/(){}[]?-_+~<>!;:,"^`.            '
len_char = len(charSet)
print('charst length =', len_char)

user_input = input("Enter the path of your file: ")
user_input = user_input.replace('"', '')

if (not os.path.exists(user_input)):
    sys.exit("I did not find the file at, "+str(user_input))

sample_image_1 = Image.open(user_input, 'r')

width, height = sample_image_1.size  # get the size of the image

print('size =', sample_image_1.size, '\narea =',
      width*height, '\nboundary =', boundary)

with open('asciitxt.html', 'w') as f:
    f.write('<link rel="stylesheet" href="style.css">\n<plaintext>\n')

    for i in range(0, height, boundary):
        for j in range(0, width, boundary):
            merge_sq(i, j)

    f.write('\n</plaintext>\n')
os.startfile(r'asciitxt.html')