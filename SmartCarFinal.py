import RPi.GPIO as GPIO
import time

GPIO_TRIGGER=3
GPIO_ECHO=5
#set GPIO Pins

def init():
	GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.setup(35,GPIO.OUT)
    GPIO.setup(36,GPIO.OUT)
    GPIO.setup(37,GPIO.OUT)
    GPIO.setup(38,GPIO.OUT)

def forward():
    GPIO.output(35,False)
    GPIO.output(36,True)
    GPIO.output(37,False)
    GPIO.output(38,True)

def speedControl():
    p=GPIO.PWM(36,50)
    q=GPIO.PWM(38,50)
    p.start(0)
    q.start(0)
    try:
		for i in range(50):
            p.ChangeDutyCycle(100-i)
            q.ChangeDutyCycle(100-i)
            time.sleep(0.02)
            if(i==49):
                dist2=distance()
                meter2=dist2/100.0
				print ("Measured Distance = %.1f m" %meter2)
                if(meter2>1 and meter2<2):
                    print "speed decresing"
                    speedControl()
                elif(meter2<1):
                    print "break"
                    speedBreak()
                else:
                    forward()
        except KeyboardIntrrupt:
            pass
        #p.stop()
        #q.stop()
def speedBreak():
	p=GPIO.PWM(36,50)
	q=GPIO.PWM(38,50)
	p.start(0)
	q.start(0)
	try:
        dist1=distance()
        meter1=dist1/100.0
		print ("Measured Distance = %.1f m" %meter1)
        if(meter1<1):
            print "break"
            p.ChangeDutyCycle(0)
            q.ChangeDutyCycle(0)
        elif(meter1>1 and meter1<2):
            print "speed decresing"
            speedControl()
        else:
            forward()
            time.sleep(0.02)
        except KeyboardInterrupt:
            pass

        #p.stop()
        #q.stop()

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



if __name__ == '__main__':
    init()
    while 1:
        try:
            dist=distance()
            meter=dist/100.0
            if(meter>3):
                print "go ahead"
                forward()
            elif(meter>1 and meter<2):
                print "speed decresing"
                speedControl()
            elif(meter<1):
                print "break"
                speedBreak()
            print ("Measured Distance = %.1f m" %meter)
            time.sleep(1)
        except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()
