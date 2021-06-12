import os
import subprocess

def LysnData(appPath):
    moveadb = 'cd C:\\Program Files (x86)\\Nox\\bin'
    if os.path.exists('/sdcard/Lysn'):
        subprocess.call(moveadb+' && adb shell rm -rf /sdcard/Lysn', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /data/data/com.everysing.lysn /sdcard/Lysn"', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /sdcard/Android/data/com.everysing.lysn/cache/.chatFile/ /sdcard/Lysn/LysnMedia"', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /data/system/users/0/settings_secure.xml /sdcard/Lysn/"', shell=True)
    subprocess.call(moveadb+f' && adb pull /sdcard/Lysn {appPath}', shell=True)
    subprocess.call(moveadb+' && adb shell rm -rf /sdcard/Lysn', shell=True)

def TongTongData(appPath):
    moveadb = 'cd C:\\Program Files (x86)\\Nox\\bin'
    if os.path.exists('/sdcard/TongTong'):
        subprocess.call(moveadb+' && adb shell rm -rf /sdcard/TongTong', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /data/data/tomato.solution.tongtong /sdcard/TongTong"', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /storage/emulated/0/Pictures/TongTong/ /sdcard/TongTong/TongMedia"', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /storage/emulated/0/video/TongTong/ /sdcard/TongTong/TongVideo"', shell=True)
    subprocess.call(moveadb+f' && adb pull /sdcard/TongTong {appPath}', shell=True)
    subprocess.call(moveadb+' && adb shell rm -rf /sdcard/TongTong', shell=True)

def KakaoTalkData(appPath):
    moveadb = 'cd C:\\Program Files (x86)\\Nox\\bin'
    subprocess.call(moveadb+' && adb shell rm -rf /sdcard/KakaoTalk', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /data/data/com.kakao.talk /sdcard/KakaoTalk"', shell=True)
    subprocess.call(moveadb+f' && adb pull /sdcard/KakaoTalk {appPath}', shell=True)
    subprocess.call(moveadb+' && adb shell rm -rf /sdcard/KakaoTalk', shell=True)

def WickrData(appPath):
    moveadb = 'cd C:\\Program Files (x86)\\Nox\\bin'
    if os.path.exists('/sdcard/Wickr'):
        subprocess.call(moveadb+' && adb shell rm -rf /sdcard/Wickr', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /data/data/com.mywickr.wickr2 /sdcard/Wickr"', shell=True)
    subprocess.call(moveadb+f' && adb pull /sdcard/Wickr {appPath}', shell=True)
    subprocess.call(moveadb+' && adb shell rm -rf /sdcard/Wickr', shell=True)

def PurpleData(appPath):
    moveadb = 'cd C:\\Program Files (x86)\\Nox\\bin'
    if os.path.exists('/sdcard/Purple'):
        subprocess.call(moveadb+' && adb shell rm -rf /sdcard/Purple', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /data/data/com.mywickr.wickr2 /sdcard/Wickr"', shell=True)
    subprocess.call(moveadb+f' && adb pull /sdcard/Purple {appPath}', shell=True)
    subprocess.call(moveadb+' && adb shell rm -rf /sdcard/Purple', shell=True)