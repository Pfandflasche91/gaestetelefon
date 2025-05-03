import pygame
import os
import time
import sys
import RPi.GPIO as GPIO
from collections import deque

time.sleep(5)
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
last_stable_value = 0
#setting playback up
#pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
#pygame.mixer.init()
#pygame.mixer.music.load(start_sound)
try:
    while True:
        gpio_receiver_value =  GPIO.input(gpio_receiver_sig)
        buffer_receiver.append(gpio_receiver_value)
        last_values = list(buffer_receiver)[-STABIL_COUNT:]
        if all(v == last_values[0] for v in last_values):
            if(last_values[0] != last_stable_value):
                 print("leck mich")
                 last_stable_value = 123456 #last_values[0]
                 time.sleep(5)
                # if last_values[0] == 1:                      print("hung up")
                # else:
                 #    print("not hung up")
                  #   time.sleep(2)
                     #pygame.mixer.music.play()
                   #  print("Playing start sound...")
                     #while pygame.mixer.music.get_busy():
                     #    time.sleep(0.1)
                     # print(f"Recording for {record_seconds} seconds...")
                     # record_cmd = f"arecord -D {mic_device} -f cd -t wav -d {record_seconds} -r 44100 {record_file}"
                     # os.system(record_cmd)
                    # print("Playing recorde audio...")
                    # os.system(f"aplay {record_file}")
                 # last_stable_value = last_values[0]
except KeyboardInterrupt:
    print("\n End Program...")
finally:
    GPIO.cleanup()



# === Schritt 1: Startsound abspielen ===
#pygame.mixer.init()
#pygame.mixer.music.load(start_sound)
#pygame.mixer.music.play()
#print("Playing start sound...")
#while pygame.mixer.music.get_busy():
    time.sleep(0.1)

# === Schritt 2: Aufnahme starten ===
#print(f"Recording for {record_seconds} seconds...")

#record_cmd = f"arecord -D {mic_device} -f cd -t wav -d {record_seconds} -r 44100 {record_file}"
#os.system(record_cmd)

# === Schritt 3: Aufnahme abspielen ===
#print("Playing recorded audio...")
#os.system(f"aplay {record_file}")

