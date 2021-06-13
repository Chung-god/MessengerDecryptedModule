import os
import subprocess

def LysnData(appPath):
    moveadb = 'cd C:\\Program Files (x86)\\Nox\\bin'
    subprocess.call(moveadb+' && adb shell rm -rf /sdcard/Lysn', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /data/data/com.everysing.lysn /sdcard/Lysn"', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /sdcard/Android/data/com.everysing.lysn/cache/.chatFile/ /sdcard/Lysn/LysnMedia"', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /data/system/users/0/settings_secure.xml /sdcard/Lysn/"', shell=True)
    subprocess.call(moveadb+f' && adb pull /sdcard/Lysn {appPath}', shell=True)
    subprocess.call(moveadb+' && adb shell rm -rf /sdcard/Lysn', shell=True)

def TongTongData(appPath):
    moveadb = 'cd C:\\Program Files (x86)\\Nox\\bin'
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
    subprocess.call(moveadb+' && adb shell rm -rf /sdcard/Wickr', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /data/data/com.mywickr.wickr2 /sdcard/Wickr"', shell=True)
    subprocess.call(moveadb+f' && adb pull /sdcard/Wickr {appPath}', shell=True)
    subprocess.call(moveadb+' && adb shell rm -rf /sdcard/Wickr', shell=True)

def PurpleData(appPath):
    moveadb = 'cd C:\\Program Files (x86)\\Nox\\bin'
    subprocess.call(moveadb+' && adb shell rm -rf /sdcard/PurPle', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /data/data/com.ncsoft.community /sdcard/PurPle"', shell=True)
    subprocess.call(moveadb+f' && adb pull /sdcard/PurPle {appPath}', shell=True)
    subprocess.call(moveadb+' && adb shell rm -rf /sdcard/PurPle', shell=True)

def WeChatData(appPath):
    moveadb = 'cd C:\\Program Files (x86)\\Nox\\bin'
    subprocess.call(moveadb+' && adb shell rm -rf /sdcard/WeChat', shell=True)
    subprocess.call(moveadb+' && adb shell "su root cp -r /data/data/com.tencent.mm /sdcard/WeChat"', shell=True)
    p = "/storage/emulated/0/Android/data/com.tencent.mm/MicroMsg"
    imgpath = subprocess.check_output(moveadb+f' && adb shell su root find {p} -name voice2', shell=True)
    rand = imgpath.decode().split('/')[-2]
    p = f"{p}/{rand}/"
    subprocess.call(moveadb+f' && adb shell mkdir /sdcard/WeChat/WCMedia', shell=True)
    subprocess.call(moveadb+f' && adb shell cp $(find {p} -type f -name "*.mp4") /sdcard/WeChat/WCMedia', shell=True)
    subprocess.call(moveadb+f' && adb shell cp $(find {p} -type f -name "*.jpg") /sdcard/WeChat/WCMedia', shell=True)
    subprocess.call(moveadb+f' && adb shell cp $(find {p} -type f -name "*.amr") /sdcard/WeChat/WCMedia', shell=True)
    subprocess.call(moveadb+f' && adb pull /sdcard/WeChat {appPath}', shell=True)
    subprocess.call(moveadb+' && adb shell rm -rf /sdcard/WeChat', shell=True)
    