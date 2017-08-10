from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def greetings():
    return render_template('landing_page.html')

@app.route('/ninja_page', methods=['GET'])
def ninja_info():
    return render_template('ninja_page.html')

@app.route('/dojos', methods =['GET'])
def dojos():
    return render_template('dojos.html')

@app.route('/dojos/new', methods =['POST'])
def dojos_new():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    favorite_turtle = request.form['favorite_turtle']
    return render_template('dojos.html', form=request.form)

app.run(debug=True)