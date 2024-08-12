from flask import Flask, render_template, request, redirect, session
import secrets
from user import User
app = Flask(__name__)
secret_key_urlsafe = secrets.token_urlsafe(16)
app.secret_key = secret_key_urlsafe

@app.route('/users')
def display_users():
    all_users = User.get_all()
    return render_template('read_all.html', all_users=all_users)

@app.route('/users/new')
def show_page():
    return render_template('create.html')

@app.route('/create_user', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        session['create_user_data'] = request.form
        return redirect('/users/new')
    # if 'create_user_data' exists in session, delete it when creating a user
    if 'create_user_data' in session:
        session.pop('create_user_data')
        
    data = {
        'fname': request.form['fname'],
        'lname': request.form['lname'],
        'email': request.form['email']
    }
    User.create_user(data)
    return redirect('/users')

if __name__=="__main__":
    app.run(debug=True, host='localhost', port='5150')