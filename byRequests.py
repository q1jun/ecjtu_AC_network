import os
import re
import time
import requests
from bs4 import BeautifulSoup


def IdAndPasswd():
    ispList = ["@cmcc", "@unicom", "@telecom"]
    osList = ["win", "linux"]
    try:
        with open("/var/www/ecjtu_AC_network/.logindata.data", 'r') as f:
            info = [a.rstrip('\n') for a in f]
        if info.__len__() < 4:
            os.remove("/var/www/ecjtu_AC_network/.logindata.data")
            info.extend((str(input("输入学号：")), str(input("输入密码："))))
            print("1:中国移动  2:中国联通  3:中国电信")
            number = int(input("选择运营商(1-3)："))
            info.append(ispList[number - 1])
            print("1:Windows  2:Linux(Macos)")
            number = int(input("选择操作系统(1-2)："))
            with open("/var/www/ecjtu_AC_network/.logindata.data", 'w') as f:
                info.append(osList[number - 1])
                f.write("\n".join(info))
    except Exception:
        info = [str(input("输入学号："))]
        info.append(str(input("输入密码：")))
        print("1:中国移动  2:中国联通  3:中国电信")
        number = int(input("选择运营商(1-3)："))
        info.append(ispList[number - 1])
        print("1:Windows  2:Linux(Macos)")
        number = int(input("选择操作系统(1-2)："))
        f = open("/var/www/ecjtu_AC_network/.logindata.data", 'w')
        info.append(osList[number - 1])
        with open("/var/www/ecjtu_AC_network/.logindata.data", 'w') as f:
            f.write("\n".join(info))
    return info


def GetIp():
    HOST = "http://172.16.2.100/"
    r = requests.get(HOST)
    bsobj = BeautifulSoup(r.content, 'html5lib')
    return re.findall(r"ss5=\"(.+?)\"", str(bsobj))[0]


def TestLog(requestObj):
    print("************** test log start *******************")
    print("Status Code: ", end="\t")
    print(requestObj.status_code)
    print("Url: ", end="\t")
    print(requestObj.url)
    print("Headers: ", end="\t")
    print(requestObj.headers)
    print("Cookies: ", end="\t")
    print(requestObj.cookies)
    print("History: ", end="\t")
    print(requestObj.history)
    print("-------------- All content ----------------------")
    print(requestObj.text)
    print("*************** test log end ********************")


def showLog(requestObj):
    result = re.findall(r"认证成功页", requestObj.text)
    if (len(result) > 0):
        for _ in range(10):
            print("*************** ok ********************")


def ACLogin(ip, id, passwd, isp):
    url = "http://172.16.2.100:801/eportal/"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3759.4 Safari/537.36",
        "Referer": f"http://172.16.2.100/a70.htm?wlanuserip={ip}&wlanacip=null&wlanacname=null&vlanid=0&ip={ip}&ssid=null&areaID=null&mac=00-00-00-00-00-00",
        "Connection": "keep-alive", "Host": "172.16.2.100:801", "Origin": "http://172.16.2.100"}

    payload = {
        "c": "ACSetting",
        "a": "Login",
        "protocol": "http:",
        "hostname": "172.16.2.100",
        "iTermType": "1",
        "wlanuserip": ip,
        "wlanacip": "null",
        "wlanacname": "null",
        "mac": "00-00-00-00-00-00",
        "ip": ip,
        "enAdvert": "0",
        "queryACIP": "0",
        "loginMethod": "1"
    }
    postData = {"DDDDD": f",0,{id}{isp}", "upass": passwd, "R1": "0", "R2": "0", "R3": "0", "R6": "0", "para": "00",
                "0MKKey": "123456", "buttonClicked": "", "redirect_url": "", "err_flag": "", "username": "",
                "password": "", "user": "", "cmd": "", "Login": ""}

    cookiesData = {"ISP_select": isp, "areaID": "null", "ip": ip, "md5_login2": f"%2C0%2C{id}{isp}%7C{passwd}",
                   "program": "test", "ssid": "null", "vlan": "0"}

    acRequest = requests.post(
        url, params=payload, data=postData, cookies=cookiesData, headers=headers)
    showLog(acRequest)


def getIpandMac_win():
    ipmac = os.popen("ipconfig /all").read()
    ip = re.findall(r"\d+.\d+.\d+.\d+", ipmac)[0]
    mac = re.findall(r"\w+-\w+-\w+-\w+-+\w+-\w+", ipmac)[0]
    dmac = ""
    for a in mac.split("-"):
        dmac += a
    return (ip, dmac,)


def getIpandMac_linux():
    ipmac = os.popen("ifconfig -a").read()
    ip = re.findall(r"\d+.\d+.\d+.\d+", ipmac)[0]
    mac = re.findall(r"\w+:\w+:\w+:\w+:+\w+:\w+", ipmac)[0]
    dmac = ""
    for a in mac.split(":"):
        dmac += a
    return (ip, dmac,)


def ACLogout(id, passwd, isp, os):
    if os == "linux":
        print(f'os = {os}')
        ip = getIpandMac_linux()[0]
        mac = getIpandMac_linux()[1]
    else:
        print(f'os = {os}')
        ip = getIpandMac_win()[0]
        mac = getIpandMac_win()[1]

    url = "http://172.16.2.100:801/eportal/"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3759.4 Safari/537.36",
        "Referer": f"http://172.16.2.100/a70.htm?wlanuserip={ip}&wlanacip=null&wlanacname=null&vlanid=0&ip={ip}&ssid=null&areaID=null&mac=00-00-00-00-00-00",
        "Connection": "keep-alive", "Host": "172.16.2.100:801", "Origin": "http://172.16.2.100"}

    payload = {
        "c": "ACSetting",
        "a": "Logout",
        # "protocol": "http:",
        "hostname": "172.16.2.100",
        "iTermType": "1",
        "wlanuserip": "null",
        "wlanacip": "null",
        "wlanacname": "null",
        "mac": mac,
        "queryACIP": "0",
        "port": ""
    }

    cookiesData = {"ISP_select": isp, "areaID": "null", "ip": ip, "md5_login2": f"%2C0%2C{id}{isp}%7C{passwd}",
                   "program": "test", "ssid": "null", "vlan": "0"}

    acRequest = requests.post(
        url, params=payload, cookies=cookiesData, headers=headers)
    # TestLog(acRequest)


# info = IdAndPasswd()
# ACLogout(info[0], info[1], info[2], info[3])
# ip = GetIp()
# ACLogin(ip, info[0], info[1], info[2])

"""
定时
"""
import time
import schedule


def job():
    print("[+]I'm logging in...now is ：",end='')
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    info = IdAndPasswd()
    ACLogout(info[0], info[1], info[2], info[3])
    ip = GetIp()
    ACLogin(ip, info[0], info[1], info[2])


if __name__ == "__main__":
    # schedule.run_all()
    print('[+]正在执行定时项目......')
    schedule.every().day.at("02:30").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
