import schedule
from time import localtime,strftime
from measure import *
import GLOBAL as v
from pymongo import MongoClient
client = MongoClient(v.LOCALHOST, 27017)
db = client["bot_local"]
posts = db.archive

def add_to_base():
        Y = strftime("%d.%m.%Y", localtime())
        v.time = strftime("%H:%M", localtime())   
        post = {"date": Y, "time": v.time,"temp" : v.temp, "temp_i" : v.temp_i, "preassure_i" : v.preassure_i, "preassure": v.preassure, "humidity" : v.humidity, "humidity_i" : v.humidity_i, "CO2" : v.CO2_BASE[-1] }
        print(post)
        try:
            posts.insert_one(post)
        except:
            print("error")


def defa():
    work_mh_z19()    
    get_temp()    
    get_pressure()    
    get_humidity()    
    get_data_from_request()
    v.time = strftime("%H:%M", localtime())


def work_minut():
    defa()
    work_mh_z19()

schedule.every(1).minutes.do(work_minut)
schedule.every(1).minutes.do(add_to_base)


if __name__ == '__main__':
    defa()
    while True:
        schedule.run_pending()




def get_last(num,name):
    global posts
    six_press = []    
    print("Now I here")
    print(name)
    for x in posts.find({},{ "_id": 0, name: 1}):
        try:
            six_press.append(x[name])            
        except KeyError:
            continue
    six = six_press[-num:]
    print("archive send")
    return six


#from temp_to_svg import generate_day_png
# def work_hour():
#     n = "temp" 
#     paths = "img/" + n + ".png"
#     generate_day_png(n,paths)
#     n = "humidity" 
#     paths = "img/" + n + ".png"
#     generate_day_png(n,paths) 
