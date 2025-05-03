import RPi.GPIO as GPIO
import time
import sys
from collections import deque

GPIO.cleanup()
# Pin-Nummern im BCM-Modus verwenden
GPIO.setmode(GPIO.BCM)
# GPIOs festlegen
gpio_end_vcc = 27    # yellow wire
gpio_end_sig = 17    # brown wire
gpio_num_vcc = 4     # orange wire
gpio_num_sig = 18     # red wire
# Setup
GPIO.setup(gpio_end_vcc, GPIO.OUT)
GPIO.setup(gpio_num_vcc, GPIO.OUT)
GPIO.setup(gpio_end_sig, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(gpio_num_sig, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Ausgang auf HIGH setzen
GPIO.output(gpio_end_vcc, GPIO.HIGH)
GPIO.output(gpio_num_vcc, GPIO.HIGH)
# ringpuffer
STABIL_COUNT = 5
BUFFER_SIZE = 10
buffer = deque([0]*BUFFER_SIZE, maxlen=BUFFER_SIZE)
end_buffer = deque([0]* BUFFER_SIZE, maxlen=BUFFER_SIZE)
last_stable_value = 0
end_last_stable_value = 0
flanken_count = 0
end_flanken_count = 0

try:
    while True:
        value = GPIO.input(gpio_num_sig)
        end_value = GPIO.input(gpio_end_sig)
        buffer.append(value)
        end_buffer.append(end_value)
        last_values = list(buffer)[-STABIL_COUNT:]
        end_last_values = list(end_buffer)[-STABIL_COUNT:]
        if all(v == last_values[0] for v in last_values):
            if last_values[0] != last_stable_value:
                flanken_count += 1
               # print(f"Flankenwechsel erkannt! Neu: {last_values[0]} → Gesamt: {flanken_count}")
                last_stable_value= last_values[0]
        if all(b == end_last_values[0] for b in end_last_values):
            if end_last_values[0] != end_last_stable_value:
               # print("End Flanke")
               # print(end_last_values[0])
                if end_last_values[0] == 1:
                    flanken_count = 0
                else:
                    number = flanken_count /2
                    if number > 9:
                        number = 0
                    print(f"Number : {number}")
                end_last_stable_value= end_last_values[0]

       
# print(f"\rNumber :{num_value}", end="\n")
       # print(f"Endstop :{end_value}")
       # sys.stdout.write("\033[2A")
except KeyboardInterrupt:
    print("\nBeende Programm...")

finally:
    GPIO.cleanup()

