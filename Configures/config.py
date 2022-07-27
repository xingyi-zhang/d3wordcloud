import math
import random 
import csv

def get_Config():
    configures = [] 
    with open('./Configures/config_e1.csv', 'r', newline='') as configFile:
        reader = csv.reader(configFile,delimiter=',')
        heading = next(reader) 
        for row in reader:
            this_task = {}
            for i in range(1,4):
                    this_task[heading[i]] = int(row[i])
            configures.append(this_task)
    return configures

# def get_Config():
#     configures = [] 
#     with open('./Configures/config_e1.csv', 'r', newline='') as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             configures.append(row)
#     return configures

distratcor_num = 60
distractor_fill = "#bdbdbd"
dis_size_config = [10,40,20,18]
font_type = "Times New Roman"
# note configures are zero-indexed
configures = get_Config() 

#  return the randomly generated position of targets with given postion coding in the board
# for the larger word:  0:upper left   1:upper right    2:lower left  3:lower right
# the smaller word is just on the opposite quadrant to the larger word
def get_target_position(posi):
    x1 = random.randint(50,125)
    y1 = random.randint(50,125)
    x2 = random.randint(50,125)
    y2 = math.floor(math.sqrt(250 **2 - (x1+x2)**2) - y1)

    if posi == 0:
        x1 = -x1
        y1 = -y1
    elif posi ==1:
        y1 = -y1
        x2 = -x2
    elif posi ==2: 
        x1 = -x1
        y2 = -y2
    else:
        x2 = -x2
        y2 = -y2 

    return [{'x': x1+256, 'y': y1+256},{'x': x2+256, 'y': y2+235}]

def get_dis_size_config():
     return dis_size_config

def get_targ_length(trial):
    return [configures[trial]['big_length'],configures[trial]['small_length']]

def get_dis_fill():
    return distractor_fill

def get_targ_size(trial):
    return [configures[trial]['big_size'],configures[trial]['big_size']-1]

def get_font_type():
    return font_type

def get_dis_num():
    return distratcor_num