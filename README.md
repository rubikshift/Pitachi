# Pitachi
Easy to use Hitachi HD44780 python module for Raspberry Pi

Pitachi provides a class to controll LCD (Hitachi HD44780 controller) with Raspberry Pi.
Pitachi uses raspberry-gpio-python module: https://sourceforge.net/p/raspberry-gpio-python/

Remember to change default pins in 'settings' python dictionary.
As a deafault interface Pitachi use 4bit interface, but you can change it whenever you want.

Pitachi allows you to use almost all Hitachi HD44780 comands. Just type function and choose arguments from 'settings' dictionary.

To use Pitachi you need to have installed raspberry-gpio-python module, then you have to import Pitachi to your script.
