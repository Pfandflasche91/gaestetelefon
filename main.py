import os
import time
import sys
import RPi.GPIO as GPIO
from collections import deque
import subprocess

# === Konfiguration ===
start_sound = "welcomeMessage.mp3"
record_file = "aufnahme.wav"
record_seconds = 5
mic_device = "plughw:2,0"  # ggf. anpassen nach "arecord -l"
GPIO.setmode(GPIO.BCM)
#define gpios
gpio_receiver_vcc = 23
gpio_receiver_sig = 24
#setup gpios
GPIO.setwarnings(False)
GPIO.setup(gpio_receiver_vcc , GPIO.OUT)
GPIO.setup(gpio_receiver_sig, GPIO.IN, pull_up_down= GPIO.PUD_DOWN)
#set vcc high
GPIO.output(gpio_receiver_vcc, GPIO.HIGH)
#ringbuffer
STABIL_COUNT =  50
BUFFER_SIZE = 100
buffer_receiver = deque([0]*BUFFER_SIZE, maxlen=BUFFER_SIZE)
last_stable_value = 1
#setting playback up
sound_file = "/home/max/git/gaestetelefon/welcomeMessage.wav"

try:
    while True:
        gpio_receiver_value =  GPIO.input(gpio_receiver_sig)
        buffer_receiver.append(gpio_receiver_value)
        last_values = list(buffer_receiver)[-STABIL_COUNT:]
        if all(v == last_values[0] for v in last_values):
            if(last_values[0] != last_stable_value):
                if last_values[0] == 1:
                    print("hung up",flush=True) 
                    try :
                        process.terminate()
                    except:
                        pass
                else:
                    print("not hung up",flush=True)
                    time.sleep(2)
                    process =  subprocess.Popen(["aplay", sound_file])
                last_stable_value = last_values[0]
except KeyboardInterrupt:
    print("\n End Program...")
finally:
    GPIO.cleanup()


