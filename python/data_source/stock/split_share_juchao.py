import json
import urllib
import requests
import datetime

"""
Get the stocks according to the code


"""



####用于获取token
def gettoken(client_id,client_secret):
    url='http://webapi.cninfo.com.cn/api-cloud-platform/oauth2/token'
    post_data="grant_type=client_credentials&client_id=%s&client_secret=%s"%(client_id,client_secret)
    post_data={"grant_type":"client_credentials",
               "client_id":client_id,
               "client_secret":client_secret
               }
    req = requests.post(url, data=post_data)
    tokendic = json.loads(req.text)
    return tokendic['access_token']

####用于解析接口返回内容
def getPage(url):
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')

param = "&scode=000002,000003"

token = gettoken('I1qrKDSzMTV8Iqm9vKomdXVJ7As3yeD0','raA6BEZoYZ9KrmVu0AJ4QXbDJUDUi0oD') ##请在平台注册后并填入个人中心-我的凭证中的Access Key，Access Secret
url = 'http://webapi.cninfo.com.cn/api/stock/p_stock2406?subtype=002&access_token='+token + param
print(url)
result = json.loads(getPage(url))
import pprint 
pprint.pprint(result['records'])
for i in range(len(result['records'])):
    print (result['records'][i]['PARENTCODE'],result['records'][i]['SORTCODE'],result['records'][i]['SORTNAME'],result['records'][i]['F002V'])

if __name__ == "__main__":
