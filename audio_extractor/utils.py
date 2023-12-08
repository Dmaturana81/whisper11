from fastcore.all import *
from datetime import datetime

def str2path(file):
    return file if isinstance(file, Path) else Path(file)

def time2msec(time:str):
    pt = datetime.strptime(time,'%H:%M:%S' )
    return (pt.hour * 3600 + pt.minute * 60 + pt.second) * 1000

def loadtsfile(file):
    file = str2path(file)
    with open(file,'r') as infile:
        ts = infile.readlines()
    tss = [x.strip('\n').split('\t')[0:3] for x in ts if len(x.split('\t'))>1]
    return [{'speaker':x[0], 'start':x[1], 'end':x[2]} for x in tss]

def to_snake_case(name):
    return name.lower().replace(" ", "_").replace(":", "_").replace("__", "_")