"""
Type cheating script for Bottimus type racers
Unlike the Tower Unite type racer, this takes in an image directly instead of screenshot shennagins
This does make it slightly more cumbersome to use, but it should work out okay
"""
import cv2
import pytesseract
import numpy
import pyautogui
import keyboard
import time
from PIL import Image

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load the image
input()
screenshot = Image.open("typeracer.png")
start_time = time.time()

# Process the image using Numpy so it's easy for Tesseract to decipher
image = numpy.array(screenshot)
image = image[:, :, ::-1].copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = cv2.threshold(image, 80, 255, cv2.THRESH_BINARY_INV)[1]
cv2.imwrite(str(start_time) + ".jpg", image)

# Run the image through Tesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
result = (
    pytesseract.image_to_string(image, lang="eng").replace("\n", " ").replace("|", "I")
)
end_time = time.time()
print("Time: ", end_time - start_time)

# Wait until F1 is pressed
while True:
    if keyboard.is_pressed("f1"):
        break

# Type out the message
pyautogui.typewrite(result, interval=0)
keyboard.press("enter")

