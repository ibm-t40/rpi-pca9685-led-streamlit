import streamlit as st
from board import SCL, SDA
import busio
import time

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)

# Set the PWM frequency to 60hz.
pca.frequency = 60

# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.

#pca.channels[0].duty_cycle = 0x0000
#pca.channels[1].duty_cycle = 0xffff
#pca.channels[2].duty_cycle = 0xffff
#pca.channels[3].duty_cycle = 0xffff
#pca.channels[4].duty_cycle = 0xffff
#pca.channels[5].duty_cycle = 0xffff
#pca.channels[6].duty_cycle = 0xffff
#pca.channels[7].duty_cycle = 0xffff

#pca.channels[8].duty_cycle = 65535
#pca.channels[9].duty_cycle = 32760
#pca.channels[10].duty_cycle = 0xfff

#for i in range(0,8):
#    pca.channels[i].duty_cycle = 0xffff

# 颜色转为占空比，颜色取值范围是（0,255），占空比取值范围是（0,100）,结果等于(颜色/255)*100
def color2ratio(x,min_color,max_color,min_ratio,max_ratio):
    return (x - min_color) * (max_ratio - min_ratio) / (max_color - min_color) + min_ratio
	
# 颜色设置
def setColor(color):
    R_val,G_val,B_val = color # 把元组解包，赋值给变量
   
    R =color2ratio(R_val, 0, 255, 0, 100)
    G =color2ratio(G_val, 0, 255, 0, 100)
    B =color2ratio(B_val, 0, 255, 0, 100)
        
    # 改变占空比，使用RPI.GPIO的方法ChangeDutyCycle()
    pca.channels[8].duty_cycle = int(65535 * R / 100)
    pca.channels[9].duty_cycle = int(65535 * G / 100)
    pca.channels[10].duty_cycle = int(65535 * B / 100)


def setLED(led,color,brightness):
    #pca.channels[4].duty_cycle = brightness
      
    R_val,G_val,B_val = color # 把元组解包，赋值给变量
   
    R =color2ratio(R_val, 0, 255, 0, 100)
    G =color2ratio(G_val, 0, 255, 0, 100)
    B =color2ratio(B_val, 0, 255, 0, 100)
        
    # 改变占空比，使用RPI.GPIO的方法ChangeDutyCycle()
    pca.channels[8].duty_cycle = int(65535 * R * brightness / 10000)
    pca.channels[9].duty_cycle = int(65535 * G * brightness / 10000)
    pca.channels[10].duty_cycle = int(65535 * B * brightness / 10000)
    
    #setColor(color)
    pca.channels[led].duty_cycle = 0x0000

    #st.write("LED亮度 ", brightness, '%')

def LED_All_On(color,brightness):
    #st.write('LED All On')
    for led in range(0,8):
        setLED(led,color,brightness)

def LED_All_Off():
    #st.write('LED All Off')
    for i in range(0,8):
        pca.channels[i].duty_cycle = 0xffff

def LED_Stepping(color,brightness):
    #st.write('LED Stepping')
    LED_All_Off()
    for j in range(0,2):
        for led in range(0,8):
            #pca.channels[i].duty_cycle = brightness
            setLED(led,color,brightness)
            time.sleep(0.5)
        LED_All_Off()
        time.sleep(0.5)

def LED_Flashing(color,brightness):
    #st.write('LED Flashing')
    for i in range(0,3):
        LED_All_On(color,brightness)
        time.sleep(0.5)
        LED_All_Off()
        time.sleep(0.5)
        


def LED_Breathing(color,brightness):
    #st.write('LED Breathing')
    LED_All_Off()
    for k in range(3):
        for i in range(2,100,5): 
            brightness = i
            LED_All_On(color,brightness)   
            time.sleep(0.1) 
        #time.sleep(1) 
        for j in range(0,92,5):
            brightness = 100-j
            LED_All_On(color,brightness)
            time.sleep(0.1) 
    LED_All_Off()

# Loading转为LED数量，Loading取值范围是（0,100），LED取值范围是（0,8）
def load2led(x,min_load,max_load,min_led,max_led):
    return (x - min_load) * (max_led - min_led) / (max_load - min_load) + min_led

def LED_System_Loading(color,brightness,loading):
    #st.write('System Loading',loading,"%")
    LED = int(load2led(loading, 0, 100, 0, 9))
    st.write("loading",loading,"%")
    LED_All_Off()
    for led in range(0,LED):
        setLED(led,color,brightness)
        #st.write('led',LED)

