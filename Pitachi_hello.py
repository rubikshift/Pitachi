#!/usr/bin/env python3
import Pitachi as lcd
import time

RS = 21
E = 20
D = [25, 24, 23, 18]

display = lcd.LCD(RS, E, D)
display.write('Hello! ')
display.print_custom_character(lcd.settings['custom_character0'])
time.sleep(10)
display.clear()
while True:
	display.write(time.strftime("%H:%M"), True)
	display.go_to_second_line()
	display.write(time.strftime("%d %b %Y"), True)
	time.sleep(10)
	display.clear()
