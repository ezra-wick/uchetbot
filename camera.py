# -*- coding: utf-8 -*-
import cv2
import pytesseract
import imutils
import easyocr
import itertools
import numpy as np
from PIL import Image, ImageEnhance


def add_capture():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
    else:
        img_name = "data/weight.png"
        cv2.imwrite(img_name, frame)
    cam.release()
    cv2.destroyAllWindows()



def remove_color(image, color):
    image = Image.open(image)
    image.show()
    image_data = image.load()
    height,width = image.size
    for loop1 in range(height):
        for loop2 in range(width):
            r,g,b = image_data[loop1,loop2]
            image_data[loop1,loop2] = r,0,b
    image.save(image)



def replace_color(image, colors):
    im = Image.open(image)
    im = im.convert('RGBA')

    for color in colors:
        data = np.array(im)   # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

        # Replace white with red... (leaves alpha values alone...)
        white_areas = (red == color[0]) & (blue == color[2]) & (green == color[1])
        data[..., :-1][white_areas.T] = (255, 0, 0) # Transpose back needed

        im = Image.fromarray(data)


    im.save(image)

def recognize(image):
    im = Image.open(image).convert('RGB')                                                                

    # Sharpen sharpener = PIL.ImageEnhance.Sharpness (img.convert('RGB'))
    # enhancer = ImageEnhance.Sharpness(im)
    # res = enhancer.enhance(4) 

    # # Improve contrast
    # enhancer = ImageEnhance.Contrast(res)
    # res = enhancer.enhance(2)

    # # Save to disk
    # res.save(image)

    reader = easyocr.Reader(['en'])
    results = reader.readtext(image)

    text =''
    for result in results:

        text += result[1] + ' '

    return text
    # image = cv2.imread(image)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # # Otsu Tresholding automatically find best threshold value
    # _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    
    # # invert the image if the text is white and background is black
    # count_white = np.sum(binary_image > 0)
    # count_black = np.sum(binary_image == 0)
    # if count_black > count_white:
    #     binary_image = 255 - binary_image
        
    # # padding
    # final_image = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"    
    # txt = pytesseract.image_to_string(
    #     final_image, config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
    # image_final = Image.fromarray(txt)    
    # image_final.show()

if __name__ == "__main__":
    add_capture()
    # export PYTHONIOENCODING=utf-8
    print(recognize('data/weight.png'))

    # colors = [(0, 33, 19), (15, 36, 31),  (29, 44, 37), (12, 40, 33), (18,24,18), (12, 48, 35), (5, 46, 30)]
    # colors = []
    # red_set = []
    # green_set = []
    # blue_set = []
    


    # for red in range(0, 10):
    #     red_set.append(red)
    # counter = 0
    # for green in range(24, 46):
    #     green_set.append(green)
    # for blue in range(18, 38):
    #     blue_set.append(blue)
    # print(red_set, green_set, blue_set)

    # colors = [set(red_set), set(green_set), set(blue_set)]
    # colors = list(itertools.product(*colors))

    # replace_color('data/weight.png', colors)