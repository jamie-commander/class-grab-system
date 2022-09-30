from bs4 import BeautifulSoup
import json
import requests
import random
import threading
import os
import time
class NKUST_Grab_A_Course:
    def __init__(self,account,password):
        self.UserAccount = account
        self.UserPassword = password
        self.r = requests.session()#建立一個session，讓每次request都算同一次，才能連續執行動作。
        self.LoginPage_URL = "https://aais6.nkust.edu.tw/selcrs_std"#高科大學生選課系統登入首頁網址。
        self.LoginPage_RVT = ""#LoginPage_RequestVerificationToken
        self.LoginButtom_URL = "https://aais6.nkust.edu.tw/selcrs_std/Login"#按下登入時post的網址。
        self.SelectPage_URL = "https://aais6.nkust.edu.tw/selcrs_std/FirstSelect/SelectPage"#高科大學生選課系統選課網址。
        self.SelectPage_RVT = ""#SelectPage_RequestVerificationToken
        self.CourseUnitCollection_URL = "https://aais6.nkust.edu.tw/selcrs_std/Unit/CourseUnitCollection"#請求下拉選單資訊網址
        self.CourseUnitCollection_Data = ""#儲存選單資訊
        self.CourseSearch_URL = "https://aais6.nkust.edu.tw/selcrs_std/FirstSelect/CourseSearch"#請求查詢課程資訊網址
        self.CourseSearch_Data = ""#儲存課程資訊
        self.AddPreSelCrs_URL = "https://aais6.nkust.edu.tw/selcrs_std/FirstSelect/AddPreSelCrs"#請求新增課程網址
        self.AddPreSelCrs_Data = ""
    def Get_LoginPage_RVT(self):
        request_out = 5
        head = {
            "referer" : "https://aais5.nkust.edu.tw/selcrs_std/PreselecrsList",
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
            }
        while(request_out != 0):
            try:
                LoginPage_Html = self.r.get(self.LoginPage_URL, headers = head, timeout = 1)
                #對伺服器發出get，取得登入頁面。
                #print(LoginPage_Html)
                #確認是否請求成功 200
                LoginPage_Html.encoding = "utf-8"#編碼成utf-8
                #print(LoginPage_Html.text)
                #未解析的資料是一大串字串，難以抓取資料，因此需要解析。
                LoginPage_Soup = BeautifulSoup(LoginPage_Html.text, 'html.parser')
                #解析LoginPage_Html。
                #print(LoginPage_Soup)
                #查看解析後內容
                LoginPage_Input = LoginPage_Soup.select("input")
                #抓取頁面中為input的標籤。
                #print("RVT :",LoginPage_Input[1]["value"])
                #該頁面第二個input有我們需要的RequestVerificationToken值。
                self.LoginPage_RVT = LoginPage_Input[1]["value"]
                #儲存到LoginPage_RVT。
                return True
            except:
                time.sleep(random.randint(1,3))
                request_out =  request_out - 1
                continue
        return False
    def Login(self):
        request_out = 5
        head = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
            "content-type" : "application/x-www-form-urlencoded",
            "origin" : "https://aais5.nkust.edu.tw",
            "referer" : "https://aais5.nkust.edu.tw/selcrs_std"
            }
        data = {
            "__RequestVerificationToken": self.LoginPage_RVT,
            "Url": "/selcrs_std/PreselecrsList",
            "UserAccount": self.UserAccount,
            "Password": self.UserPassword
            }
        while(request_out != 0):
            try:
                LoginButtom = self.r.post(self.LoginButtom_URL,data=data, headers = head, timeout = 1)
                #對伺服器發出post，達成登入動作。
                #print(LoginButtom)
                #確認是否請求成功 200
                return True
            except:
                time.sleep(random.randint(1,3))
                request_out =  request_out - 1
                continue
        return False
    def Get_SelectPage_RVT(self):
        request_out = 5
        head = {
            "referer" : "https://aais5.nkust.edu.tw/selcrs_std/Home/About",
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
            }
        while(request_out != 0):
            try:
                SelectPage_Html = self.r.get(self.SelectPage_URL, headers = head, timeout = 1)
                #對伺服器發出get，取得選課頁面。
                #print(SelectPage_Html)
                #確認是否請求成功 200
                SelectPage_Html.encoding = "utf-8"#編碼成utf-8
                #print(SelectPage_Html.text)
                #未解析的資料是一大串字串，難以抓取資料，因此需要解析。
                SelectPage_Soup = BeautifulSoup(SelectPage_Html.text, 'html.parser')
                #解析SelectPage_Html。
                #print(SelectPage_Soup)
                #查看解析後內容
                SelectPage_Input = SelectPage_Soup.select("input")
                #抓取頁面中為input的標籤。
                #print("RVT :",SelectPage_Input[len(SelectPage_Input)-1]["value"])
                #該頁面最後一個input有我們需要的RequestVerificationToken值。
                self.SelectPage_RVT = SelectPage_Input[len(SelectPage_Input)-1]["value"]
                #儲存到SelectPage_RVT。
                return True
            except:
                time.sleep(random.randint(1,3))
                request_out =  request_out - 1
                continue
        return False
    def CoursUnitCollection(self):
        request_out = 5
        head={
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://aais6.nkust.edu.tw",
            "referer": "https://aais6.nkust.edu.tw/selcrs_std/FirstSelect/SelectPage",
            "requestverificationtoken": self.SelectPage_RVT,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
           }
        data = {
            "CrsType": "A",
            "ShortTerm": "N"
            }
        while(request_out != 0):
            try:
                CourseUnitCollection = self.r.post(self.CourseUnitCollection_URL ,data=data, headers = head, timeout = 0.5)
                #對伺服器發出post，取得下拉選單資訊。
                self.CourseUnitCollection_Data = json.loads(CourseUnitCollection.text)
                #將資料存成json型態
                #print(self.CourseUnitCollection_Data[0])
                #印出第一筆資料來查看是否有成功
                return True
            except:
                time.sleep(random.randint(1,3))
                request_out =  request_out - 1
                continue
        return False
    def CourseSearch(self,number = ""):
        request_out = 5
        head={
            "Content-Type": "application/json; charset=UTF-8",
            "origin": "https://aais6.nkust.edu.tw",
            "referer": "https://aais6.nkust.edu.tw/selcrs_std/FirstSelect/SelectPage",
            "requestverificationtoken": self.SelectPage_RVT,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
           }
        data = {
            "SearchViewModel":{#在此你可以依據取得的下拉表單資訊帶入查詢，我僅用課程代碼示範。
                "cmp_area":"1",
                "dgr_id":"14",
                "unt_id":"UE29",
                "cls_year":"3",
                "cls_seq":"ALL",
                "scr_selcode": number,#課程代碼，當課程代碼不為""時，僅查詢課程代碼。
                "scr_language":"",
                "scr_time":"",
                "CrsType":"N"
                }
            }
        while(request_out != 0):
            try:
                CourseSearch = self.r.post(self.CourseSearch_URL ,data=json.dumps(data), headers = head, timeout = 0.5)
                #對伺服器發出post，取得課程資訊。
                self.CourseSearch_Data = json.loads(CourseSearch.text)
                #將資料存成json型態
                #print(self.CourseSearch_Data["recordsTotal"])
                #總共查詢到幾個課程
                #print(self.CourseSearch_Data["data"][0])
                #第一筆課程資訊，以課程代碼查詢僅會查詢到一筆。
                return True
            except:
                time.sleep(random.randint(1,3))
                request_out =  request_out - 1
                continue
        return False
    def AddPreSelCrs(self,number = ""):
        request_out = 5
        head={
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://aais6.nkust.edu.tw",
            "referer": "https://aais6.nkust.edu.tw/selcrs_std/FirstSelect/SelectPage",
            "requestverificationtoken": self.SelectPage_RVT,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
           }
        data = {
            "CrsNo": number,#選課代號
            "PCrsNo": self.CourseSearch_Data["data"][0]['scj_sub_percode'],#可用剛剛查詢課程資訊的函示查詢該筆資料
            "SelType": "O",
            "CrsType": self.CourseSearch_Data["data"][0]['CrsType'],
            "NewClass": "N"
            }
        while(request_out != 0):
            try:
                AddPreSelCrs = self.r.post(self.AddPreSelCrs_URL ,data=data, headers = head, timeout = 0.5)
                #對伺服器發出post，新增課程。
                self.AddPreSelCrs_Data = json.loads(AddPreSelCrs.text)
                print(self.AddPreSelCrs_Data["result"])
                print(self.AddPreSelCrs_Data["MessageBotton"])
                print(self.AddPreSelCrs_Data["MessageShow"])
                #印出資訊查看是否有新增成功
                return True
            except:
                time.sleep(random.randint(1,3))
                request_out =  request_out - 1
                continue
        return False
if __name__ == '__main__':
    Start = NKUST_Grab_A_Course("C108152305","abc900403")
    Start.Get_LoginPage_RVT()
    Start.Login()
    Start.Get_SelectPage_RVT()
    Start.CoursUnitCollection()
    Start.CourseSearch("0988")
    Start.AddPreSelCrs("0988")
