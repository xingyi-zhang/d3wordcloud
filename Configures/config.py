distratcor_num = 80
distractor_fill = "#bdbdbd"
dis_size_config = [10,40,20,18]
target_size = [20,23]
target_text = ['test_1','test_2222']
font_type = "Times New Roman"

import math
import random 

#  return the randomly generated position of targets with given postion coding in the board
def get_target_position(posi):
    x1 = random.randint(50,150)
    y1 = random.randint(50,150)
    x2 = random.randint(50,150)
    y2 = math.floor(math.sqrt(300 **2 - (x1+x2)**2) - y1)

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

def get_targ_text():
    return target_text

def get_dis_fill():
    return distractor_fill

def get_targ_size():
    return target_size

def get_font_type():
    return font_type

def get_dis_num():
    return distratcor_num