from flask import Flask, render_template
app = Flask(__name__)

#route to paige's home page
@app.route('/')
def home():
    return render_template('home.html')

#route to paige's resume
@app.route('/resume')
def resume():
    return render_template('resume.html')

#route to paige's contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)



