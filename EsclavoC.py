from machine import UART
from machine import Pin
from neopixel import Neopixel
import utime

#separator for the text file
#separator = " "

#define values for uart communication
uart= UART(1,9600)
uart.init(9600, bits=8, parity=0, stop=1)  
num_decimals = 1000 #every 0 is a decimal
delay = 1 #one second
header = b'C'

#received decimals
num_decimales = 1000 #cada 0 es un decimal

#value for Strip rgb
strip = Neopixel(4, 0, 15, "GRB")#num_leds, state_machine, pinGPIO, mode="RGB"\
strip.brightness(40)#overall brightness (0-255)

def readDate(): 
    if uart.any() > 0 :#if there are elements in the buffer
        received = uart.read(2)#read two bytes
            
    num_16bits = int.from_bytes(received, 'big') #conversion to 16-bit integer
    num_16bits = num_16bits # Calculate the decimals that were previously removed
    return num_16bits

def rescale(signal, in_min, in_max, out_min, out_max):
        if(signal <  in_min):
            return out_min
        if(signal >  in_max):
            return out_max
        return int((signal - in_min)*(out_max - out_min)/(in_max - in_min) + out_min)
    
def read():
    if uart.any() > 0:#validation
        if uart.read(1) == header:#if the information is correct
            utime.sleep(0.5)
            return readDate()
    return False

def show():
    value = read()
    while value == False:
        value = read()
    #here is the loaded value
    value = rescale(value,0,40,0,255)
    strip.fill((value,0,0))
    strip.show()

def main():
    
    while True:
        try:
            show()
        except Exception as e:
            print("Error:", e)
    
if __name__ == '__main__':
    main()
    