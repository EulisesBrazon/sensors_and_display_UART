from machine import UART
from ST7735 import TFT
from machine import SPI,Pin,ADC
from sysfont import sysfont
import utime
import math



#separator for the text file
separator = " "

#define values for uart communication
uart= UART(1,9600)
uart.init(9600, bits=8, parity=0, stop=1)  
num_decimals = 1000 #every 0 is a decimal
delay = 1 #one second
header = b'A'

#difien values for displey use
spi = SPI(0, baudrate=20000000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
tft=TFT(spi,0,7,1)
tft.initr()
tft.rgb(True)

#received decimals
num_decimales = 1000 #cada 0 es un decimal

def seeDate(temperature, light, potentiometer, distance):
    
    temperature = str(temperature)
    light = str(light)
    potentiometer = str(potentiometer)
    distance = str(distance)
    
    size=2
    separation = 4
    h=0
    
    tft.fill(TFT.BLACK)#clean screen
    
    tft.text((0, h), "Temperatura:", TFT.RED, sysfont, size, nowrap=True)
    
    h += sysfont["Height"]*size+separation
    tft.text((0, h), temperature+"C", TFT.BLUE, sysfont, size, nowrap=True)
    
    h += sysfont["Height"]*size+separation
    tft.text((0, h), "Nivel Luz:", TFT.RED, sysfont, size, nowrap=True)
    
    h += sysfont["Height"]*size+separation
    tft.text((0, h), light, TFT.BLUE, sysfont, size, nowrap=True)
    
    h += sysfont["Height"]*size+separation
    tft.text((0, h), "Potenciometo:", TFT.RED, sysfont, size-1, nowrap=True)
    
    h += sysfont["Height"]*size+separation
    tft.text((0, h), potentiometer, TFT.BLUE, sysfont, size, nowrap=True)
    
    h += sysfont["Height"]*size+separation
    tft.text((0, h), "Distancia:", TFT.RED, sysfont, size, nowrap=True)
    
    h += sysfont["Height"]*size+separation
    tft.text((0, h), distance +"cm", TFT.BLUE, sysfont, size, nowrap=True)
    
def readDate(): 
    if uart.any() > 0 :#if there are elements in the buffer
        received = uart.read(2)#read two bytes
            
    num_16bits = int.from_bytes(received, 'big') #conversion to 16-bit integer
    num_16bits = num_16bits # Calculate the decimals that were previously removed
    return num_16bits

def saveFile(temperature, light, potentiometer, distance):
    file = open("Info.txt", "a")
    file.write(str(temperature)+separator+str(light)+separator+str(potentiometer)+separator+str(distance)+"\n")
    file.close()
    
def readAndShow():
    if uart.any() > 0:
        if uart.read(1) == header:
            utime.sleep(0.5)
            temperature = readDate()/num_decimals
            light = readDate()
            potentiometer = readDate()
            distance = readDate()/num_decimals
            saveFile(temperature, light, potentiometer, distance)
            seeDate(temperature, light, potentiometer, distance)
               
def main():
    tft.fill(TFT.BLACK)
    tft.text((0, 50), "Sincronizando...", TFT.GREEN, sysfont, 1, nowrap=True)
    
    while True:
        try:
            readAndShow()
            
        except Exception as e:
            print("Error:", e)
        #utime.sleep(1)
    
        
if __name__ == '__main__':
    main()




