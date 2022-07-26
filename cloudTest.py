import dataclasses
import flask
from flask import Flask, render_template, json
import random
import math
from Configures import config
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/testText/')
def test_text():
    return 'Testing 1 2 4. "Three sir!" 3!'

@app.route('/start')
def start_generate():
    return flask.redirect(flask.url_for('cloud',trial=1))

@app.route('/cloud/<trial>/')
def cloud(trial):
    if int(trial) > 71:
        return 'done'
    return render_template('cloud.html',trial_num = trial, targets = json.dumps(get_target(2,int(trial))), distractors = json.dumps(get_distractor(100)),dis_num = config.get_dis_num(), font_type = config.get_font_type())

@app.route('/post_stim',methods=['POST'])
def post_data_multi():
    data = json.loads(flask.request.data)
    stringToSave = '<svg width="512" height="512">' + data['stim'].replace('&quot;', '\'') + '</svg>'
    with open('./Stim/stim_'+str(data['trial'])+'.html', 'w') as f:
        f.write(stringToSave)
    return json.dumps(data)

def get_targ_config(posi):
    return config.get_target_position(posi)

# the config array is [min,max,mean,sd]
def getGaussian(length_config):
    while True:
        length = random.gauss(length_config[2],length_config[3])
        if (length >length_config[0]) and (length < length_config[1]):
            return math.floor(length)

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
        distractor_list.append({'text': dis_list[i],'size':getGaussian(size_config),'fill': dis_fill})
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
        target_list.append({'text': targ_text, 'size': targ_size[i], 'fill':'black', 'x': targ_posi[i]['x'], 'y':targ_posi[i]['y'], 'rotate': 0})
    return target_list



if __name__=='__main__':
    wordlist = get_wordlist()
    
    # with app.app_context():
    #     position = json.dumps(get_target(2))
    #     print(position)

    app.run(debug=True)

# def get_english_stimuli(num_of_distractor, target1, target2):
#     legit_words = get_legit_word(decent_word_list,config.minLen,config.maxLen)
#     target_words = []
#     distractor_words = []

#     target1_text = ''
#     while True:
#         target1_text = random.choice(legit_words)
#         if(len(target1_text) == target1['length']):
#             legit_words.remove(target1_text)
#             break
    
#     target2_text = ''
#     while True:
#         target2_text = random.choice(legit_words)
#         if(len(target2_text) == target2['length']):
#             legit_words.remove(target2_text)
#             break

#     target_word_1 = {'text': target1_text, 'fontsize': target1['fontsize'], 'html': 'target'}
#     target_word_2 = {'text': target2_text, 'fontsize': target2['fontsize'], 'html': 'target'}

