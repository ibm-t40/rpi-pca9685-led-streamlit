import streamlit as st
import pca9685_led as pca_led
import busio
import numpy as np
import time


st.title("PCA9685 LED控制")

 
st.subheader("颜色控制：")
#level_r = st.slider("Red Level: ",  0, 65535, 32760)
#level_g = st.slider("Green Level: ",0, 65535, 32760)
#level_b = st.slider("Blue Level: ", 0, 65535, 32760)
level_R = st.slider("Red Level: ",  0, 255, 255)
level_G = st.slider("Green Level: ",0, 255, 255)
level_B = st.slider("Blue Level: ", 0, 255, 255)
#st.write("当前LED颜色： ", "RGB[",level_R,",",level_G,",",level_B,"]")
color = level_R,level_G,level_B
st.write("当前LED颜色： ", "RGB",color)
pca_led.setColor(color)

st.subheader("亮度控制：")
#L=R*0.30+G*0.59+B*0.11
max_brightness = max(level_R, level_R, level_B)
brightness= st.slider('LED Brightness', 0, 100, 100)
st.write("LED亮度 ", brightness,"%")
pca_led.LED_All_On(color,brightness)


st.subheader("行为控制：")
behavior = st.radio(
    "LED Behavior",
    ('All On','Stepping','Flashing','Breathing','System Loading'))

if behavior == 'All On':
    st.write('LED All On')
    pca_led.LED_All_On(color,brightness)

elif behavior == 'Stepping':
    st.write('LED Stepping')
    pca_led.LED_Stepping(color,brightness)

elif behavior == 'Flashing':
    st.write('LED Flashing')
    pca_led.LED_Flashing(color,brightness)

elif behavior == 'Breathing':
    st.write('LED Breathing')
    pca_led.LED_Breathing(color,brightness)

elif behavior == 'System Loading':
    loading= st.slider('Manual', 0, 100, 20)    
    #st.write('System Loading',loading,"%")
    pca_led.LED_System_Loading(color,brightness,loading)

    bt_random=st.button('Random')
    if bt_random:
        for int in range(20):
            loading = np.random.randint(1,100)
            # delay 1 second
            time.sleep(0.5) 
            pca_led.LED_System_Loading(color,brightness,loading)

else:
    st.write('LED off')