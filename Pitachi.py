#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

#SETTINGS
settings = {
	'RS' : 21,					#pin RS
	'E' : 20,					#pin E
	'D' : [18, 23, 24, 25, 8, 7 ,12, 16],	 	#pins D7 - D0
	
	'display_width' : 16,
	
	'increment' : 0x02, 'decrement' : 0, 'cursor_shift_on' : 0x01, 'cursor_shift_off': 0, 
	
	'display_on' : 0x04, 'display_off' : 0, 'cursor_on' : 0x02, 'cursor_off': 0, 'cursor_blink_on' : 0x01, 'cursor_blink_off' : 0,

	'display_shift_on' : 0x04, 'display_shift_off' : 0, 'cursor_right' : 0x04, 'cursor_left' : 0,

	'8bit' : 0x10, '4bit' : 0, 'two_lines' : 0x08, 'one_line': 0, 'font_5x10': 0x04, 'font_5x7': 0,
	
	'command' : False, 'data' : True,		
	
	'delay' : 0.0015,	
	
	'clear' : 0x01, 'home': 0x02, 'cursor_move_direction' : 0x04, 'enable_display_cursor' : 0x08, 
	'move_cursor_shift_display' : 0x10, 'set_interface_length' : 0x20, 'set_CGRAM_address': 0x40, 'set_DDRAM_address': 0x80,
	
	'second_line' : 0x40,
	
	'custom_character0': 0x00, 'custom_character1': 0x01, 'custom_character2': 0x02, 'custom_character3': 0x03, 
	'custom_character4': 0x04, 'custom_character5': 0x05, 'custom_character6': 0x06, 'custom_character7': 0x07
}
#EXAMPLE CUSTOM CHARACTER
example_custom_character = [
	0b00000,
	0b01010,
	0b01010,
	0b01010,
	0b00000,
	0b10001,
	0b01110,
	0b00000
]

#LCD
class LCD:
	mode = 0
	lines = 0
	font = 0

	def __init__(self, mode = settings['4bit'], lines = settings['two_lines'], font = settings['font_5x7']):
		self.mode = mode
		self.lines = lines
		self.font = font
		self.start()
	
	def start(self):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(settings['RS'], GPIO.OUT)
		GPIO.setup(settings['E'], GPIO.OUT)
		if self.mode == settings['8bit']:
			for i in range(8):
				GPIO.setup(settings['D'][i], GPIO.OUT)
			self.init_lcd()
		elif self.mode == settings['4bit']:
			for i in range(4):
				GPIO.setup(settings['D'][i], GPIO.OUT)
			self.init_lcd()
		else:
			print("Unknown mode")

	def init_lcd(self):
		time.sleep(0.02)
		#if self.mode == settings['8bit']:
		self.cmd(0x30, settings['command'])		#1
		time.sleep(0.005)
		self.cmd(0x30, settings['command'])		#2
		time.sleep(0.000160)
		self.cmd(0x30, settings['command'])		#3
		time.sleep(0.000160)
		if self.mode == settings['4bit']:
			self.cmd(0x02, settings['command'])
		self.set_interface_length(self.mode, self.lines, self.font)
		self.enable_display_cursor(settings['display_off'], settings['cursor_off'], settings['cursor_blink_off'])
		self.clear()
		self.move_cursor_shift_display(settings['display_shift_off'], settings['cursor_right'])
		self.cursor_move_direction(settings['increment'], settings['cursor_shift_off'])
		self.enable_display_cursor(settings['display_on'], settings['cursor_off'], settings['cursor_blink_off'])
		self.add_custom_character(example_custom_character, settings['custom_character0'])
		self.cursor_home()	
		
	def write(self, text, center = False):
		if center == True:
			text = self.center(text)
		for char in text:
			if char == '\n':
				self.go_to_second_line()
			else:
				self.cmd(ord(char), settings['data'])
	
	def center(self, text):
		length = len(text)
		if text[length - 1] == '\n':
			length = length - 1
		if length < settings['display_width']:
			x = (settings['display_width'] - length) / 2
			text = (" " * int(x)) + text
		return text
	
	def go_to_second_line(self):
		self.set_DDRAM_address(settings['second_line'])

	def clear(self):
		self.cmd(settings['clear'], settings['command'])

	def cursor_home(self):
		self.cmd(settings['home'], settings['command'])					
	
	def cursor_move_direction(self, increment_decrement, cursor_shift_on_off):
		bits = settings['cursor_move_direction']
		bits = bits | increment_decrement
		bits = bits | cursor_shift_on_off
		self.cmd(bits, settings['command'])

	def enable_display_cursor(self, display_on_off, cursor_on_off, cursor_blink_on_off):
		bits = settings['enable_display_cursor']
		bits = bits | display_on_off
		bits = bits | cursor_on_off	
		bits = bits | cursor_blink_on_off
		self.cmd(bits, settings['command'])
	
	def move_cursor_shift_display(self, display_shift_on_off, cursor_left_right):
		bits = settings['move_cursor_shift_display']
		bits = bits | display_shift_on_off
		bits = bits | cursor_left_right
		self.cmd(bits, settings['command'])
	
	def set_interface_length(self, data_interface_8bit_4bit, one_two_line_display, character_font): 
		bits = settings['set_interface_length']
		bits = bits | data_interface_8bit_4bit
		bits = bits | one_two_line_display
		bits = bits | character_font
		self.cmd(bits, settings['command'])	
	
	def set_CGRAM_address(self, address):
	        bits = settings['set_CGRAM_address']
	        bits = bits | address
	        self.cmd(bits, settings['command'])

	def add_custom_character(self, character, address):
		self.set_CGRAM_address(address)
		for i in range(8):
			self.cmd(character[i], settings['data'])
	
	def print_custom_character(self, address):
		self.cmd(address, settings['data'])
	
	def set_DDRAM_address(self, address):
		bits = settings['set_DDRAM_address']
		bits = bits | address
		self.cmd(bits, settings['command'])
	
	def cmd(self, bits, state):
		bits = bin(bits)[2:].zfill(8)
		GPIO.output(settings['RS'], state)
		if self.mode == settings['8bit']:
			for i in range(8):
				GPIO.output(settings['D'][i], False)
			for i in range(8):
				if bits[i] == "1":
					GPIO.output(settings['D'][i], True)	
			GPIO.output(settings['E'], True)
			time.sleep(settings['delay'])
			GPIO.output(settings['E'], False)
		if self.mode == settings['4bit']:
			for i in range(4):
				GPIO.output(settings['D'][i], False)
			for i in range(4):
				if bits[i] == "1":
					GPIO.output(settings['D'][i], True)
			GPIO.output(settings['E'], True)
			time.sleep(settings['delay'])
			GPIO.output(settings['E'], False)
			for i in range(4):
				GPIO.output(settings['D'][i], False)
			for i in range(4, 8):
				if bits[i] == "1":
					GPIO.output(settings['D'][i-4], True)
			GPIO.output(settings['E'], True)
			time.sleep(settings['delay'])
			GPIO.output(settings['E'], False)
