# RpiZeroW-keyboard-emulator-for-a-serial-connected-measuring-device
Using a Wilnos NDT LCD 301 densitometer and R-Pi zero W as keyboard emulator to type measured into a text editor data after a button press.
Keypad keycode dictionary (0*07) scan code dictionary for numbers and decimal operand.
required aditional modules 
-RPI.GPIO 
-serial
-Rpi_I2C_driver 
-time 
-isticktoit or equivalent to enable libcomposites kernel module.

Code has been commented as best as i can. An Engineer by training and passion so excuse any 'layman' expressions therein.
The second branch is a little bit more complex. It is the initial code adapted for a Keithley 6485 picoamperemeter to measure optical density.
