#import modules we need to establish connections and set up our I/O devices
import RPi_I2C_driver
import serial
import RPi.GPIO as GPIO
from time import * #imports everything from the time class
GPIO.setwarnings(False)

#Set up serial port.
port=serial.Serial("/dev/ttyS0" , baudrate=9600 ,timeout = 10)
#write data to serial line     
port.write(b'r\r')

#Button connected to pin 40 as an input device
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#Beeper definition as output
GPIO.setup(26,GPIO.OUT)
#ON-bord LCD setup
mylcd=RPi_I2C_driver.lcd()
disp_string = ""
serial_string = ""
#start screen display 
mylcd.lcd_display_string("R-Pi0 Display On", 1)
mylcd.lcd_display_string("UweZ HID Interf.", 2)
sleep(2)
mylcd.lcd_clear()
#virtual keyboard write to file (on host computer open the intended excell sheet)
NULL_CHAR = chr(0)
def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())
#keycode dictionary
keycode_map={
    '0':(NULL_CHAR*2+chr(39)+NULL_CHAR*5),
    '1':(NULL_CHAR*2+chr(30)+NULL_CHAR*5),
    '2':(NULL_CHAR*2+chr(31)+NULL_CHAR*5),
    '3':(NULL_CHAR*2+chr(32)+NULL_CHAR*5),
    '4':(NULL_CHAR*2+chr(33)+NULL_CHAR*5),
    '5':(NULL_CHAR*2+chr(34)+NULL_CHAR*5),
    '6':(NULL_CHAR*2+chr(35)+NULL_CHAR*5),
    '7':(NULL_CHAR*2+chr(36)+NULL_CHAR*5),
    '8':(NULL_CHAR*2+chr(37)+NULL_CHAR*5),
    '9':(NULL_CHAR*2+chr(38)+NULL_CHAR*5),
    '.':(NULL_CHAR*2+chr(55)+NULL_CHAR*5),
    ',':(NULL_CHAR*2+chr(54)+NULL_CHAR*5)
    }
#Specific task readings.

#create an empty arrray and convert data to float points
#start a counter for the data stream control
OD=[]
cnt=0
#counter for values written to sheet
i=1
#an infinite loop        
while True:
    #run unless interupted by error. Comment out if you cant locate error.
    try:
	#query serial line     
	port.write(b'r\r')
        #read line from serial. Readline requires a timeout
        serialString = port.read_until(b'\r')
        serialString = serialString.decode('Ascii')

        #convert serial string to float data type
        newstr=serialString.replace(',','.')
        new=float(newstr)

        #opticalDensity=float(opticalDensity)
        OD.append(new)
        cnt+=1
        if cnt>6:
            OD.pop(0)
            #calculate simple weighted moving average and round the ans to 3 decimal places
            ODavg=round(((OD[1]*1/15)+(OD[2]*2/15)+(OD[3]*3/15)+(OD[4]*4/15)+(OD[5]*5/15)) , 3)
        
            #Set up the on board display
            disp_string = "OD value # %d" % (i)
            mylcd.lcd_display_string(disp_string, 1)
            mylcd.lcd_display_string(str(ODavg), 2)            
            #A loop that executes only when the button is pushed to record values
            if GPIO.input(40) == GPIO.LOW :
                #turn the beeper on
                GPIO.output(26 , GPIO.HIGH)
                sleep(0.02)
                #Beeper off
                GPIO.output(26 , GPIO.LOW)
                #print results in python shell
                print(i, ODavg)
                i += 1
                #prepare data for transfer
                ODavg_str=str(ODavg)

                #implementation of virtual keyboard (Dictionary)
                for element in ODavg_str:
                    #compare element in ODavg to keys in the dictionary and write
                    write_report(keycode_map[element])
                    #Release all keys      
                    write_report(NULL_CHAR*8)
                    #creates the view that data is actually being typed by depicting human typing
                    sleep(0.2)
                # Press RETURN/ENTER key to skip to next cell or line
                write_report(NULL_CHAR*2+chr(40)+NULL_CHAR*5)
                #Release all keys     
                write_report(NULL_CHAR*8)
    except:
        continue
#End program shut down screen
sleep(2)
mylcd.lcd_clear()
mylcd.backlight(0)