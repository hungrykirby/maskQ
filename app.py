import serial
import re
import threading
import sys

#import arrange
import config

import words
import face

MODE = input("test or train > ")
is_new = input("renew or make new file > ")
face_or_words = input("face or words > ")

def serial_loop():
    with serial.Serial('COM3', 9600, timeout=0.1) as ser:
        if face_or_words == "face":
            arranged_data = face.Face(MODE, 3)
        elif face_or_words == "words":
            arranged_data = words.Words(MODE, 3)
        arranged_data.make_dir_train_or_test(is_new) #フォルダを作成する
        try:
            while True:
                s = ser.readline()
                m = None
                try:
                    de = s.decode('utf-8')
                    m = re.match("\-*[\w]+", str(de))
                except Exception as e:
                    pass
                if(m != None):
                    config.is_calibration, make_serial_flush = arranged_data.fetch_numbers(m.group())
                    if make_serial_flush:
                        ser.flushInput()
                else:
                    pass
                    #print(type(m))
        except:
             print("Unexpected error:", sys.exc_info()[0])
             raise
        ser.close()

ser_loop = threading.Thread(target=serial_loop,name="ser_loop",args=())
ser_loop.setDaemon(True)
ser_loop.start()

def main():
    while True:
        console_input = input()
        if console_input == "s":
            config.is_input_word = True
        elif console_input == "e":
            config.is_input_word = False
            config.finish_input_word = True
        elif console_input == "o":
            config.is_calibration = True
        elif console_input != config.console_input_number:
            config.console_input_number = console_input
            print("c =", config.console_input_number)
        else:
            print("else")

if __name__ == "__main__":
    main()
