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
threshold = 1.65

# インターバル（ミリ秒）
sleep_ms = 10

# volt: 検出した電圧値
# threshold: しきい値
def is_detect_sound(volt, threshold):
    return volt > threshold

# 音を検知するかどうか
is_detect_sound = False

# 最後に音を検知することになった時間
last_detect_sound_activated_time = -1

# 音を検知しない間のスリープ秒数
inactive_sleep_seconds = 60 * 30 # 30分

# 音の検知を行う時間帯かどうかを判定する
def detect_sound_by_time(now):
    target_time = time.gmtime(now)
    hour = target_time[3]

    # UTC 0000-1200 (JST 0900-2100)
    if (hour >= 0 and hour <= 12):
        return True

    return False

# 前回通知したタイムスタンプ
last_notified_time = -1

# 通知間隔（秒数）
notify_interval = 5

# 検出した時の通知処理
def notify(now, volt):
    global led, last_notified_time
    if (last_notified_time < 0 or (now - last_notified_time) > notify_interval):
        print('notify: now={0}, volt={1}, last_notified_time={2}, notify_interval={3}'.format(now, volt, last_notified_time, notify_interval))
        last_notified_time = now
        led.on()
        
while (True):
    now = time.time()
    if (last_detect_sound_activated_time < 0 or (now - last_detect_sound_activated_time > inactive_sleep)):
        is_detect_sound = detect_sound_by_time(now)

    if (not is_detect_sound):
        time.sleep(inactive_sleep_seconds)
        continue

    time.sleep_ms(sleep_ms)
    volt_raw = mic.read_u16()
    volt = abs(volt_raw * unit)
    #print(volt)
    
    # detect sound
    if is_detect_sound(volt, threshold):
        notify(time.time(), volt)
    else:
        led.off()
