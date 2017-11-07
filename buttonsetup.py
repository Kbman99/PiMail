import RPi.GPIO as GPIO
import time
from gpiozero import Button
import ultrasonic

GPIO.setmode(GPIO.BCM)

GPIO_BUTTON = 16

GPIO.setup(GPIO_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

button = None
dist = None

def setup(button, dist):
    print("Setting up hardware...")
    button = Button(GPIO_BUTTON)
    print("Awaiting button press to initiate measurement")
    dist = measurement_loop(button)
    if dist is None or dist <= 0:
        print("Setup failed :(")
    else:
        print("Setup complete! Distance set to: {}".format(dist))


def measurement_loop(button):
    timeout = time.time() + 5
    while True:
        if button.is_pressed:
            dist = ultrasonic.start_measurement()
            return dist
        elif time.time() > timeout:
            return 0
        time.sleep(0.5)


if __name__ == "__main__":
    setup(button, dist)
