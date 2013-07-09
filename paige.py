from flask import (
    Flask, 
    render_template,
    request,
    abort
)
import flask

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/resume')
def resume():
    return render_template('paige_resume.htm', page='RESUME')

@app.route('/contact')
def contact():
    return render_template('contact.html', page='CONTACT')

@app.route('/drawings')
def drawings():
    return render_template('drawings.html', page='DRAWINGS')

@app.route('/paintings')
def paintings():
    return render_template('paintings.html', page='PAINTINGS')

@app.route('/sculptures')
def sculptures():
    return render_template('sculptures.html', page='SCULPTURES')

@app.route('/admin')
def admin():
    if '9f4yZIjq' in request.cookies and request.cookies['9f4yZIjq'] == 'CsyGlIE0':
        return render_template('admin.html', page='ADMIN')
    abort(401)


if __name__ == "__main__":
    app.run(debug=True)