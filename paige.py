from flask import (
    Flask, 
    render_template,
    request,
    abort,
    url_for,
    redirect
)
import flask

REAL_KEY = '9f4yZIjq'
REAL_VALUE = 'CsyGlIE0'

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/resume')
def resume():
    return render_template('resume.html', page='Resume')

@app.route('/contact')
def contact():
    return render_template('contact.html', page='Contact')

@app.route('/drawings')
def drawings():
    return render_template('drawings.html', page='Drawings')

@app.route('/paintings')
def paintings():
    return render_template('paintings.html', page='Paintings')

@app.route('/sculptures')
def sculptures():
    return render_template('sculptures.html', page='Sculptures')

@app.route('/admin')
def admin():
    #if the cookie is valid, then the admin page will be shown, otherwise an abort error
    try:
        if request.cookies[REAL_KEY] == REAL_VALUE:
            return render_template('admin.html', page='Administration')
    except KeyError:    #error raised when a dict object is requested and no key is found
        pass
    abort(401)

@app.route('/login')
def login():
    return render_template('login.html', page='Login')

@app.route('/login/authenticate')
def authenticate():
    try:
        if request.cookies[REAL_KEY] == REAL_VALUE:
            return redirect(url_for('admin'))
    except KeyError:
        pass
    abort(401)

#is returned when user tries to access a page that they are unauthorized to access
@app.errorhandler(401)
def unauthorized_page(error):
    return render_template('unauthorized.html'), 401

@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404

if __name__ == "__main__":
    app.run(debug=True)



    