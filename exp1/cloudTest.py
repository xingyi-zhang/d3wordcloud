import dataclasses
import flask
from flask import Flask, render_template, json
import random
import math
from Configures import config
import csv
import os,sys 

p = os.path.abspath('..')
sys.path.insert(2,p)

from flask_util_js.flask_util_js import FlaskUtilJs

app = Flask(__name__,template_folder = '../exp1/templates')
app.config['WEB_ROOT'] = '/'
# For flask_util.url_for() in JavaScript: https://github.com/dantezhu/flask_util_js
fujs = FlaskUtilJs(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/landing/')
def get_landing_page():
    return render_template('landing.html')

@app.route('/instruction_1/', methods = ['POST'])
def get_instruction_1():
    turker_id = flask.request.form['turker_id']
    order = config.get_order()
    return render_template('instruction_1.html',turker_id = turker_id, order= order, width = config.get_config_env()[2], height = config.get_config_env()[3],)

@app.route('/instruction_2/',methods = ['POST'])
def get_instruction_2():
    turker_id = flask.request.form['turker_id']
    order = json.loads(flask.request.form['order'])
    trial_index = int(flask.request.form['trial_index'])
    return render_template('instruction_2.html',turker_id = turker_id, order = order, trial_index=trial_index)

@app.route('/completion/',methods = ['POST'])
def get_completion():
    turker_id = flask.request.form['turker_id']
    return render_template('completion.html',turker_id = turker_id)

@app.route('/start')
def start_generate():
    return flask.redirect(flask.url_for('buildcloud',trial=0))

@app.route('/stim/',methods = ['POST'])
def get_stim():
    turker_id = flask.request.form['turker_id']
    order = json.loads(flask.request.form['order'])
    trial_index = int(flask.request.form['trial_index'])
    stim_id = order[trial_index]
    with open('./Stim_checked/stim_'+str(stim_id)+'.html', 'r') as f:
        stim_html = f.read()
    return render_template('stim.html', stim_html = stim_html, trial_index = trial_index, stim_id = stim_id, turker_id = turker_id, order = order,config_env = config.get_config_env())

@app.route('/buildcloud/<trial>/')
def buildcloud(trial):
    if int(trial) > 71:
        return 'done'
    # weather to build all cloud, 1 means yes
    buildAll = 0
    return render_template('cloud.html',buildall = buildAll, trial_num = trial, targets = json.dumps(get_target(2,int(trial))), distractors = json.dumps(get_distractor(100)),dis_num = config.get_dis_num(), font_type = config.get_font_type())

@app.route('/post_stim_gen/',methods=['POST'])
def post_stim_gen():
    data = json.loads(flask.request.data)
    stringToSave = '<svg width="512" height="512">' + data['stim'].replace('&quot;', '\'') + '</svg>'
    with open('./Stim/stim_'+str(data['trial'])+'.html', 'w') as f:
        f.write(stringToSave)
    return json.dumps(data)

@app.route('/post_stim/',methods=['POST'])
def post_stim():
    data = json.loads(flask.request.data)
    with open('./Results/pilot.csv','a',newline = '') as f:
        fieldnames = ['turker_id',"stim_id","resp_time","resp"]
        writer = csv.DictWriter(f, fieldnames= fieldnames)
        # writer.writeheader()
        writer.writerow(data)
    return json.dumps(data)

@app.route('/post_demographic/', methods = ['POST'])
def post_demographic():
    data = json.loads(flask.request.data)
    with open('./Demographics/pilot.csv','a',newline = '') as f:
        fieldnames = ['turker_id', 'age', 'gender', 'education', 'device', 'browser', 'difficulty', 'confidence', 'exp_de','exp_cl','comments']
        writer = csv.DictWriter(f, fieldnames= fieldnames)
        # writer.writeheader()
        writer.writerow(data)
        f.write('\n')
    return json.dumps(data)

@app.route('/post_landing/', methods = ['POST'])
def post_landing():
    data = json.loads(flask.request.data)
    print(data)
    # turker_id = flask.request.form
    # print(turker_id)
    return data


def get_targ_config(posi):
    return config.get_target_position(posi)

# the config array is [min,max,mean,sd]
def getGaussian(length_config):
    while True:
        length = random.gauss(length_config[2],length_config[3])
        if (length >length_config[0]) and (length < length_config[1]):
            return math.floor(length)

# generate pronuncible word with given length 
def randShortStr(length):
    word = ""
    cons = ["c","n","c","n","c","n","s","v","x","z"]
    vow = ["a","e","o","u","a","e","o","u"] 
    countVow =0 
    countCon =0

    for i in range(0,length):
        rand = random.random()
        if ((countVow < 2) and (rand < 0.54)) or (countCon > 1):
            newChar = random.choice(vow)
            vow.remove(newChar)
            countCon = 0
            countVow +=1
        else: 
            newChar = random.choice(cons)
            cons.remove(newChar)
            countVow = 0
            countCon +=1
        word=word+newChar
    return word

def get_wordlist():
    wordlist = []
    blacklist =  ['anal', 'anus', 'arrse', 'arse', 'ass', 'asses','assfucker', 'assfukka', 'asshole', 'assholes', 'asswhole','b!tch', 'b00bs','b17ch','b1tch','ballbag','balls','ballsack','bastard','beastial','beastiality','bellend','bestial','bestiality','biatch','bitch','bitcher','bitchers','bitches','bitchin','bitching','bloody','blow job','blowjob','blowjobs','boiolas','bollock','bollok','boner','boob','boobs','booobs','boooobs','booooobs','booooooobs','bras','breasts','buceta','bugger','bum','bunny fucker','butt','butthole','buttmuch','buttocks','buttplug','c0ck','c0cksucker','carpet muncher','cawk','chink','cipa','cl1t','clit','clitoris','clits','cnut','cock','cock-sucker','cockface','cockhead','cockmunch','cockmuncher','cocks','cocksuck','cocksucked','cocksucker','cocksucking','cocksucks','cocksuka','cocksukka','cok','cokmuncher','coksucka','coon','cox','cracker','crap','cum','cummer','cumming','cums','cumshot','cunilingus','cunillingus','cunnilingus','cunt','cuntlick','cuntlicker','cuntlicking','cunts','cyalis','cyberfuc','cyberfuck','cyberfucked','cyberfucker','cyberfuckers','cyberfucking','d1ck','damn','diarrhea','dick','dickhead','dike','dildo','dildos','dink','dinks','dirsa','dlck','dog-fucker','doggin','dogging','donkeyribber','doosh','duche','dyke','ejaculate','ejaculated','ejaculates','ejaculating','ejaculatings','ejaculation','ejakulate','f u c k','f u c k e r','f4nny','fag','fagging','faggitt','faggot','faggs','fagot','fagots','fags','fanny','fannyflaps','fannyfucker','fanyy','fatass','fcuk','fcuker','fcuking','feces','feck','fecker','felching','fellate','fellatio','fingerfuck','fingerfucked','fingerfucker','fingerfuckers','fingerfucking','fingerfucks','fistfuck','fistfucked','fistfucker','fistfuckers','fistfucking','fistfuckings','fistfucks','flange','fook','fooker','fuck','fucka','fucked','fucker','fuckers','fuckhead','fuckheads','fucking','fuckings','fuckingshitmotherfucker','fuckme','fucks','fuckwhit','fuckwit','fudge packer','fudgepacker','fuk','fuker','fukker','fukkin','fuks','fukwhit','fukwit','fux','fux0r','f_u_c_k','gangbang','gangbanged','gangbangs','gaylord','gaysex','goatse','God','god-dam','god-damned','goddamn','goddamned','hardcoresex','hell','heshe','hoar','hoare','hoer','homo','homosexual','homosexuals','hooker','hore','horniest','horny','hotsex','"jack-off','jackoff','jap','jerk-off','jism','jiz','jizm','jizz','kawk','knob','knobead','knobed','knobend','knobhead','knobjocky','knobjokey','kock','kondum','kondums','kum','kummer','kumming','kums','kunilingus','l3i+ch','l3itch','labia','lesbian','lesbians','lesbo','lmfao','lust','lusting','m0f0','m0fo','m45terbate','ma5terb8','ma5terbate','masochist','massacre','master-bate','masterb8','masterbat*','masterbat3','masterbate','masterbation','masterbations','masturbate','mo-fo','mof0','mofo','mothafuck','mothafucka','mothafuckas','mothafuckaz','mothafucked','mothafucker','mothafuckers','mothafuckin','mothafucking','mothafuckings','mothafucks','mother fucker','motherfuck','motherfucked','motherfucker','motherfuckers','motherfuckin','motherfucking','motherfuckings','motherfuckka','motherfucks','muff','mutha','muthafecker','muthafuckker','muther','mutherfucker','n1gga','n1gger','nazi','nigg3r','nigg4h','nigga','niggah','niggas','niggaz','nigger','niggers','nob','nob jokey','nobhead','nobjocky','nobjokey','numbnuts','nutsack','orgasim','orgasims','orgasm','orgasms','p0rn','pawn','pecker','penis','penisfucker','phonesex','phuck','phuk','phuked','phuking','phukked','phukking','phuks','phuq','pigfucker','pimpis','piss','pissed','pisser','pissers','pisses','pissflaps','pissin','pissing','pissoff','playboy','poop','porn','porno','pornography','pornos','prick','pricks','pron','pube','pusse','pussi','pussies','pussy','pussys','rape','raper','rapist','rectum','retard','rimjaw','rimming','s hit','s.o.b.','sadist','schlong','screwing','scroat','scrote','scrotum','semen','sensual','sensuous','sex','sexes','"sh!+"','"sh!t"','sh1t','shag','shagger','shaggin','shagging','shemale','"shi+"','shit','shitdick','shite','shited','shitey','shitfuck','shitfull','shithead','shiting','shitings','shits','shitted','shitter','"shitters "','shitting','shittings','"shitty "','skank','slut','sluts','smegma','smut','snatch','"son-of-a-bitch"','spac','spunk','s_h_i_t','t1tt1e5','t1tties','teets','teez','testical','testicle','tit','titfuck','tits','titt','tittie5','tittiefucker','titties','tittyfuck','tittywank','titwank','tosser','turd','tw4t','twat','twathead','twatty','twunt','twunter','urinary','urine','uterus','v14gra','v1gra','vagina','vaginal','viagra','vulva','w00se','wang','wank','wanker','wanky','weiner','whoar','whore','whores','willies','willy','xrated','xxx','FALSE','corpses','corpse','bodies','auschwitz']
    i = 0
    while i<10000:
        word = randShortStr(getGaussian([3,10,6,2]))
        if (not (word in wordlist)) and (not (word in blacklist)):
            wordlist.append(word)
            i = i +1
    return wordlist

def get_dis_list(num):
    dis_list = []
    i  = 0
    while i < num : 
        word = random.choice(wordlist)
        if (not (word in dis_list)):
            dis_list.append(word)
            i += 1
    return dis_list

def get_distractor(num):
    dis_list = get_dis_list(num)
    distractor_list = []
    dis_fill = config.get_dis_fill()
    size_config = config.get_dis_size_config()
    for i in range(0,num):
        distractor_list.append({'text': dis_list[i],'size':getGaussian(size_config),'fill': dis_fill,'class':'distractor'})
    return distractor_list

# num: number of target words
def get_target(num,trial):
    target_list = []
    targ_size = config.get_targ_size(trial)
    posi = random.randint(1,4)
    targ_posi = config.get_target_position(posi)
    targ_length = config.get_targ_length(trial)
    for i in range(0,num):
        targ_text = randShortStr(targ_length[i])
        # check for conflict with existing wordlist, need to update for only check distractor wordlist
        while (targ_text in wordlist):
            targ_text = randShortStr(targ_length[i])
        target_list.append({'text': targ_text, 'size': targ_size[i], 'fill':'black', 'x': targ_posi[i]['x'], 'y':targ_posi[i]['y'], 'rotate': 0,'id':'target'+str(i),'class':'target'})
    return target_list



if __name__=='__main__':
    wordlist = get_wordlist()
    # with app.app_context():
    #     position = json.dumps(get_target(2))
    #     print(position)

    app.run(debug=True)