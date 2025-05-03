import lgpio
import time

IN_PIN = 18   # Eingang
OUT_PIN = 4   # Ausgang (Pin 7)
CHIP = 0

flank_count = 0

def on_edge(gpio, level, tick):
    global flank_count
    flank_count += 1
    print(f"Flanke erkannt! Gesamt: {flank_count}")

# GPIO-Chip öffnen
h = lgpio.gpiochip_open(CHIP)

# Eingang konfigurieren (ohne Pull-Down, extern sicherstellen!)
lgpio.gpio_claim_input(h, IN_PIN)
lgpio.gpio_set_alert_func(h, IN_PIN, on_edge)

# Ausgang konfigurieren und auf HIGH setzen
lgpio.gpio_claim_output(h, OUT_PIN)
lgpio.gpio_write(h, OUT_PIN, 1)
print(f"GPIO {OUT_PIN} auf HIGH gesetzt.")

try:
    print("Zähle Flanken... Drücke Strg+C zum Stoppen.")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Programm beendet.")

finally:
    lgpio.gpiochip_close(h)
    print("GPIOs freigegeben.")
