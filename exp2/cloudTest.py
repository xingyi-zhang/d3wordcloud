import flask
from flask import Flask, render_template, json
import random
import math
from Configures import config
import csv
import sys
try:
    import psycopg2
    from psycopg2 import sql
except Exception as e:
    print(e, file=sys.stderr)
tid_database = 'wc22_e2_tid'
results_database = 'wc22_e2a_results'
demographics_database = 'wc22_e2a_dem'

from flask_util_js import FlaskUtilJs

app = Flask(__name__)
app.config['WEB_ROOT'] = '/'
# For flask_util.url_for() in JavaScript: https://github.com/dantezhu/flask_util_js
fujs = FlaskUtilJs(app)

def get_connection():
    connection = None
    try:
        connection = psycopg2.connect(host='localhost',database='fontsize',user='fontsize',password='wordcloudsbad?')
    except Exception as e:
        print(e, file=sys.stderr)
    return connection

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/buildcloud/<trial>/')
def buildcloud(trial):
    if int(trial) > 94:
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
    group = (stim_id-order[5])&1
    target = get_target(stim_id, group)
    with open('./Stim_checked/stim_'+str(stim_id)+'.html', 'r') as f:
        stim_html = f.read()
    return render_template('stim.html',group = group, display_time = config.get_display_time(stim_id), target = target, stim_html = stim_html, trial_index = trial_index, stim_id = stim_id, turker_id = turker_id, order = order,config_env = config.get_config_env())

@app.route('/completion/',methods = ['POST'])
def get_completion():
    turker_id = flask.request.form['turker_id']
    hash_code = hash(turker_id + 'Carleton')
    return render_template('completion.html',turker_id = turker_id, hash_code = hash_code)

# generate the svg image
@app.route('/post_stim_gen/',methods=['POST'])
def post_stim_gen():
    data = json.loads(flask.request.data)
    stringToSave = '<svg width="400" height="400">' + data['stim'].replace('&quot;', '\'') + '</svg>'
    with open('./Stim/stim_'+str(data['trial'])+'.html', 'w') as f:
        f.write(stringToSave)
    return json.dumps(data)

def get_prime(trial,num):
    pri_list = target_dict[trial]["cues"].copy()
    if num ==1:
        return [{'text':pri_list[0],'size':23,'fill': 'black','id':'central'}]
    prime_list = []
    for i in range(1,num+1):
        prime_list.append({'text':pri_list[i],'size':23,'fill': 'black'})
    return prime_list

# get the target
# flag = 1: non word; flag = 0: English word
def get_target(stim_id,flag):
    return config.get_target(stim_id,flag)

# find words in the all cues that are not related with the target
def get_distractor(trial,num):
    distractor_list = []
    dis_list = []
    pri_list = target_dict[trial]["cues"]
    all_cue = cue_dict[trial]["cues"]
    if num ==1:
        dis = random.choice(whole_dict)
        while ((dis in all_cue) or (dis in dis_list)):
            dis = random.choice(whole_dict)
        return [{'text':dis,'size':23,'fill': 'black','id':'central'}]
    for i in range(0,num):
        dis = random.choice(whole_dict)
        while ((dis in all_cue) or (dis in dis_list)):
            dis = random.choice(whole_dict)
        dis_list.append(dis)
        distractor_list.append({'text': dis,'size':23,'fill': "black"})
    return distractor_list

