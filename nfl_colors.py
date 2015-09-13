from __future__ import division  #http://stackoverflow.com/questions/1267869/how-can-i-force-division-to-be-floating-point-in-python
import time
import math
import boto
import pprint

from neopixel import *


# LED strip configuration:
LED_COUNT      = 30      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

def flashColors(colors, wait_ms=500, flash_count=3):
	for flash in range(flash_count):
		for i in range(strip.numPixels()):
			strip.setPixelColorRGB(i, 0, 0, 0);
		strip.show()
		time.sleep(wait_ms/1000.0)
		
		for i in range(strip.numPixels()):
			pos = i % len(colors)
			strip.setPixelColorRGB(i, colors[pos][0], colors[pos][1], colors[pos][2])
		strip.show()
		time.sleep(wait_ms/1000.0)

def showColors(colors, wait_ms=50):
	for i in range(strip.numPixels()):
		pos = i % len(colors)
		strip.setPixelColorRGB(i, colors[pos][0], colors[pos][1], colors[pos][2])
		strip.show()
		time.sleep(wait_ms/1000.0)

# Main program logic follows:
if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
	strip.begin()

	print 'Press Ctrl-C to quit.'

	team_colors = {
          'cardinals' : [[155,39,67],[0,0,0]],
          'seahawks': [[0,21,50],[105,190,40],[155,161,162]],
          'cardinals' : [[155,39,67],[0,0,0],[255,255,255]],
          'falcons' : [[189,13,24],[0,0,0]],
          'ravens' : [[40,3,83],[0,0,0],[208,178,64]],
          'buffalo bills' : [[0,51,141],[198,12,48]],
          'panthers' : [[0,136,206],[0,0,0],[165,172,175]],
          'bears' : [[3,32,47],[221,72,20]],
          'bengals' : [[251,79,20],[0,0,0]],
          'browns' : [[38,32,30],[254,60,0]],
          'cowboys' : [[13,37,76],[197,206,214],[255,255,255]],
          'broncos' : [[251,79,20],[0,34,68]],
          'lions' : [[0,109,176],[197,199,207],[0,0,0],[255,255,255]],
          'packers' : [[32,55,49],[255,182,18]],
          'texans' : [[2,37,58],[179,27,52]],
          'colts' : [[0,59,123],[255,255,255]],
          'jaguars' : [[0,0,0],[159,121,44],[215,162,42],[0,101,118],[255,255,255]],
          'chiefs' : [[178,0,50],[242,200,0]],
          'dolphins' : [[0,141,151],[245,129,31]],
          'vikings' : [[59,1,96],[240,191,0]],
          'patriots' : [[13,37,76],[200,8,21],[214,214,214],[255,255,255]],
          'saints' : [[210,184,135],[0,0,0]],
          'giants' : [[25,47,10],[202,0,26],[162,170,173],[255,255,255]],
          'jets' : [[12,55,29],[255,255,255]],
          'raiders' : [[0,0,0],[196,200,203]],
          'eagles' : [[0,59,72],[0,0,0],[112,128,144],[192,192,192]],
          'steelers' : [[255,182,18],[0,0,0],[255,255,255]],
          'chargers' : [[12,35,64],[255,184,28],[0,114,206]],
          'buccaneers' : [[214,10,11],[0,0,0],[137,118,95]],
          'titans' : [[100,143,204],[13,37,76]],
          'redskins' : [[119,49,65],[255,182,18],[255,255,255]],
          'clear': [[0,0,0]],
          'forty niners': [[175,30,44],[230,190,138]]
	};

	sqs = boto.connect_sqs(profile_name="default")
	queue = boto.sqs.queue.Queue(sqs, "https://sqs.us-east-1.amazonaws.com/612895797421/neopixel")
	
	while True:
		messages = queue.get_messages(num_messages=1, wait_time_seconds=10)
		for m in messages:
			team = m.get_body().lower()
			print "We got a message: " + team
			if team in team_colors:
				showColors(team_colors[team])
				flashColors(team_colors[team])
			queue.delete_message(m)