# def generate_wordlist(minL,maxL):
#     blacklist = ['ace', 'acerous', 'acers', 'aces', 'acne', 'acnes', 'acorn', 'acorns', 'acre', 'acres', 'aeons', 'anus', 'arc', 'arcs', 'are', 'ares', 'arose', 'arouse', 'ars', 'arson', 'aver', 'axe', 'axes', 'axon', 'axons', 'azure', 'azures', 'can', 'cane', 'caner', 'caners', 'canes', 'canoe', 'canoer', 'canoes', 'cans', 'car', 'care', 'cares', 'carouse', 'cars', 'carve', 'carves', 'case', 'cause', 'causer', 'cave', 'caver', 'cavern', 'cavernous', 'caverns', 'cavers', 'caves', 'censor', 'coarse', 'coarsen', 'coax', 'coaxer', 'coaxes', 'con', 'cone', 'cones', 'cons', 'convex', 'core', 'cores', 'corn', 'cornea', 'corneas', 'corns', 'course', 'cove', 'coven', 'covens', 'cover', 'covers', 'coves', 'crane', 'cranes', 'crave', 'craves', 'craze', 'crazes', 'crone', 'crones', 'crux', 'cruxes', 'cue', 'cues', 'cur', 'cure', 'cures', 'curs', 'curse', 'curve', 'curves', 'czar', 'czars', 'ear', 'earn', 'earns', 'ears', 'ecru', 'ecrus', 'ens', 'eon', 'eons', 'era', 'eras', 'eros', 'euro', 'euros', 'exon', 'exons', 'nares', 'nave', 'naves', 'near', 'nears', 'nervous', 'nevus', 'nexus', 'nor', 'norse', 'nos', 'nose', 'nova', 'novae', 'novas', 'nurse', 'nus', 'oar', 'oars', 'ocean', 'oceans', 'once', 'one', 'ones', 'onus', 'orca', 'ore', 'ores', 'ors', 'ounce', 'ounces', 'our', 'ours', 'ova', 'oven', 'ovens', 'over', 'overs', 'oxane', 'oxen', 'oxens', 'oxes', 'race', 'races', 'ran', 'rave', 'raven', 'ravenous', 'ravens', 'raves', 'raze', 'razes', 'reason', 'recon', 'rescan', 'rev', 'revs', 'roan', 'roans', 'roe', 'roes', 'rose', 'roue', 'roues', 'rouse', 'rove', 'roves', 'rue', 'rues', 'run', 'rune', 'runes', 'runs', 'ruse', 'sac', 'sane', 'saner', 'sauce', 'saucer', 'save', 'saver', 'savor', 'savour', 'sax', 'scan', 'scar', 'scare', 'scone', 'score', 'scorn', 'scour', 'sea', 'sear', 'senor', 'senora', 'sera', 'sex', 'snare', 'snore', 'soar', 'son', 'sonar', 'sore', 'sour', 'source', 'sox', 'suave', 'suaver', 'sue', 'suer', 'sun', 'sure', 'uncase', 'uncover', 'uncovers', 'unsex', 'urea', 'urn', 'urns', 'use', 'user', 'uvea', 'van', 'vane', 'vanes', 'vans', 'vase', 'vear', 'vears', 'venous', 'venus', 'vex', 'xerus', 'zas', 'zax', 'zaxes', 'zen', 'zens', 'zero', 'zeros', 'zoa', 'zoea', 'zoeas', 'zone', 'zoner', 'zoners', 'zones', 'zorse', 'zouave', 'zouaves']
#     naughtyList =  ['anal', 'anus', 'arrse', 'arse', 'ass', 'asses','assfucker', 'assfukka', 'asshole', 'assholes', 'asswhole','b!tch', 'b00bs','b17ch','b1tch','ballbag','balls','ballsack','bastard','beastial','beastiality','bellend','bestial','bestiality','biatch','bitch','bitcher','bitchers','bitches','bitchin','bitching','bloody','blow job','blowjob','blowjobs','boiolas','bollock','bollok','boner','boob','boobs','booobs','boooobs','booooobs','booooooobs','bras','breasts','buceta','bugger','bum','bunny fucker','butt','butthole','buttmuch','buttocks','buttplug','c0ck','c0cksucker','carpet muncher','cawk','chink','cipa','cl1t','clit','clitoris','clits','cnut','cock','cock-sucker','cockface','cockhead','cockmunch','cockmuncher','cocks','cocksuck','cocksucked','cocksucker','cocksucking','cocksucks','cocksuka','cocksukka','cok','cokmuncher','coksucka','coon','cox','cracker','crap','cum','cummer','cumming','cums','cumshot','cunilingus','cunillingus','cunnilingus','cunt','cuntlick','cuntlicker','cuntlicking','cunts','cyalis','cyberfuc','cyberfuck','cyberfucked','cyberfucker','cyberfuckers','cyberfucking','d1ck','damn','diarrhea','dick','dickhead','dike','dildo','dildos','dink','dinks','dirsa','dlck','dog-fucker','doggin','dogging','donkeyribber','doosh','duche','dyke','ejaculate','ejaculated','ejaculates','ejaculating','ejaculatings','ejaculation','ejakulate','f u c k','f u c k e r','f4nny','fag','fagging','faggitt','faggot','faggs','fagot','fagots','fags','fanny','fannyflaps','fannyfucker','fanyy','fatass','fcuk','fcuker','fcuking','feces','feck','fecker','felching','fellate','fellatio','fingerfuck','fingerfucked','fingerfucker','fingerfuckers','fingerfucking','fingerfucks','fistfuck','fistfucked','fistfucker','fistfuckers','fistfucking','fistfuckings','fistfucks','flange','fook','fooker','fuck','fucka','fucked','fucker','fuckers','fuckhead','fuckheads','fucking','fuckings','fuckingshitmotherfucker','fuckme','fucks','fuckwhit','fuckwit','fudge packer','fudgepacker','fuk','fuker','fukker','fukkin','fuks','fukwhit','fukwit','fux','fux0r','f_u_c_k','gangbang','gangbanged','gangbangs','gaylord','gaysex','goatse','God','god-dam','god-damned','goddamn','goddamned','hardcoresex','hell','heshe','hoar','hoare','hoer','homo','homosexual','homosexuals','hooker','hore','horniest','horny','hotsex','"jack-off','jackoff','jap','jerk-off','jism','jiz','jizm','jizz','kawk','knob','knobead','knobed','knobend','knobhead','knobjocky','knobjokey','kock','kondum','kondums','kum','kummer','kumming','kums','kunilingus','l3i+ch','l3itch','labia','lesbian','lesbians','lesbo','lmfao','lust','lusting','m0f0','m0fo','m45terbate','ma5terb8','ma5terbate','masochist','massacre','master-bate','masterb8','masterbat*','masterbat3','masterbate','masterbation','masterbations','masturbate','mo-fo','mof0','mofo','mothafuck','mothafucka','mothafuckas','mothafuckaz','mothafucked','mothafucker','mothafuckers','mothafuckin','mothafucking','mothafuckings','mothafucks','mother fucker','motherfuck','motherfucked','motherfucker','motherfuckers','motherfuckin','motherfucking','motherfuckings','motherfuckka','motherfucks','muff','mutha','muthafecker','muthafuckker','muther','mutherfucker','n1gga','n1gger','nazi','nigg3r','nigg4h','nigga','niggah','niggas','niggaz','nigger','niggers','nob','nob jokey','nobhead','nobjocky','nobjokey','numbnuts','nutsack','orgasim','orgasims','orgasm','orgasms','p0rn','pawn','pecker','penis','penisfucker','phonesex','phuck','phuk','phuked','phuking','phukked','phukking','phuks','phuq','pigfucker','pimpis','piss','pissed','pisser','pissers','pisses','pissflaps','pissin','pissing','pissoff','playboy','poop','porn','porno','pornography','pornos','prick','pricks','pron','pube','pusse','pussi','pussies','pussy','pussys','rape','raper','rapist','rectum','retard','rimjaw','rimming','s hit','s.o.b.','sadist','schlong','screwing','scroat','scrote','scrotum','semen','sensual','sensuous','sex','sexes','"sh!+"','"sh!t"','sh1t','shag','shagger','shaggin','shagging','shemale','"shi+"','shit','shitdick','shite','shited','shitey','shitfuck','shitfull','shithead','shiting','shitings','shits','shitted','shitter','"shitters "','shitting','shittings','"shitty "','skank','slut','sluts','smegma','smut','snatch','"son-of-a-bitch"','spac','spunk','s_h_i_t','t1tt1e5','t1tties','teets','teez','testical','testicle','tit','titfuck','tits','titt','tittie5','tittiefucker','titties','tittyfuck','tittywank','titwank','tosser','turd','tw4t','twat','twathead','twatty','twunt','twunter','urinary','urine','uterus','v14gra','v1gra','vagina','vaginal','viagra','vulva','w00se','wang','wank','wanker','wanky','weiner','whoar','whore','whores','willies','willy','xrated','xxx','FALSE','corpses','corpse','bodies','auschwitz']
#     all_word = []
#     dictionary = []
#     adescenders = r"qtyiplkjhgfdb"
#     with open('dict.csv', 'r') as csvfile:
#         reader = csv.reader(csvfile)
#         for row in reader:
#             all_word.append(row[0])
#     for word in all_word:
#         if not any(char in word for char in adescenders):
#              if  (len(word) >= minL)& (len(word) <= maxL):
#                  if (not word in blacklist )& (not word in naughtyList):
#                     dictionary.append(word)
#     return dictionary