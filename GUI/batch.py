import os
import subprocess

def LysnData(phoneNo):
    moveadb = 'cd C:\\Program Files (x86)\\Nox\\bin'
    if os.path.exists('/sdcard/Lysn'):
        subprocess.call(moveadb+' && adb shell rm -rf /sdcard/Lysn', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /data/data/com.everysing.lysn /sdcard/Lysn"', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /sdcard/Android/data/com.everysing.lysn/cache/.chatFile/ /sdcard/Lysn/LysnMedia"', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /data/system/users/0/settings_secure.xml /sdcard/Lysn/"', shell=True)
    subprocess.call(moveadb+f' && adb pull /sdcard/Lysn C:/AppData/{phoneNo}', shell=True)
    subprocess.call(moveadb+' && adb shell rm -rf /sdcard/Lysn', shell=True)

def TongTongData(phoneNo):
    moveadb = 'cd C:\\Program Files (x86)\\Nox\\bin'
    if os.path.exists('/sdcard/TongTong'):
        subprocess.call(moveadb+' && adb shell rm -rf /sdcard/TongTong', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /data/data/tomato.solution.tongtong/ /sdcard/TongTong"', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /storage/emulated/0/Pictures/TongTong/thumbnail/ /sdcard/TongTong/TongMedia"', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /storage/emulated/0/tongtong/ /sdcard/TongTong/Tongaudio"', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /storage/emulated/0/video/TongTong/encoded_video/ /sdcard/TongTong/TongVideo"', shell=True)
    subprocess.call(moveadb+f' && adb pull /sdcard/TongTong C:/AppData/{phoneNo}', shell=True)
    subprocess.call(moveadb+' && adb shell rm -rf /sdcard/TongTong', shell=True)

def KakaoTalkData(phoneNo):
    moveadb = 'cd C:\\Program Files (x86)\\Nox\\bin'
    if os.path.exists('/sdcard/KakaoTalk'):
        subprocess.call(moveadb+' && adb shell rm -rf /sdcard/KakaoTalk', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /data/data/com.kakao.talk/ /sdcard/KakaoTalk"', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /sdcard/Android/data/com.kakao.talk/cache/ /sdcard/KakaoTalk/KakaoTalkMedia"', shell=True)
    subprocess.call(moveadb+f' && adb pull /sdcard/KakaoTalk C:/AppData/{phoneNo}', shell=True)
    subprocess.call(moveadb+' && adb shell rm -rf /sdcard/KakaoTalk', shell=True)

