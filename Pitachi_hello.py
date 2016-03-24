#!/usr/bin/env python3
import lcd
import time

display = lcd.LCD(lcd.settings['8bit'])
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