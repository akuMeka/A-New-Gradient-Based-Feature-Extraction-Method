from __future__ import print_function
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os
import RPi.GPIO as GPIO

# GPIO'LAR TANIMLANIYOR
redLed = 21
panPin = 27
tiltPin = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(redLed, GPIO.OUT)



# Video akışı başlatılıyor
print("Kameranın calışması bekleniyor...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

# nesnenin alt ve üst sınırları tanımlanıyor.
# HSV renk uzayında tanımlanacak
altsinir=  (47, 100, 100)
ustsinir = (68, 255, 255)

# Led kapalı iken basla
GPIO.output(redLed, GPIO.LOW)
ledOn = False

# Servoları 90-90 pozisyonda baslat Nötr konum.Global degıskenler programın her yerınden ulasmak için  tanımlanıyor.
global panServoAngle
panServoAngle = 90
global tiltServoAngle
tiltServoAngle = 90

# Konumlandırma servoları
print("\n Servoları başlangıç pozisyonuna getir ==>Programdan 'q' ile cik  \n")
# angleServoctrl dosyası cagırılıyor.
os.system("python servokontrol.py " + str(panPin) + " " + str(panServoAngle))
os.system("python3 servokontrol.py " + str(tiltPin) + " " + str(tiltServoAngle))


# nesneyi ekranın ortasına cekmek için servolar yerlestirildi.
def servoPosition(x, y):
    global panServoAngle
    global tiltServoAngle
    if (x < 220):
        panServoAngle += 10
        if panServoAngle > 140:
            panServoAngle = 140
        os.system("python servokontrol.py " + str(panPin) + " " + str(panServoAngle))

    if (x > 280):
        panServoAngle -= 10
        if panServoAngle < 40:
            panServoAngle = 40
        os.system("python servokontrol.py " + str(panPin) + " " + str(panServoAngle))

    if (y < 160):
        tiltServoAngle += 10
        if tiltServoAngle > 140:
            tiltServoAngle = 140
        os.system("python servokontrol.py " + str(tiltPin) + " " + str(tiltServoAngle))

    if (y > 210):
        tiltServoAngle -= 10
        if tiltServoAngle < 40:
            tiltServoAngle = 40
        os.system("python servokontrol.py " + str(tiltPin) + " " + str(tiltServoAngle))



while True:
    # bir sonraki kareyi video akısından al ve 180 derece cevir
    # hsv renk uzayına cevir
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    frame = imutils.rotate(frame, angle=180)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, altsinir, ustsinir)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)


    # (x, y) nesnenin merkezi
    #konturleri buluyoruz.
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    center = None

    #
    if len(cnts) > 0:
         #maskedeki en buyuk yeri bulmak ve minumum cevreleme merkezi ve agırlık merkezını hesaplama

        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # yarıcap minumum boyutta ise
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            servoPosition(int(x), int(y))
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

            # led açık değilse ledi açın
            if not ledOn:
                GPIO.output(redLed, GPIO.HIGH)
                ledOn = True

    # cisim tespit edilmez ise ledi kapatın
    elif ledOn:
        GPIO.output(redLed, GPIO.LOW)
        ledOn = False


    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


print("\n Programdan cik ve temizle\n")
GPIO.cleanup()
cv2.destroyAllWindows()
vs.stop()