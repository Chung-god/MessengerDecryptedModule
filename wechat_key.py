import hashlib
from xml.etree.ElementTree import parse
from xml.etree.ElementTree import Element, dump, ElementTree
import subprocess
import hashlib


def wechat_imei(imei):
    imei = subprocess.check_output('adb shell "service call iphonesubinfo 4 | cut -c 52-66 | tr -d \'.[:space:]\'"', shell=True, encoding='utf-8')
    return imei

def wechat_ua(uin):

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

def wechat_path(root):
    wpath = subprocess.check_output('find ./ -name "EnMicroMsg.db"', shell=True, encoding='utf-8')
    root = wpath[18:50]
    return root

if __name__=='__main__':
    Imei={}
    Uin={}
    Acc={}
    Key={}
    Root={}
    
    Imei=wechat_imei(Imei)
    print(Imei)
    Uin=wechat_ua(Uin)
    print(Uin)
    Key=wechat_en(Uin,Imei)
    print(Key)
    Root=wechat_path(Root)
    print(Root)
