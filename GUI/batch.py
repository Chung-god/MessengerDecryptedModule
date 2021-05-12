import os
import subprocess

def LysnData(phoneNo):
    if os.path.exists('/sdcard/Lysn'):
        subprocess.call('adb shell rm -rf /sdcard/Lysn', shell=True)
    subprocess.call('adb shell "su root cp -r /data/data/com.everysing.lysn /sdcard/Lysn"', shell=True)
    subprocess.call('adb shell "su root cp -r /sdcard/Android/data/com.everysing.lysn/cache/.chatFile/ /sdcard/Lysn/LysnMedia"', shell=True)
    subprocess.call('adb shell "su root cp -r /data/system/users/0/settings_secure.xml /sdcard/Lysn/"', shell=True)
    subprocess.call(f'adb pull /sdcard/Lysn AppData/{phoneNo}', shell=True)
    subprocess.call('adb shell rm -rf /sdcard/Lysn', shell=True)

def TongTongData(phoneNo):
    subprocess.call('adb shell "su root cp -r /data/data/tomato.solution.tongtong/ /sdcard/TongTong"', shell=True)
    subprocess.call(f'adb pull /sdcard/TongTong AppData/{phoneNo}', shell=True)
    subprocess.call('adb shell rm -rf /sdcard/TongTong', shell=True)

def KakaoTalkData(phoneNo):
    subprocess.call('adb shell "su root cp -r /data/data/com.kakao.talk/ /sdcard/KakaoTalk"', shell=True)
    subprocess.call('adb shell "su root cp -r /sdcard/Android/data/com.kakao.talk/cache/ /sdcard/KakaoTalk/KakaoTalkMedia"', shell=True)
    subprocess.call(f'adb pull /sdcard/KakaoTalk AppData/{phoneNo}', shell=True)
    subprocess.call('adb shell rm -rf /sdcard/KakaoTalk', shell=True)

