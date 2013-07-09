from flask import Flask, render_template
app = Flask(__name__)

#route to paige's home page
@app.route('/')
def home():
    return render_template('home.html')

#route to paige's resume
@app.route('/resume')
def resume():
    return render_template('paige_resume.htm', page='RESUME')

#route to paige's contact page
@app.route('/contact')
def contact():
    return render_template('contact.html', page='CONTACT')

#route to paige's drawings
@app.route('/drawings')
def drawings():
    return render_template('drawings.html', page='DRAWINGS')

#route to paige's paintings
@app.route('/paintings')
def paintings():
    return render_template('paintings.html', page='PAINTINGS')

#route to paige's sculptures
@app.route('/sculptures')
def sculptures():
    return render_template('sculptures.html', page='SCULPTURES')

if __name__ == "__main__":
    app.run(debug=True)