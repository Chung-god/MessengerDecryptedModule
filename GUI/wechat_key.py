from xml.etree.ElementTree import parse
from xml.etree.ElementTree import Element, dump, ElementTree
import subprocess
import hashlib
import os


def wechat_imei():
    imei = subprocess.check_output('adb shell "service call iphonesubinfo 4 | cut -c 52-66 | tr -d \'.[:space:]\'"', shell=True, encoding='utf-8')
    return imei

def wechat_ua(path):
    path = path + 'shared_prefs/system_config_prefs.xml'
    tree = parse(path)
    root = tree.findall('./int')
    for i in root:
        if i.get('name') == 'default_uin':
            uin = i.get('value')
    return uin

def wechat_me(path):
    path = path + 'shared_prefs/com.tencent.mm_preferences.xml'
    tree = parse(path)
    name = tree.find('./string[@name="last_login_nick_name"]').text
    return name

def wechat_en(UIN, IMEI):
    UIN = UIN.encode()
    IMEI = IMEI.encode()
    EN_string = IMEI + UIN
    EN_key = hashlib.md5(EN_string).hexdigest()
    key = EN_key[:7]
    return key

def wechat_path(path):
    path=path.replace('/','\\')
    wpath = subprocess.check_output(f"where /r {path} EnMicroMsg.db", shell=True, encoding='utf-8')
    dbfile = wpath.split('\n')[0]
    return dbfile

def wechat_media(path, rpath):
    path=path.replace('/','\\')
    rpath = rpath.replace('/','\\')+'\\image2'
    os.makedirs(f'{path}/WCMedia/image', exist_ok=True)
    filepath = subprocess.check_output(f'where /r {rpath} *.jpg' ,shell=True)
    filelist = filepath.decode().split('\r\n')[:-1]
    for file in filelist :
        subprocess.run(f'copy {file} {path}WCMedia\\image',shell=True)
    

if __name__=='__main__':
    Imei=wechat_imei()
    path = 'C:/MDTool/SM-G925S/20210614-WeChat-4/WeChat/'
    uin=wechat_ua(path)
    Key=wechat_en(uin,Imei)
    Root=wechat_path(path)
    rpath = 'C:/MDTool/SM-G925S/20210614-WeChat-4/WeChat/MicroMsg/a9323caa87f66a4d82248f72601d7b5c'
    wechat_media(path, rpath)
    
