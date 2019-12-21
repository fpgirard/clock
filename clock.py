# Time functions
import utime, ntptime, network
from machine import I2C, Pin

# LED stuff
import tm1637
tm = tm1637.TM1637(clk=Pin(0), dio=Pin(16))
tm.brightness(0)
tm.write([0, 0, 0, 0])

import mpu6050
i2c = I2C(scl=Pin(5), sda=Pin(4))
accelerometer = mpu6050.accel(i2c)

# networking stuff
sta_if = network.WLAN(network.STA_IF) 

def get_time(sta_if):
   if sta_if.isconnected():
      ntptime.settime()
      return (utime.localtime(utime.mktime(utime.localtime()) - 5*3600))

def get_motion():
   d = motion=accelerometer.get_values()
   return d['GyZ']
   
def baseline(samples):
   sum = 0
   for i in range(samples):
      sum += get_motion()
      utime.sleep_ms(100)
   return sum/samples

def show_time(seconds):
   counter = 0
   localtime = get_time(sta_if)
   while (counter <= seconds): 
      tm.numbers(localtime[3],localtime[4])
      utime.sleep(1)
      counter += 1
   tm.write([0, 0, 0, 0])

immobile = abs(baseline(10))

while(True):
   new_motion = abs(get_motion())   
   if (new_motion > (2 * immobile)) :
      print("new_motion is: ",new_motion, "immobile: ",immobile)
      get_time(sta_if)
      show_time(4)
      immobile = baseline(10)
   utime.sleep_ms(100)
