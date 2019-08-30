import smbus2
import bme280
appid = "4574f3776299fa2b73a2d24cb8f27caa"
import requests
import GLOBAL as v
import mh_z19

address = 0x76
bus = smbus2.SMBus(1)


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#      measure temp,pressure, humidity and CO2                   #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_temp():
    data = bme280.sample(bus, address)
    variable_with_temp= data.temperature
    v.temp = float('{:05.2f}'.format(variable_with_temp))

def get_pressure():
    data = bme280.sample(bus, address)
    variable_with_pressure = data.pressure*0.750064
    v.preassure = float('{:05.2f}'.format(variable_with_pressure))
    

def get_humidity():
    data = bme280.sample(bus, address)
    variable_with_humidity= data.humidity
    v.humidity = float('{:05.2f}'.format(variable_with_humidity))     


def work_mh_z19():
    v.ppm = mh_z19.read()
    print(v.ppm)
    if len(v.CO2_BASE) == 60:
        v.CO2_BASE.pop(0)
    v.CO2_BASE.append(v.ppm["co2"])
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#                        Request Weather                         #
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_data_from_request():   
        data = get_update_request()
        v.temp_i = data['main']['temp']
        v.humidity_i = data['main']['humidity']
        v.preassure_i = data["main"]['pressure']*0.750064
        temps = data['weather'][0]
        v.status = temps['description']


def get_update_request():   
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'id': v.city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        return data
    except Exception as e:
        print("Exception (weather):", e)
        pass


