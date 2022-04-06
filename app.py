import requests, math
from datetime import datetime
import keys, dbms
db = dbms.dbInfo

# print(key.keys['Encode'])
# http://apis.data.go.kr/1360000/TourStnInfoService/getTourStnVilageFcst?serviceKey=인증키(URL Encode)&numOfRows=10&pageNo=1&CURRENT_DATE=2016121010&HOUR=24&COURSE_ID=1
site = 'http://apis.data.go.kr/1360000/TourStnInfoService/getTourStnVilageFcst'
key = keys.keys['Encode']
nOR = '1000'
pageNo = '1'
dataType = 'json'
CURRENT_DATE = datetime.now().strftime("%Y%m%d") + '00'
HOUR = '24'
COURSE_ID = '1'

str = site + '?serviceKey=' + key + '&numOfRows=' + nOR + '&pageNo=' + pageNo + '&dataType=' + dataType + '&CURRENT_DATE=' + CURRENT_DATE + '&HOUR='+HOUR+'&COURSE_ID=' + COURSE_ID

response = requests.get(str)
response = response.json()['response']
# for문 max값
# print(math.ceil(response.json()['response']['body']['totalCount']/int(nOR)))
totalCount = response['body']['totalCount']
print("totalCount :", totalCount, type(totalCount))
print("ResultCode : " + response['header']['resultCode'], type(response['header']['resultCode']))

itemList = response['body']['items']['item']
cursor = db.cursor(dbms.pymysql.cursors.DictCursor)

# for item in itemList:
#     sql = "insert into TourStnInfoService values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#     cursor.execute(sql, (item['tm'], item['thema'], item['courseId'], item['courseAreaId'], item['courseAreaName'], item['courseName'], item['spotAreaId'], item['spotAreaName'], item['spotName'], item['th3'], item['wd'], item['ws'], item['sky'], item['rhm'], item['pop']))
#     db.commit()
    
# 데이터 조회 
# select_sql = "select * from TourStnInfoService"
# cursor.execute(select_sql)
# result = cursor.fetchall()
# print(result)

db.close()
