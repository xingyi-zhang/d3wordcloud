import flask
from flask import Flask, render_template, json
import random
import math
from Configures import config
import csv

from flask_util_js import FlaskUtilJs

app = Flask(__name__)
app.debug = True
app.config['WEB_ROOT'] = '/'
# For flask_util.url_for() in JavaScript: https://github.com/dantezhu/flask_util_js
fujs = FlaskUtilJs(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/buildcloud/<trial>/')
def buildcloud(trial):
    if int(trial) > 76:
        return 'done'
    # weather to build all cloud, 1 means yes
    buildAll = 1
    return render_template('cloud.html',buildall = buildAll, trial_num = trial, size = config.get_size(),words = json.dumps(get_words(int(trial))),font_type = config.get_font_type())

@app.route('/landing/')
def get_landing_page():
    return render_template('landing.html')

@app.route('/instruction_1/', methods = ['POST'])
def get_instruction_1():
    turker_id = flask.request.form['turker_id']
    order = config.get_order()
    return render_template('instruction_1.html',turker_id = turker_id, order= order, width = config.get_size()[0], height = config.get_size()[1],)

@app.route('/instruction_2/',methods = ['POST'])
def get_instruction_2():
    turker_id = flask.request.form['turker_id']
    order = json.loads(flask.request.form['order'])
    trial_index = int(flask.request.form['trial_index'])
    return render_template('instruction_2.html',turker_id = turker_id, order = order, trial_index=trial_index)

# group indicate whether show a english word or nonword. 1 being nonword and 0 being word
@app.route('/stim/',methods = ['POST'])
def get_stim():
    turker_id = flask.request.form['turker_id']
    order = json.loads(flask.request.form['order'])
    trial_index = int(flask.request.form['trial_index'])
    stim_id = order[trial_index]
    group = (stim_id-order[0])&1
    target = get_target(stim_id, group)
    with open('./Stim_checked/stim_'+str(stim_id)+'.html', 'r') as f:
        stim_html = f.read()
    return render_template('stim.html',group = group, display_time = config.get_display_time(stim_id), target = target, stim_html = stim_html, trial_index = trial_index, stim_id = stim_id, turker_id = turker_id, order = order,config_env = config.get_config_env())

@app.route('/completion/',methods = ['POST'])
def get_completion():
    turker_id = flask.request.form['turker_id']
    hash_code = hash(turker_id + 'Carleton')
    return render_template('completion.html',turker_id = turker_id, hash_code = hash_code)

@app.route('/post_stim_gen/',methods=['POST'])
def post_stim_gen():
    data = json.loads(flask.request.data)
    stringToSave = '<svg width="400" height="400">' + data['stim'].replace('&quot;', '\'') + '</svg>'
    with open('./Stim/stim_'+str(data['trial'])+'.html', 'w') as f:
        f.write(stringToSave)
    return json.dumps(data)

def get_prime(trial,num):
    pri_list = target_dict[trial]["cues"].copy()
    prime_list = []
    for i in range(0,num):
        cue = random.choice(pri_list)
        prime_list.append({'text':cue,'size':23,'fill': 'black', 'class':'p'})
        pri_list.remove(cue)
    return prime_list

def get_target(stim_id,flag):
    return config.get_target(stim_id,flag)

# find words in the all cues that are not related with the target
def get_distractor(trial,num):
    distractor_list = []
    dis_list = []
    pri_list = target_dict[trial]["cues"]
    all_cue = cue_dict[trial]["cues"]
    for i in range(0,num):
        dis = random.choice(whole_dict)
        while ((dis in all_cue) or (dis in dis_list)):
            dis = random.choice(whole_dict)
        dis_list.append(dis)
        distractor_list.append({'text': dis,'size':23,'fill': "black",'class':'np'})
    return distractor_list

@app.route('/post_stim/',methods=['POST'])
def post_stim():
    data = json.loads(flask.request.data)
    with open('./Results/pilot.csv','a',newline = '') as f:
        fieldnames = ['turker_id',"stim_id","resp_time","resp","group"]
        writer = csv.DictWriter(f, fieldnames= fieldnames)
        #writer.writeheader()
        writer.writerow(data)
    return json.dumps(data)

@app.route('/post_demographic/', methods = ['POST'])
def post_demographic():
    data = json.loads(flask.request.data) 
    with open('./Demographics/pilot.csv','a',newline = '') as f:
        fieldnames = ['turker_id', 'age', 'gender', 'education', 'language','device', 'browser', 'difficulty', 'confidence', 'exp_de','exp_cl','comments']
        writer = csv.DictWriter(f, fieldnames= fieldnames)
        writer.writeheader()
        writer.writerow(data)
        f.write('\n')
    return json.dumps(data)

@app.route('/post_landing/', methods = ['POST'])
def post_landing():
    data = json.loads(flask.request.data)
    return json.dumps(data)

def get_words(trial):
    words = []
    #  actual ratio = 1/3 * ratio 
    ratio = config.get_config_ratio(trial)
    primes = get_prime(trial,10*ratio)
    distractors = get_distractor(trial,30-10*ratio)
    avail = primes + distractors
    for i in range(0,30):
        word = random.choice(avail)
        words.append(word)
        avail.remove(word)
    return words

if __name__=='__main__':
    target_dict = config.get_dict()
    whole_dict = config.get_whole_dict()
    cue_dict = config.get_cue_dict()
    # print(len(cue_dict))
    # config.get_target_dict()
    app.run(debug=True)