# record the data after each trial into database or csv
@app.route('/post_stim/',methods=['POST'])
def post_stim():
    data = json.loads(flask.request.data)
    turker_id = data["turker_id"]
    stim_id = int(data["stim_id"])
    resp_time = float(data["resp_time"])
    resp = int(data["resp"])
    group = int(data["group"])
    correct = int(data["correct"])
    trial_index = int(data["trial_index"])
    display_time = int(data["display_time"])
    ratio = int(data["ratio"])
    if not app.debug:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql.SQL(""" INSERT INTO {} (turker_id,stim_id,resp_time,resp,nonword,correct,trial_index,display_time,ratio)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);""").format(sql.Identifier(results_database)),(turker_id,stim_id,resp_time,resp,group,correct,trial_index,display_time,ratio))
        connection.commit()
        cursor.close()
        connection.close()
    else:
        with open('./Results/pilot.csv','a',newline = '') as f:
            fieldnames = ['turker_id',"stim_id","resp_time","resp","group","correct","trial_index","display_time","ratio"]
            writer = csv.DictWriter(f, fieldnames= fieldnames)
            # writer.writeheader()
            writer.writerow(data)
    return json.dumps(data)

# record the demographic data into database or csv
@app.route('/post_demographic/', methods = ['POST'])
def post_demographic():
    data = json.loads(flask.request.data) 
    turker_id = data["turker_id"]
    age = data["age"]
    gender = data["gender"]
    education = int(data["education"])
    language = int(data["language"])
    device = int(data["device"])
    browser = int(data["browser"])
    difficulty = int(data["difficulty"])
    confidence = int(data["confidence"])
    exp_de = int(data["exp_de"])
    exp_cl = int(data["exp_cl"])
    zoom = float(data["zoom"])
    user_agent = data["user_agent"]
    device_type =  data["device_type"]
    comments = data["comments"]
    if not app.debug:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql.SQL(""" INSERT INTO {} (turker_id,age, gender,education,language,device,browser,difficulty, confidence,exp_de,exp_cl,zoom,user_agent,device_type,comments) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""").format(sql.Identifier(demographics_database)),(turker_id,age, gender,education,language,device,browser,difficulty, confidence,exp_de,exp_cl,zoom,user_agent,device_type,comments))
        connection.commit()
        cursor.close()
        connection.close()
    else:
        with open('./Demographics/pilot.csv','a',newline = '') as f:
            fieldnames = ['turker_id', 'age', 'gender', 'education', 'language','device', 'browser', 'difficulty', 'confidence', 'exp_de','exp_cl','zoom','user_agent','device_type','comments']
            writer = csv.DictWriter(f, fieldnames= fieldnames)
            # writer.writeheader()
            writer.writerow(data)
            f.write('\n')
    return json.dumps(data)

# check if the participant has participanted in our experiment, if not, allow them to move on
@app.route('/post_landing/', methods = ['POST'])
def post_landing():
    flag = "1"
    data = json.loads(flask.request.data)
    turker_id = data["turker_id"]
    if not app.debug:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql.SQL("SELECT turker_id FROM {} WHERE turker_id = %s").format(sql.Identifier(tid_database)),(turker_id,))
        if len(cursor.fetchall()) == 0:
            cursor.execute(sql.SQL("INSERT INTO {} (turker_id) VALUES (%s)").format(sql.Identifier(tid_database)),(turker_id,))
        else:
            flag = "-1"
        connection.commit()
        cursor.close()
        connection.close()
    return flag

# get words that will be used in word cloud
# actual ratio = 1/3 * ratio 
def get_words(trial):
    # sur is whether the surrounding words are primes. 1 being primes, 0 being none, and -1 being distractors 
    # cen is whetehr the center word is prime. 1 being primes, 0 being not.
    sur = config.get_config_sur(trial)
    cen = config.get_config_cen(trial)
    if cen == 1:
        words = get_prime(trial,1)
    else:
        words = get_distractor(trial,1)
    if sur == 1:
        surrounding = get_prime(trial,24)
    elif sur == -1:
        surrounding = get_distractor(trial,24)
    else:
        surrounding = []
    return words+surrounding

if __name__=='__main__':
    target_dict = config.get_target_dict()
    whole_dict = config.get_whole_dict()
    cue_dict = config.get_cue_dict()
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]))
        print('  Example: {0} allen.mathcs.carleton.edu xxxx'.format(sys.argv[0]))
        exit()
    host = sys.argv[1]
    port = int(sys.argv[2])
    app.run(host=host, port=port, debug=True)