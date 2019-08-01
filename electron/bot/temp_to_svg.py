import csv, pygal , os.path , os
from pygal.style import TurquoiseStyle
from mongodbcm import get_last
import GLOBAL as v
from time import sleep,time
def generate_day_png(name,paths):
    archive  = get_last(144,name)
    chart = pygal.Line(style=TurquoiseStyle)
    chart.add(name,archive)
    chart.render_to_png(paths)
    #print("png is ready")

def generate_co2(name,paths):
    #start = time()
    chart = pygal.Line(style=TurquoiseStyle)
    chart.add(name,v.CO2_BASE)
    chart.render_to_png(paths)
    #print("Process took: {:.2f} seconds".format(time() - start))

