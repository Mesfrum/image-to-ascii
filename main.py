# This is my attempt at making a image to ascii converter
# This program is one of my first projects and hence is not perfect
# Anyone with suggestions and willingness to contribute is welcome.

from PIL import Image
import sys
import os

# Function to convert pixel brightness into ascii character

def add_char(i, j, brightness):
    # calculating the equivalent of the brightness to the character
    char_number = brightness//(256//len_char)-1
    if (j == 0):
        # when reached the end of line start on new
        f.write('\n')

    # prit equivalent character from characer set onto the html
    f.write(charSet[char_number % len_char])

#  Function to merge all the pixels within the boundary into a single pixel

def merge_sq(i, j):
    average_pixel_brightness = 0            # initialize average brightness of pixel

    for row in range(i, i+boundary):        # iterate through all pixels within boundary
        if (row > height-1):                # wrap if going out of bounds
            row = height-1
        for col in range(j, j+boundary):
            if col > width-1:
                col = width-1               # wrap if going out of bounds

            r, g, b = sample_image_1.getpixel(
                (col, row))       # strip rgb values of pixel

            # average rgb values to get brightness i.e. a grayscaled pixel
            brightness = int(sum([r, g, b])/3)

            # add the brightness to average poxel brightnesss which will be used to calculate the average brightness
            average_pixel_brightness += brightness

    # calculate average brightness for all the pixels
    average_pixel_brightness = average_pixel_brightness//(boundary*boundary)

    # proceed to add characater to html
    add_char(i, j, average_pixel_brightness)


# Define character set
charSet = r'$@%&#*/(){}[]?-_+~<>!;:,"^`. '
len_char = len(charSet)

# Take user input i.e. a path to a image
user_input = input("Enter the path of your file: ")
user_input = user_input.replace('"', '')

# validate path
if (not os.path.exists(user_input)):
    sys.exit("I did not find the file at, "+str(user_input))

# open image in the path and convert into a .jpg format
sample_image_1 = Image.open(user_input, 'r')
sample_image_1 = sample_image_1.convert('RGB')
sample_image_1.save('colors.jpg')

# get dimensions of image
width, height = sample_image_1.size  # get the size of the image
pix = width*height

# Calculate resolution(pix as in pixels) and set a boundary value
if (pix >= 7680*4320):
    print('This is an 8k image.\nIt will take a few minutes!!')
    boundary = 70
elif (pix >= 3840*2160):
    print('This is an 4k image')
    boundary = 30
elif (pix >= 1280*720):
    print('THis is a HD image')
    boundary = 10
elif (pix >= 640*480):
    print('THis is a image with <HD quality.')
    boundary = 5
else:
    boundary = 3

# details about Conversion to ascii
print('charst length =', len_char, '\nsize =', sample_image_1.size, '\narea =',
      width*height, '\nboundary =', boundary)

# open a new html document
with open('asciitxt.html', 'w') as f:
    # link html to css
    f.write('<link rel="stylesheet" href="style.css">\n<plaintext>\n')

    # iterate through each pixel while merging boundary pixels together
    for i in range(0, height, boundary):
        for j in range(0, width, boundary):
            merge_sq(i, j)

# open html file
os.startfile(r'asciitxt.html')
