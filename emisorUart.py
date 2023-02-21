from machine import UART
from machine import Pin,ADC
import machine
import utime

#define values for uart communication
uart= UART(0,9600)
uart.init(9600, bits=8, parity=0, stop=1)  
num_decimals = 1000 #every 0 is a decimal
delay = 1 #one second
slaveA = b'0xA'
slaveB = b'0xB'
slaveC = b'0xC'
freeBus = Pin(16, Pin.IN)

#define value for read LM35
analog_value = ADC(26)
conversion_factor = 3.3/ 65535

#define pin for photoresist
photoResist = ADC(27)

#define pin for potenciometro
potenciometer_analog_value = ADC(28)

#define pin distance
trigger = Pin(15,Pin.OUT)
echo = Pin(14, Pin.IN)

def readTemperature():
    temp_voltage_raw = analog_value.read_u16()
    convert_voltage = temp_voltage_raw*conversion_factor
    tempC = convert_voltage/(10.0 / 1000)
    return tempC

def readLight():
    return photoResist.read_u16()

def readPotenciometer():
    return potenciometer_analog_value.read_u16()

def readDistance():
    trigger.high()
    utime.sleep_ms(10)
    trigger.low()
    
    while echo.value() == 0:
        star = utime.ticks_us()
    while echo.value() ==1:
        end = utime.ticks_us()
        
    duration = end - star
    distance = (duration * 0.0343) / 2
    return distance

def sendValueInt(value):
    value = int(value)
    data = bytearray(value.to_bytes(2, 'big'))#convert 16-bit integer value to two 8-bit bytes
    uart.write(data) #send two bytes
    
def sendValueFloat(value):
    value = int(value*num_decimals)#save some decimals
    data = bytearray(value.to_bytes(2, 'big'))#convert 16-bit integer value to two 8-bit bytes
    uart.write(data) #send two bytes
    
def sendDates():
    #loading values
    temperature=readTemperature()
    light = readLight()
    potenciometer = readPotenciometer()
    distance = readDistance()
    
    #sending values
    uart.write(slaveA)
    sendValueFloat(temperature)
    sendValueInt(light)
    sendValueInt(potenciometer)
    sendValueFloat(distance)
    
    uart.write(slaveB)
    sendValueInt(potenciometer)
    
    uart.write(slaveC)
    sendValueInt(distance)
    
def main():
    while True :
        try:
            sendDates()
        except Exception as e:
            print("Error:", e)
        utime.sleep(2)
        
if __name__ == '__main__':
    main()
    