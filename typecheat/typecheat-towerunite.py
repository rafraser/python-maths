"""
Type cheating script for Bottimus typerace game
This takes a screenshot of the screen and feeds it through Tesseract before typing it out
This can reach very fast speeds - but there are some issues with the game that cause it to break down
I would not recommend using this for anything more than proof of concept
"""
import cv2
import pytesseract
import numpy
import pyautogui
import keyboard
import time
from PIL import ImageGrab

# Step 1: Find the Tower Unite window
# TODO: Find the Tower Unite window instead of guesstimating the position
"""
uniteWindow = win32gui.FindWindow(None, "Tower Unite")
print(uniteWindow)
rect = win32gui.GetWindowRect(uniteWindow)
print(rect)
"""

abort = False
auto_do = False

while True:
    while True:
        try:
            if auto_do:
                time.sleep(0.25)
                break

            if keyboard.is_pressed("1"):
                break
            if keyboard.is_pressed("2"):
                abort = True
                break
            if keyboard.is_pressed("3"):
                auto_do = True
                break
        except:
            continue

    # Exit
    if abort:
        break

    if auto_do:
        if keyboard.is_pressed("2"):
            auto_do = False
        pyautogui.typewrite(" ")

    start_time = time.time()

    # Step 2: Screenshot the text
    screenshot = ImageGrab.grab(bbox=(680, 700, 1250, 750)).convert("RGB")

    # Step 3: OpenCV processing
    image = numpy.array(screenshot)
    image = image[:, :, ::-1].copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 80, 255, cv2.THRESH_BINARY_INV)[1]
    cv2.imwrite(str(start_time) + ".jpg", image)

    # Step 4: Figure out the text using Tesseract
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
    result = (
        pytesseract.image_to_string(image, lang="eng")
        .replace("\n", " ")
        .replace("|", "I")
    )
    end_time = time.time()
    print("Time: ", end_time - start_time)
    print(result)
    pyautogui.typewrite(result, interval=0.01)
