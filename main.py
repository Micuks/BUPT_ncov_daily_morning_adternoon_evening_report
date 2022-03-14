import requests
import json
import os

LOGIN_URL = "https://app.bupt.edu.cn/uc/wap/login/check"
GET_URL = 'https://app.bupt.edu.cn/xisuncov/wap/open-report/index'
POST_URL = 'https://app.bupt.edu.cn/xisuncov/wap/open-report/save'
__uname = os.environ['BUPT_USERNAME']
__upswd = os.environ['BUPT_PASSWORD']

FormData = []

Connection = requests.session()

#Login
Result = Connection.post(
    url = LOGIN_URL,
    data = {'username': __uname, 'password': __upswd}
)
if Result.status_code != 200:
    print("Failed to login. Check your username and password.", Result.status_code)
    exit()
else:
    print("Successfully logged in.")

#Get
Result = Connection.post(
    url = GET_URL
)
if Result.status_code != 200:
    print("Failed to get form data.", Result.status_code)
    exit()
else:
    with open("last_get.json", "w") as fp:
        fp.write(Result.text)
    #print(Result.text)
    NewFormData = json.load(open("last_get.json", "r"))
    NewFormData = NewFormData['d']['info']
    del NewFormData['date']
    del NewFormData['flag']
    del NewFormData['uid']
    del NewFormData['creator']
    del NewFormData['created']
    del NewFormData['id']
    FormData = NewFormData
    print(json.dumps(FormData, indent=4))

#Submit
Result = Connection.post(
    url = POST_URL,
    data = FormData
)
if Result.status_code != 200:
    print("Failed to submit.", Result.status_code)
    exit()
else: 
    ResultMessage = json.loads(Result.text)
    if ResultMessage['m'] == '操作成功':
        if os.path.exists("form.json"):
            os.rename("form.json", "form.json.bak")
        with open("form.json", "w") as fp:
            fp.write(json.dumps(FormData, indent = 4))
        print("SUBMIT BIG SUCCESS", ResultMessage['m'])
    else:
        print(ResultMessage['m'])
