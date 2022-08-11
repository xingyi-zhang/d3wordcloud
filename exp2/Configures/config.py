import csv
import random

# get a target - 20 cues dictionary 
def get_dict():
    target_dict = []
    raw_dict = []
    with open('./Configures/target_dict.csv', 'r', newline='') as f:
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            raw_dict.append([row[0],row[1]])
    word = raw_dict[0][0]
    current = []
    for i in range(0,len(raw_dict)):
        if raw_dict[i][0] == word:
            current.append(raw_dict[i][1])
        else: 
            target_dict.append({'target':word, 'cues':current})
            current = [raw_dict[i][1]]
            word = raw_dict[i][0]
    target_dict.append({'target':word, 'cues':current})
    return target_dict

# Read in all the target and find corresponding nonwords with the same length 
# Only need to execute once when a new target dictionary is generated
def get_target_dict():
    nonword = []
    target = []
    target_all = []
    with open('./Configures/nonword.txt','r') as f:
        rawnonword = f.read().split('\n')
    for i in rawnonword:
        if ((len(i) >5) and (len(i)<11)):
            nonword.append(i)
    with open('./Configures/targets.csv', 'r', newline='') as f:
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            target.append(row[0])
    for i in target:
        nw = random.choice(nonword).upper()
        while (len(nw)!= len(i)):
            nw = random.choice(nonword).upper()
        target_all.append([i,nw])
    with open('./Configures/all_targets.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(target_all)
    return True

# return a dictionary with targets & all their cues 
def get_whole_dict():
    whole_dict = []
    with open('./Configures/all_cues.csv', 'r', newline='') as f:
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            whole_dict.append(row[1])
    return whole_dict

# find all the words appear as cues
# will serves to be the list where distractors come from
def get_cue_dict():
    cue_dict = []
    raw_dict = []
    with open('./Configures/all_cues.csv', 'r', newline='') as f:
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            raw_dict.append([row[0],row[1]])
    word = raw_dict[0][0]
    current = []
    for i in range(0,len(raw_dict)):
        if raw_dict[i][0] == word:
            current.append(raw_dict[i][1])
        else: 
            cue_dict.append({'target':word, 'cues':current})
            current = [raw_dict[i][1]]
            word = raw_dict[i][0]
    cue_dict.append({'target':word, 'cues':current})
    return cue_dict

def get_config():
    configures = [] 
    with open('./Configures/config_e2.csv', 'r', newline='') as configFile:
        reader = csv.reader(configFile,delimiter=',')
        heading = next(reader) 
        for row in reader:
            this_task = {}
            for i in range(1,3):
                    this_task[heading[i]] = int(row[i])
            configures.append(this_task)
    return configures

def get_target(stim_id,flag):
    raw_dict = []
    with open('./Configures/all_targets.csv', 'r', newline='') as f:
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            raw_dict.append([row[0],row[1]])
    return raw_dict[stim_id][flag]

configures = get_config() 

def get_config_ratio(stim_id):
    return configures[stim_id]["ratio"]

def get_display_time(stim_id):
    return int(configures[stim_id]["time"])

font_type = "Times New Roman"
svg_width = 400
svg_height = 400
trial_num = 72
prac_num = 5 

def get_font_type():
    return font_type

def get_size():
    return [svg_width,svg_height]

# generate the order in which the stimuli will be presented
# the first five is practice trial
def get_order():
    order = list(range(0,prac_num))
    avail =  list(range(prac_num,trial_num+prac_num))
    for i in range(0,trial_num):
        x = random.choice(avail)
        order.append(x)
        avail.remove(x)
    return order

def get_config_env():
    return [prac_num,trial_num+prac_num]