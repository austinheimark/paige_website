from flask import (
    Flask, 
    render_template,
    request,
    abort,
    url_for,
    redirect,
    flash,
    g,
     _app_ctx_stack
    )

import flask

REAL_KEY = '9f4yZIjq'
REAL_VALUE = 'CsyGlIE0'
VALID_PASSWORD = 'password'
DATABASE = 'paige_website.db'

app = Flask(__name__)
app.secret_key = 'something'
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#returns true if the user is logged in
def verify_login():
    try:
        return request.cookies[REAL_KEY] == REAL_VALUE
    except KeyError:
        return False

#initializes the database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()    

#creates a database connection if there isn't already one
def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db

    return top.sqlite_db

#closes the database again at the end of the request
@app.teardown_appcontext
def close_db_connection(exception):
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()

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
    if not verify_login():
        abort(401)    

    return render_template('admin.html', page='Administration')


@app.route('/login')
def login():
    return render_template('login.html', page='Login')

@app.route('/login/authenticate', methods=['POST'])
def authenticate():
    try:
        if request.form['password'] == VALID_PASSWORD:      #if correct password, redirect to admin page and set the cookie
            response = redirect(url_for('admin'))
            response.set_cookie(REAL_KEY, REAL_VALUE)
            return response
    except KeyError:
        pass
    flash('Wrong password, try again!')
    return redirect(url_for('login'))

@app.route('/logout', methods=['POST'])
def logout():
    #logout redirects to the home page
    response = redirect(url_for('home'))
    #reset the cookie with the wrong value and an immediate expiration date --> hence logged out
    response.set_cookie(REAL_KEY, 'wrong', expires=0)
    return response

@app.route('/new_image')
def new_image():
    if not verify_login():
        abort(401) 

    return render_template('new_image.html', page='New Image')

#accepts form from '/new_image', authenticates form data, then posts the new image
@app.route('/new_image/authenticate', methods=['POST'])
def upload_image():
    if not verify_login():
        abort(401)

    wanted_keys = ['link', 'title', 'caption', 'type']

    if not set(wanted_keys) <= set(request.form.keys()):
        flash('You forgot some entry fields!')
        response = redirect(url_for('new_image'))
        return response 

    #add form data to the database here
    db = get_db()
    db.execute('insert into images (link, title, caption, type) values (?, ?, ?, ?)',
        [request.form['link'], request.form['title'], request.form['caption'], request.form['type']])
    db.commit()

    flash('Image successfully uploaded!')
    response = redirect(url_for('admin'))
    return response

@app.route('/delete_image')
def delete_image():
    if not verify_login():
        abort(401)
    
    return render_template('delete_image.html', page='Delete Image')

#401 is when user tries to access a page that they are unauthorized to access
@app.errorhandler(401)
def unauthorized_page(error):
    return render_template('unauthorized.html'), 401

#not found error page
@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True)



    