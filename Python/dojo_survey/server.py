from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def user_results():
    print 'got info'
    print request.form['name', 'dojo location', 'favorite language', 'comment']
    return redirect ('/index.html')   

app.run(debug=True)

