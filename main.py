import machine
import time

led = machine.Pin('LED', machine.Pin.OUT)

# mic
# 出典:[【ADC】RaspberryPi Pico MicroPythonでアナログ入力を使う方法 【CdS】]
# https://tech-and-investment.com/raspberrypi-pico7-adc-cds/
# 16bitの数値一単位での電圧値を設定します
unit = 0.00005035477
mic = machine.ADC(0)

# 閾値 マイクの出力電圧がこの値を超えるとノックと判断します
# Vddを3.3V (36番ピン)に接続＆ゲインが40dBの場合1.5としました
# 環境に合わせて調整してください
threshold = 1.5

print('start')

while (True):
    #time.sleep_ms(30)
    volt_raw = mic.read_u16()
    volt = volt_raw * unit
    volt_abs = abs(volt)
    #print(volt_abs)
    if volt_abs > threshold:
        print('detected: {0}'.format(volt_abs))
        led.on()
    else:
        led.off()
