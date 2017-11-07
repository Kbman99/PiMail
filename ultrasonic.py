import RPi.GPIO as GPIO
import time

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 12
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

def start_measurement():
    try:
        dist_list = []
        for i in range(5):
            dist_list.append(distance())
        dist = sum(dist_list)/5
        for item in dist_list:
            print(item)
        print ("Average Measured Distance = {:1f} cm".format(dist))
        time.sleep(1)
        return dist
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
        return 0
