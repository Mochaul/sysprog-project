from flask import Flask,render_template
from time import sleep
# import threading
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)

GPIO.cleanup()

#sensor infra red
GPIO.setup(17, GPIO.IN)

pins = {
		20 : {'name' : 'GPIO 20', 'state' : 0},
		21 : {'name' : 'GPIO 21', 'state' : 0}
		#######_________________CAN ADD MORE GPIO HERE___________________#########
		}

for pin in pins:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, 0)	

app=Flask(__name__)

def cleanup():
	for pin in pins:
		GPIO.output(pin, 0)

@app.after_request
def mainProgram(response):
	timeout = 10
	buka = False
	# status = "Belum Dibuka"
	countdown = 5
	while True:
		sensor = GPIO.input(17)
		if sensor == 0 and not buka:
			#pintu buka
			print("Menunggu buka pintu")
			sleep(2)
			print("Ganjal pintu")
			GPIO.output(20, 1)
			GPIO.output(21, 0)
			buka = True
			countdown = 5
			sleep(1)
			timeout = 10
			cleanup()
			
		elif sensor == 1 and buka and countdown == 0:
			#pintu tutup
			print("Pintu tertutup")
			GPIO.output(20, 0)
			GPIO.output(21, 1)
			buka = False
			countdown = 5
			sleep(1)
			timeout = 10
			cleanup()
		
		elif sensor == 1 and buka:
			print("Tidak ada orang")
			countdown-=1
			sleep(1)
			timeout = 10
		
		elif sensor == 0 and buka:
			print("Ada orang")
			countdown=5
			sleep(1)
			timeout = 10

		elif sensor == 1 and not buka:
			timeout -= 1
			if timeout == 0:
				return response

@app.route('/')
def index():
		templateData = {
			# pins
		}
		return render_template('index.html', **templateData)

@app.route("/<action>")
def action(action): 
	if action == "open":
		GPIO.output(20, 1)
		GPIO.output(21, 0)
		sleep(1)
		cleanup()

	elif action == "close":
		GPIO.output(20, 0)
		GPIO.output(21, 1)
		sleep(1)
		cleanup()

	templateData = {
              'pins'    : pins,
								}
	return render_template('index.html', **templateData)	

if(__name__=='__main__'):
	app.run(debug=True,host='0.0.0.0')

	# try:
	# 	while True:
	# 		sleep(0.5)
	# except KeyboardInterrupt as e:
	# 	GPIO.cleanup()