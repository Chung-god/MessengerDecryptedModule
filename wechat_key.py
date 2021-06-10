from xml.etree.ElementTree import parse
from xml.etree.ElementTree import Element, dump, ElementTree
import subprocess
import hashlib
import os


def wechat_imei():
    imei = subprocess.check_output('adb shell "service call iphonesubinfo 4 | cut -c 52-66 | tr -d \'.[:space:]\'"', shell=True, encoding='utf-8')
    return imei

def wechat_ua():

    tree = parse('com.tencent.mm_preferences.xml')
    root = tree.getroot()

    map= (root.findall("string"))
    uin = map[4].text
    return uin

def wechat_en(UIN,IMEI):
    
    UIN2 = UIN.encode()
    IMEI2 = IMEI.encode()


    EN_string = IMEI2 + UIN2
    EN_key = hashlib.md5(EN_string).hexdigest()
    key = EN_key[:7]
    
    return key

def wechat_path():
    wpath = subprocess.check_output('find ./ -name "EnMicroMsg.db"', shell=True, encoding='utf-8')
    root = wpath[18:50]
    return root

def wechat_mkdir():
    subprocess.check_output('mkdir -p Wechat/media', shell=True)

def wechat_media():
    filename = subprocess.check_output('find ./ -name *.jpg 2>/dev/null > imagefile.txt' ,shell=True, encoding='utf-8')
    imagefilelist = open('imagefile.txt', 'r').read().split('\n')
    for i in imagefilelist :
        path1 = i[2:57]
        path2 = i[57:60]
        path3 = i[60:64]
        imgfile = i[64:101]
        path = path1 + path2 + path3
        subprocess.run('cp -p ' + path + imgfile + ' ' + 'Wechat/media/' + imgfile ,shell=True)

if __name__=='__main__':
    Imei={}
    Uin={}
    Acc={}
    Key={}
    Root={}
    Mkdir={}
    Media={}
    
    Imei=wechat_imei()
    Uin=wechat_ua()
    Key=wechat_en(Uin,Imei)
    Root=wechat_path()
    Mkdir=wechat_mkdir()
    Media=wechat_media()
    
