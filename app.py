import requests, math
from datetime import datetime
import keys, dbms

site = 'http://apis.data.go.kr/1360000/TourStnInfoService/getTourStnVilageFcst'
key = keys.keys['Encode']
nOR = 1000
pageNo = 1
dataType = 'json'
CURRENT_DATE = datetime.now().strftime("%Y%m%d") + '00'
HOUR = 96
COURSE_ID = 1
No_Data_Count = 0
sum = 0

db = dbms.dbInfo
# f = open("log.txt", "w+")
# f.close()
while True:
    try:
        f = open("log.txt", "a+")
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"\n")
        if No_Data_Count>10:
            break
        msg = f"{site}?serviceKey={key}&numOfRows={nOR}&pageNo={pageNo}&dataType={dataType}&CURRENT_DATE={CURRENT_DATE}&HOUR={HOUR}&COURSE_ID={COURSE_ID}"
        # f.write(msg+"\n")
        response = requests.get(msg)
        response = response.json()['response']
        if response['header']['resultCode'] == '03':
            f.write("No_Data"+"\n")
            No_Data_Count += 1
        elif response['header']['resultCode'] == '02':
            COURSE_ID -= 1
            f.write("DB_Error"+"\n")
        elif response['header']['resultCode'] == '00':
            No_Data_Count = 0
            totalCount = response['body']['totalCount']
            f.write("totalCount : "+ str(totalCount)+"\n")
            print("totalCount : "+ str(totalCount))
            sum += totalCount
            
            if totalCount > nOR:
                msg = f"{site}?serviceKey={key}&numOfRows={totalCount}&pageNo={pageNo}&dataType={dataType}&CURRENT_DATE={CURRENT_DATE}&HOUR={HOUR}&COURSE_ID={COURSE_ID}"
                response = requests.get(msg)
                # f.write(response.text+"\n")
                response = response.json()['response']
            f.write(msg+"\n")
            # print(msg)
            itemList = response['body']['items']['item']
            cursor = db.cursor(dbms.pymysql.cursors.DictCursor)
            # print(itemList)

            for item in itemList:
                select_sql = """select * from TourStnInfoService where tm = %s and thema = %s and courseId = %s and courseAreaId = %s and courseAreaName = %s and courseName = %s and spotAreaId = %s and spotAreaName = %s and spotName = %s and th3 = %s and wd = %s and ws = %s and sky = %s and rhm = %s and pop = %s"""
                cursor.execute(select_sql, (item['tm'], item['thema'], item['courseId'], item['courseAreaId'], item['courseAreaName'], item['courseName'], item['spotAreaId'], item['spotAreaName'], item['spotName'], item['th3'], item['wd'], item['ws'], item['sky'], item['rhm'], item['pop']))
                count = cursor.rowcount
                if count == 0:
                    sql = """insert into TourStnInfoService values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql, (item['tm'], item['thema'], item['courseId'], item['courseAreaId'], item['courseAreaName'], item['courseName'], item['spotAreaId'], item['spotAreaName'], item['spotName'], item['th3'], item['wd'], item['ws'], item['sky'], item['rhm'], item['pop'], datetime.now()))
                else:
                    break;
            db.commit()
            cursor.close()
        else:
            f.write(response.text+"\n")
            break
    except Exception as e:
        print(e)
        f.write(str(e))
    finally:
        COURSE_ID+=1
        f.close()
db.close()
print(sum)
# 데이터 조회 
# select_sql = "select * from TourStnInfoService"
# cursor.execute(select_sql)
# result = cursor.fetchall()
# print(result)
