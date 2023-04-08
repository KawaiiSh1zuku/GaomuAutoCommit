import requests
import time
import random

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://data.gaomuxuexi.com",
    "Referer": "https://data.gaomuxuexi.com/s/wap/index.htm",
    "S_HASH": "/home/class",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
cookie = None
sid = 0

def Login(account, password):
    url = "https://data.gaomuxuexi.com/s_login"
    data = {
        "ACCOUNT": account,
        "PWD": password,
        "ATYPE": 1,
        "TLOCATE": int(round(time.time() * 1000)),
        "READONLY": 0,
        "AUTO": 0,
        "AGENT": 0
    }
    r = requests.post(url, json=data, headers=headers)
    global cookie
    global sid
    cookie = r.cookies
    sid = r.json()['sID']
    print(f"登录用户: {r.json()['class']['cName']} {r.json()['name']}")

def ccgQry():
    url = "https://data.gaomuxuexi.com/s_ccgQry"
    data = {
        "COURSE": 5,
        "STATE": 1
    }
    r = requests.post(url, json=data, headers=headers, cookies=cookie)
    if (r.json()["no"] == 200):
        ccgList = r.json()["ccg"]
    else:
        print(r.json())
        exit()
    for i in range(len(ccgList)):
        if(ccgList[i]["done"] == 0):#未完成的作业
            print(ccgList[i]["id"], ccgList[i]["tit"])
            return ccgList[i]["id"]

def ccgLstQ(ccgId):
    url = "https://data.gaomuxuexi.com/s_ccgLstQ"
    data = {
        "SID": sid,
        "TKID": ccgId
    }
    r = requests.post(url, json=data, headers=headers, cookies=cookie)
    if (r.json()["no"] == 200):
        Qs = r.json()["Qs"]
        return Qs
    else:
        print(r.json())
        exit()

def getAnswer(Qs):
    for i in range(len(Qs)):
        qid = Qs[i][0]
        url = f"https://data.gaomuxuexi.com/q_get?COURSE=5&QLIB=0&QID={qid}&Q=1&V=1"
        r = requests.get(url, headers=headers, cookies=cookie)
        if (r.json()["no"] == 200):
            Q = r.json()["Q"]
            question = Q["Q"].replace(u'&nbsp;', u'').split('<')[0]
            answer = Q["A"][0]["A"]
            answerStr = chr(answer + 65)
            print(question, answerStr)
            qCommit(qid, answer, i, ccgId, question[:32])
        else:
            print(r.json())
            exit()

def qCommit(Qid, Answer, TKQIDX, TKID, QTXT):
    url = "https://data.gaomuxuexi.com/s_qCommit"
    timeU = random.randint(9, 15)
    params = {
        "Q": f"[{Qid},1,{str(timeU)},{Answer},{Answer}]",
        "NEXTQ": 0,
        "QTXT": QTXT,
        "TKQIDX": TKQIDX,
        "TKID": TKID,
        "COURSE": 5,
        "BOOKVER": 1
    }
    r = requests.post(url, headers=headers, cookies=cookie, json=params)
    if (r.json()["no"] == 200):
        #print(r.json())
        pass
    else:
        print(r.json())
        exit()
    time.sleep(8)
    
if __name__ == "__main__":
    Login("account", "password")
    ccgId = ccgQry()
    getAnswer(ccgLstQ(ccgId))
