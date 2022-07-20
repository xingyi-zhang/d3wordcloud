from flask import Flask, render_template, jsonify
import random
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/testText/')
def test_text():
    return 'Testing 1 2 4. "Three sir!" 3!'

@app.route('/cloud/')
def cloud():
    return render_template('cloud.html')

if __name__=='__main__':
    app.run(debug=True)
