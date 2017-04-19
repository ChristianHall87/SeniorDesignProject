
import serial
import string
import time
import picamera

ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=3.0)

OK='OK'
#Switch the pound sign to send to phonenumber
#Phonenumber='7014037106'
Phonenumber='3208284142'
#Phonenumber='2188413509'

global IncomingText
global gpsText
global voltRead
global battdata

a='a'
b='b'
c='c'
d='d'
p='p'
n='n'
g='g'
i='i'

TextRecieved=0

def FONA_Respond():

		ser.write(b'\r')
		ser.write(b'\r')
		ser.write(b'AT\r')
		time.sleep(.01)
		rcv = ser.readline()
		rcv2 = ser.read(2)
		rcv3 = ser.readline()

if rcv2==OK:
	Response=1

else:

	ser.write(b'\r')
	ser.write(b'\r')
	ser.write(b'AT\r')
	rcv = ser.readline()
	rcv2 = ser.read(2)
	rcv3 = ser.readline()

	if rcv2==OK:
		Response=1

		print('FONA Responded. 2nd try')

	else:
		ser.write(b'\r')
		ser.write(b'\r')
		ser.write(b'AT\r')
		rcv = ser.readline()
		rcv2 = ser.read(2)
		rcv3 = ser.readline()

	if rcv2==OK:
		Response=1
		print('Woke up FONA.')
		time.sleep(1)

	else:
		Response=0
		print('No Response.')
		time.sleep(1)
		return Response

def FONA_SENDTEXT(Command):

"""Send text to a programmed phone number, returns 'OK."""
if FONA_Respond()==1:

		ser.write(b'AT+CMGF=1\r')

		time.sleep(.1)

		#print("Text Mode")

		rcv = ser.readline()

		rcv2 = ser.read(2)

		rcv3 = ser.readline()

	if rcv2==OK:

		time.sleep(.1)
		#print("made it")
		ser.write(b'AT+CMGS="')
		time.sleep(.1)
		#print("composing")
		ser.write(Phonenumber)
		ser.write(b'"\r')
		time.sleep(.1)
		#print("number entered")
		rcv = ser.readline()
		rcv2 = ser.readline()
		ser.write(str(Command))
		ser.write(b'\x1a')
		time.sleep(.1)
		#print("ctrl z")
		rcv3 = ser.readline()
		rcv4 = ser.readline()
		rcv5 = ser.readline()
		rcv6 = ser.readline()
		rcv7 = ser.read(2)
		rcv8 = ser.readline()
		print('Sent.')

	else:

		print("NOT working")

return

def FONA_GPS():
global gpsText

	if FONA_Respond()==1:
		ser.write(b'AT+CGPSINFO\r')
		rcv = ser.readline()
		rcv3 = ser.read(10)
		NorthCoord = ser.read(11)
		rcv4 = ser.read(3)
		WestCoord = ser.read(12)
		rcv5=ser.read(25)
		knots = ser.read(3)
		rev6=ser.read(2)
		rc8 = ser.readline()
		gpsText = NorthCoord + " N\r" + WestCoord + " W\r" + knots + " knots"
		time.sleep(.1)

return gpsText

def FONA_INITIALIZE():

	if FONA_Respond() == 1:

		ser.write(b'AT+CGPS=1,1\r')
		#print('GPS Initialized.')
		FONA_GPS()
		#print(gpsText)
		print('Initialized.')

return

def TimedSnap():

"Take picture"

	with picamera.PiCamera() as camera:
		camera.resolution = (400, 400)
		camera.start_preview()
		time.sleep(1)
		camera.capture('/home/pi/image.jpg')
		camera.stop_preview()
return

def FONA_DELETETEXT():

"Delete all texts in FONA's storage"

time.sleep(1)

	if FONA_Respond()==1:
		ser.write(b'AT+CMGD=0,4\r')
		rcv = ser.readline()
		rcv2 = ser.read(2)
		rcv3 = ser.readline()
		print('Texts have been deleted.\r')

	else:
		print("NOT working")

return

def FONA_RECTEXT():

"Recieve next unread text"

global IncomingText

	if FONA_Respond()==1:
		ser.write(b'AT+CMGR=0\r')
		rcv = ser.readline()
		rcv2 = ser.read(21) ##read or unread
		rcv4 = ser.readline()
		IncomingText = ser.read(1) ##text from APP
		rcv6 = ser.readline()
		rcv7 = ser.readline()
		rcv8 = ser.readline()
		print("Received Text: " + IncomingText)
		time.sleep(.5)

return IncomingText

def FONA_NetworkConnect():

