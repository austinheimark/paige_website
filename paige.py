from flask import (
    Flask, 
    render_template,
    request,
    abort,
    url_for,
    redirect,
    flash
    )

import flask

REAL_KEY = '9f4yZIjq'
REAL_VALUE = 'CsyGlIE0'
VALID_PASSWORD = 'password'

app = Flask(__name__)
app.secret_key = 'something'

#returns true if the user is logged in
def verify_login():
    return request.cookies[REAL_KEY] == REAL_VALUE

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
        if verify_login():
            return render_template('admin.html', page='Administration')
    except KeyError:    #error raised when a dict object is requested and no key is found
        pass
    abort(401)

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

#page where you Paige can add new images, will fill out form with all the options
@app.route('/new_image')
def new_image():
    #if the cookie is valid, then the admin page will be shown, otherwise an abort error
    try:
        if verify_login():
            return render_template('new_image.html', page='New Image')
    except KeyError:    #error raised when a dict object is requested and no key is found
        pass
    abort(401)   

#accepts form from '/new_image'
@app.route('/new_image/authenticate', methods=['POST'])
def upload_image():
    try:
        #test to ensure that every entry field has been entered
        if (request.form['link'] and 
            request.form['title'] and 
            request.form['caption'] and 
            #radio button...
            request.form['']):

            #add the image to respective section of website now

            flash('Image successfully uploaded!')
            return render_template('admin.html', page='Administration')
    except:
        pass
    flash('You forgot some entry fields!')
    return redirect(url_for('new_image'))

#page where Paige can delete images
@app.route('/delete_image')
def delete_image():
    #if the cookie is valid, then the admin page will be shown, otherwise an abort error
    try:
        if verify_login():
            return render_template('delete_image.html', page='Delete Image')
    except KeyError:    #error raised when a dict object is requested and no key is found
        pass
    abort(401)       


#is returned when user tries to access a page that they are unauthorized to access
@app.errorhandler(401)
def unauthorized_page(error):
    return render_template('unauthorized.html'), 401

#404 - not found
@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404

if __name__ == "__main__":
    app.run(debug=True)



    