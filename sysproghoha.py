from flask import Flask,render_template
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)

GPIO.cleanup()

#sensor infra red
GPIO.setup(17, GPIO.IN)

#buat motor

app=Flask(__name__)
	
pins = {
		20 : {'name' : 'GPIO 20', 'state' : 0},
		21 : {'name' : 'GPIO 21', 'state' : 0}
		#######_________________CAN ADD MORE GPIO HERE___________________#########
		}
#setup

def cleanup():
	for pin in pins:
		GPIO.output(pin, 0)
	
@app.route('/')
def index():
		templateData = {
			# 'data' : status
		}
		return render_template('index.html', **templateData)	


if(__name__=='__main__'):
	app.run(debug=True,host='0.0.0.0')

	try:
		while True:
			sleep(0.5)
	except KeyboardInterrupt as e:
		GPIO.cleanup()

for pin in pins:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, 0)
	
buka = False
status = "belum dibuka"
countdown = 5
while True:
	sensor = GPIO.input(17)
	if sensor == 0 and not buka:
		#pintu buka
		print("tunggu buka pintu")
		sleep(2)
		print("ganjel pintu")
		GPIO.output(20, 1)
		GPIO.output(21, 0)
		buka = True
		countdown = 5
		sleep(1)
		cleanup()
		
	elif sensor == 1 and buka and countdown == 0:
		#pintu tutup
		print("pintu tutup")
		GPIO.output(20, 0)
		GPIO.output(21, 1)
		buka = False
		countdown = 5
		sleep(1)
		cleanup()
	
	elif sensor == 1 and buka:
		print("gaada orang")
		countdown-=1
		sleep(1)
	
	elif sensor == 0 and buka:
		print("ada orang")
		countdown=5
		sleep(1)

		