"Initialize network connection, returns a 1 if connection is made"

	if FONA_Respond()==1:
		ser.write(b'AT+CREG=2\r')
		ser.write(b'AT+CGDCONT=1,"IP","NXTGENPHONE","0.0.0.0",0,0\r')
		ser.write(b'AT+CGSOCKCONT=1,"IP","NXTGENPHONE","0.0.0.0",0,0\r')
		ser.write(b'AT+CIPMODE=1\r')
		ser.write(b'AT+CGATT=1\r')
		ser.write(b'AT+CGACT=1\r')
		time.sleep(4)
		ser.write(b'AT+NETOPEN\r')
		ser.write(b'AT+NETOPEN?\r')
		rcv = ser.readline()
		rcv2 = ser.readline()
		rcv3 = ser.readline()
		rcv4 = ser.readline()
		rcv5 = ser.readline()
		rcv6 = ser.readline()
		rcv7 = ser.readline()
		rcv8 = ser.read(11)
		rcv9 = ser.readline()
		print(rcv8)

	if rcv8=='+NETOPEN: 0':
		Response=1

	else:
		Response=0

return Response

def FONA_SENDPIC_MMS():

ser.flushInput()
ser.flushOutput()

"Send picture MMS to Phonenumber"

	if FONA_Respond()==1:

		#Set MMS protocols #CHANGE THE IMAGE TO SEND JPG ONLY
		ser.write(b'AT+CMMSCURL="mmsc.mobile.att.net"\r')
		time.sleep(2)
		ser.write(b'AT+CMMSPROTO=1,"172.26.39.1",80\r')
		time.sleep(2)
		#Put FONA in MMS edit mode
		ser.write(b'AT+CMMSEDIT=1\r')
		time.sleep(2)
		#Select Recipient
		RecipCommand = 'AT+CMMSRECP="' + Phonenumber +'"\r'
		ser.write(RecipCommand)
		time.sleep(1)
		#Download picture from PI
		#This breaks up the image into bytes.
		image_raw = []

	with open("/home/pi/image.jpg","rb") as p: 
		byte = p.read(1)

	while byte:
		#ser.write(byte)
		image_raw.append(byte)
		byte=p.read(1)
		#print(ord(byte))
		DownloadCommand = 'AT+CMMSDOWN="PIC",{},"image.jpg"\r'.format(len(image_raw))
		#print(DownloadCommand)
		ser.write(DownloadCommand)
		time.sleep(1)

	for byte in image_raw:
		ser.write(byte)
		time.sleep(0.0001) #.01

	if FONA_Respond()==1:
		print("Image Prepped.\r")
		print("Sending...")
		#Send Message
		ser.write(b'AT+CMMSSEND\r')
		time.sleep(25)
		print("Image Sent.\r")

return

FONA_INITIALIZE()
return

def FONA_CHECKBATTERY():

global battdata
ser.write(b'AT+CBC\r')
time.sleep(.5)
rcv = ser.readline()
rcv2 = ser.read(8)
batt = ser.read(2)
battdata = 'Battery: ' + batt + '%'
return battdata

def FONA_PhoneHome():

ser.write(b'ATD' + Phonenumber + ';\r')
time.sleep(1)
	while True:
		rcv = ser.readline()
		rcv2 = ser.read(1)
		rcv3 = ser.readline()
		rcv4 = ser.read(1)
		rcv5 = ser.readline()
		rcv6 = ser.read(1)
		rcv7 = ser.readline()
		rcv8 = ser.read(1)
		rcv9 = ser.readline()
		rcv10 = ser.read(1)

if rcv2 == 'N':
break
if rcv4 == 'N':
break
if rcv6 == 'N':
break
if rcv8 == 'N':
break
if rcv10 == 'N':
break

return

##initialize FONA-delete texts etc..

while True:
FONA_INITIALIZE()
ser.flushInput()
ser.flushOutput()

time.sleep(2)

FONA_DELETETEXT()

voltRead=8;

global battdata

while True:

	FONA_RECTEXT()

	if IncomingText == a:
		FONA_SENDTEXT('Connection Confirmed')
		FONA_DELETETEXT()
		voltRead = voltRead + 1

	elif IncomingText == g:
		print('Getting GPS coordinates...')
		FONA_GPS()
		print(gpsText)
		FONA_SENDTEXT(gpsText)
		FONA_DELETETEXT() #MAKE KNOTS WORK
		voltRead = voltRead + 1 #GET BATTERY ACTUALLY

	elif IncomingText == i:
		FONA_SENDTEXT("i")
		print("i")
		FONA_DELETETEXT()
		voltRead = voltRead + 1

	elif IncomingText == p:
		print("Attempting to Take Picture")
		TimedSnap()
		print('Attempting Picture Send')
		FONA_SENDPIC_MMS()

	break
		FONA_DELETETEXT()

	break

	elif IncomingText == n:
		print('Attempting Network Connect')
		FONA_NetworkConnect()
		FONA_SENDTEXT("Network Opened.")
		FONA_DELETETEXT()
		voltRead = voltRead + 1

	elif IncomingText == c:
		print('Attemping Call...')
		FONA_PhoneHome()
		print('Call complete')
		FONA_DELETETEXT()
		voltRead = voltRead + 1

	else:
		print('No texts to read.\r')

	if voltRead == 10:
		FONA_CHECKBATTERY()
		FONA_SENDTEXT(battdata)
		FONA_DELETETEXT()
		voltRead = 0