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
import flask.ext.sqlalchemy
import sys

REAL_KEY = '9f4yZIjq'
REAL_VALUE = 'CsyGlIE0'
VALID_PASSWORD = 'password'

app = Flask(__name__)
app.secret_key = 'something'
app.config.from_object(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://paigeuser:paigepassword@localhost/paigewebsitedb'
db = flask.ext.sqlalchemy.SQLAlchemy(app)

class Image(db.Model):
    __tablename__ = 'images'
    link = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    caption = db.Column(db.String)
    kind = db.Column(db.String)

    def __init__(self, link, title, caption, kind):
        self.link = link
        self.title = title
        self.caption = caption
        self.kind = kind

# class Password(db.Model):
#     __tablename__ = 'password'

# VALID_PASSWORD = Password.query.all()

#returns true if the user is logged in
def verify_login():
    try:
        return request.cookies[REAL_KEY] == REAL_VALUE
    except KeyError:
        return False

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
    images = Image.query.filter_by(kind='drawings').all()

    return render_template('picture.html', page='Drawings', images=images)

@app.route('/paintings')
def paintings():
    images = Image.query.filter_by(kind='paintings').all()

    return render_template('picture.html', page='Paintings', images=images)

@app.route('/sculptures')
def sculptures():
    images = Image.query.filter_by(kind='sculptures').all()

    return render_template('picture.html', page='Sculptures', images=images)

@app.route('/admin')
def admin():
    #if the cookie is valid, then the admin page will be shown, otherwise an abort error
    if not verify_login():
        abort(401)    

    return render_template('admin.html', page='Administration')


@app.route('/login')
def login():
    if verify_login():
        flash('Already logged in!')
        return redirect(url_for('admin'))

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

    wanted_keys = ['link', 'title', 'caption', 'kind']

    if not set(wanted_keys) <= set(request.form.keys()):
        flash('You forgot some entry fields!')
        response = redirect(url_for('new_image'))
        return response 

    #add form data to the database here
    new_image = Image(request.form['link'], request.form['title'], request.form['caption'], request.form['kind'])    
    db.session.add(new_image)

    #not sure if we need this
    db.session.commit()
    
    flash('Image successfully uploaded!')
    response = redirect(url_for('admin'))
    return response

@app.route('/delete_image')
def delete_image():
    if not verify_login():
        abort(401)
    
    images = Image.query.all()

    return render_template('delete_image.html', page='Delete Image', images=images)

@app.route('/delete_image/authenticate', methods=['POST'])
def actually_delete_image():
    if not verify_login():
        abort(401)

    link = request.form['img-delete']
    delete_this = Image.query.get(link)

    db.session.delete(delete_this)
    db.session.commit()

    flash('You successfully deleted an image!')
    return redirect(url_for('admin'))

#401 is when user tries to access a page that they are unauthorized to access
@app.errorhandler(401)
def unauthorized_page(error):
    return render_template('unauthorized.html'), 401

#not found error page
@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404

if __name__ == "__main__":
    try:
        command = sys.argv[1]
    except IndexError:
        print('A command is required')
        sys.exit(1)

    if command == 'initialize_db':
        db.create_all()        
    else:
        print('Command not recognized')
        sys.exit(1)
        




    