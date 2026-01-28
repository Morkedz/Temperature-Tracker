from gpiozero import Button, MCP3008
import math
from time import sleep
from matplotlib import pyplot as plt

temp_pin = MCP3008(channel = 0)
temp_but = Button(18)
x = []
y = []

def print_cond(cond):
    if cond == 1:
        print("appropriate")
    else:
        print("hot")

def loop():
    status = 1
    tmp = 1
    seconds = 0
    while True:
        ana = temp_pin.value
        vr = float(ana)*3.3
        rt = 10000*vr/(3.3-vr)
        new_temp = 1/((math.log(rt/10000)/3950) + (1/(273.15+25)))
        c = new_temp-273.15
        f = c *(9/5)+32
        print("temp c={:.2f}\ttemp f={:.2f}".format(c,f))
        tmp = not temp_but.is_pressed
        if tmp != status:
            print_cond(tmp)
            status = tmp
        x.append(seconds)
        y.append(c)
        seconds+=1
        sleep(1)
    
if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        plt.plot(x,y)
        plt.xlabel("time (s)")
        plt.ylabel("temperature (c)")
        plt.title("Temperature as a function of time")
        plt.show()
        temp_pin.close()
        temp_but.close()