# import re
# import time
# import argparse
# import locale
# import datetime


# from luma.led_matrix.device import max7219
# from luma.core.interface.serial import spi, noop
# from luma.core.render import canvas
# from luma.core.virtual import viewport
# from luma.core.legacy import text, show_message
# from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
# from itertools import repeat



# import time
# import RPi.GPIO as GPIO
# from keypad import keypad

# lastDigit=''

# def demo(n, block_orientation, rotate,d,l):
#     # create device for linear preassembled 4x8x8 max7219 matrix
#     serial = spi(port=0, device=0, gpio=noop())
#     device = max7219(serial, cascaded=4, block_orientation=-90)
#     device.contrast(0x05)
#     print("Created device")
#     # note: change device.contrast value (0xXX) to change leds brightness

#     # start scrolling text demo - just once at startup
#     msg = "Hello bigsleepdata"
#     print(msg)
#     show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.05)

#     # MAX7219 4x8x8 LED Matrix Clock
#     for _ in repeat(None):
#         if d!=l:
#             break
#         else:
#             time.sleep(1)
#             msg= d
#             with canvas(device) as draw:
#             text(draw, (1, 0), msg, fill="white")
#     time.sleep(1)
#     pass


# if __name__ == "__main__":
#     # Initialize
#     kp = keypad(columnCount = 4)
#     parser = argparse.ArgumentParser(description='matrix_demo arguments',
#         formatter_class=argparse.ArgumentDefaultsHelpFormatter)

#     parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 LED matrices')
#     parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
#     parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')

#     args = parser.parse_args()

#     # waiting for a keypress
#     while 1:
#         digit = None
#         while digit == None:
#             digit = kp.getKey()
#         # Print result
#         print(digit)
#         demo(args.cascaded, args.block_orientation, args.rotate,digit)
#         digit = None
#         time.sleep(0.5)

#     # try:
#     #     demo(args.cascaded, args.block_orientation, args.rotate)
#     # except KeyboardInterrupt:
#     #     pass





from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
import time
from gpiozero import Button
import RPi.GPIO as GPIO
from keypad import keypad
import mysql.connector

mydb = mysql.connector.connect(
  host='127.0.0.1',
  database='bigsleep',
  user='root'
)

GPIO.setwarnings(False)

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=-90)
from luma.core.legacy import text
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT
kp = keypad(columnCount = 4)

from threading import Timer

button14 = Button(14) # user 1
button18 = Button(18) # user 2

button15 = Button(15) # stress
button24 = Button(24) # fatigue
button23 = Button(23) # vigilance
button25 = Button(25) # reveil

my_string=''
my_insertion=dict()


def button14Hello():
        my_insertion["user_id"]=1
def button18Hello():
        my_insertion["user_id"]=2
def button15Hello():
        my_insertion["etat"]='stress'
def button24Hello():
        my_insertion["etat"]='fatigue'
def button23Hello():
        my_insertion["etat"]='vigilance'
def button25Hello():
        my_insertion["etat"]='reveil'

def se_reveiller():
    show_message(device, "Tu doit se reveiller", fill="white", font=proportional(LCD_FONT), scroll_delay=0.05)

while 1:
    button14.when_released=button14Hello
    button15.when_released=button15Hello
    button18.when_released=button18Hello
    button24.when_released=button24Hello
    button23.when_released=button23Hello
    button25.when_released=button25Hello
    digit = None
    while digit == None:
        digit = kp.getKey()
        time.sleep(0.2)
    # Print result
    print(digit)
    if str(digit)!='C':
        my_string+=str(digit)
        if len(my_string)==5:
            my_string=my_string[1:]
        with canvas(device) as draw:
            text(draw, (0, 0), my_string, fill="white", font=None)
            time.sleep(0.7)
    if my_string!= '' and str(digit)=='C':
        print(my_string)
        my_insertion["note"]=int(my_string)
        if my_insertion["etat"]=='reveil':
            timer = Timer(my_insertion["note"]*60, se_reveiller)
            timer.start()
        print(my_insertion)
        mycursor = mydb.cursor()
        sql = f"INSERT INTO {my_insertion['etat']} (note, user_id) VALUES (%s, %s)"
        val = (my_insertion["note"],my_insertion["user_id"])
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        my_string=''
        text(draw, (0, 0), my_string, fill="white", font=None)
    digit = None

 

 
# from gpiozero import Button

# button14 = Button(14)
# button15 = Button(15)
# button18 = Button(18)

# def button14Hello():
#         print("Button14")
# def button15Hello():
#         print("Button15")
# def button18Hello():
#         print("Button18")


# while True:
#         button14.when_released=button14Hello
#         button15.when_released=button15Hello
#         button18.when_released=button18Hello

