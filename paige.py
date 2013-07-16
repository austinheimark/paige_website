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
    return render_template('resume.html', page='RESUME')

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
    #if the cookie is valid, then the admin page will be shown, otherwise an abort error
    try:
        if request.cookies['9f4yZIjq'] == 'CsyGlIE0':
            return render_template('admin.html', page='ADMIN')
    except KeyError:    #error raised when a dict object is requested and no key is found
        pass
    abort(401)

#is returned when user tries to access a page that they are unauthorized to access
@app.errorhandler(401)
def unauthorized_page():
    return render_template('unauthorized.html'), 401


if __name__ == "__main__":
    app.run(debug=True)

    