from flask import Flask, render_template, jsonify, json
import random
import csv
from Configures import config
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/testText/')
def test_text():
    return 'Testing 1 2 4. "Three sir!" 3!'

@app.route('/cloud/')
def cloud():
    return render_template('cloud.html',dis_fill = "#bdbdbd",posi = jsonify(config.get_target_position(1)))


def get_targ_config(posi):
    return config.get_target_position(posi)

# def get_targ_word(leng):


if __name__=='__main__':
    with app.app_context():
    #     position = json.dumps({'a':3})
         position = json.dumps(config.get_target_position(1))
    #     print("111")
         print(position)

    app.run(debug=True)

# def get_stim()

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