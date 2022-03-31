import requests, json, os, re, form
from time import sleep
from random import randint

LOGIN_URL = "https://app.bupt.edu.cn/uc/wap/login/check"
GET_URL = 'https://app.bupt.edu.cn/xisuncov/wap/open-report/index'
OLDFORM_URL = 'https://app.bupt.edu.cn/ncov/wap/default/index'
POST_URL = 'https://app.bupt.edu.cn/xisuncov/wap/open-report/save'
__timeout = 3.0
__uname = os.environ['BUPT_USERNAME']
__upswd = os.environ['BUPT_PASSWORD']

FormData = form.FormItems

Connection = requests.session()

#Login
Response = Connection.post(
    url = LOGIN_URL,
    data = {'username': __uname, 'password': __upswd},
    timeout = __timeout
)
if Response.status_code != 200:
    print("Failed to login. Check your username and password.", Response.status_code)
    exit()
else:
    print("Successfully logged in.")
    print(Response.text)

#OldForm
Response = Connection.post(
    url = "https://app.bupt.edu.cn/a_bupt/api/sso/cas?redirect=https%3A%2F%2Fapp.bupt.edu.cn%2Fncov%2Fwap%2Fdefault%2Findex&from=wap",
    allow_redirects=True
)
sleep(randint(1000, 2000)/1000)

if Response.status_code != 200:
    print("Failed to get old form data.", Response.status_code)
    exit()
else:
    if Response.history:
        print(Response.history)
        for item in Response.history:
            print(item.status_code, item.url)
        print("End of urls.")
        print(Response.history[0].text)
    OldForm = re.search(r'oldInfo: \{.+\}', Response.text)
    if OldForm is not None:
        OldForm = json.loads(OldForm.group(0).split(': ')[1])
    else:
        print("Failed to get old submit context.")
        exit()
    for key in FormData:
        if key in OldForm:
            FormData[key] = OldForm[key]

#Get
Response = Connection.post(
    url = GET_URL
)
if Response.status_code != 200:
    print("Failed to get form data.", Response.status_code)
    exit()
else:
    NewFormData = json.loads(Response.text)
    NewFormData = NewFormData['d']['info']
    for key in FormData:
        if FormData[key] == "" and key in NewFormData:
            FormData[key] = NewFormData[key]
    for key in form.NewFormItems:
        FormData[key] = NewFormData[key]

    if FormData['province'] in ['北京市', '天津市', '上海市', '重庆市']:
        FormData['city'] = FormData['province']
    if(FormData['geo_api_info'] == ''):
        print("昨日填报信息为空.请先手动填报一次.")
        exit()

#Submit
Response = Connection.post(
    url = POST_URL,
    data = FormData
)
if Response.status_code != 200:
    print("Failed to submit.", Response.status_code)
    exit()
else: 
    # 如果想查看自己的位置信息等,请去掉71行注释符号
    # print(json.dumps(FormData, indent=4))
    ResponseMessage = json.loads(Response.text)
    if ResponseMessage['m'] == '操作成功':
        print("Successfully submitted.", ResponseMessage['m'])
    else:
        print(ResponseMessage['m'])
