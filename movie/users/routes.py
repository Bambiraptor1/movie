from flask import Blueprint, render_template, redirect, url_for, request, flash
from movie.models import User
from movie.extensions import db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required

user_bp = Blueprint('user', __name__, template_folder='templates')

@user_bp.route('/')
@login_required
def index():
  return render_template('users/index.html', title='User Page')

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    query = db.select(User).where(User.username==username)
    user = db.session.scalar(query)
    if user:
      flash('Username is already exists!', 'warning')
      return redirect(url_for('user.register'))
    else:
      query = db.select(User).where(User.email==email)
      user = db.session.scalar(query)
      if user:
        flash('Email is already exists!', 'warning')
        return redirect(url_for('user.register'))
      else:
        if password == confirm_password:
          pwd_hash = bcrypt.generate_password_hash(password).decode('utf-8')
          user = User(username=username, email=email, password=pwd_hash)
          db.session.add(user)
          db.session.commit()
          flash('Register successful!', 'success')
          return redirect(url_for('user.login'))
        else:
          flash('Password not match!', 'warning')
          return redirect(url_for('user.register'))
        
  return render_template('users/register.html', title='Register Page')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    query = db.select(User).where(User.username==username)
    user = db.session.scalar(query)
    if user:
      if bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for('user.index'))
      else:
        flash(f'Check your password again!', 'warning')
        return redirect(url_for('user.login'))
    else:
      flash(f'Username: {username} is not exists!', 'warning')
      return redirect(url_for('user.login'))

  return render_template('users/login.html', title='Login Page')

@user_bp.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('core.index'))

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
  user = current_user
  if request.method == 'POST':
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')

    if len(firstname)>0 or len(lastname)>0:
      user.firstname = firstname
      user.lastname = lastname

      db.session.add(user)
      db.session.commit()

      flash('Update profile successful!', 'success')
      return redirect(url_for('user.profile'))
    

  return render_template('users/profile.html', title='Profile Page', user=user)

@user_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
  if request.method == 'POST':
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if bcrypt.check_password_hash(current_user.password, current_password):
      flash('Current password is incorrect!', 'warning')
      return redirect(url_for('user.change_password'))

    if new_password != confirm_password:
      flash('New password not match!', 'warning')
      return redirect(url_for('user.change_password'))

    pwd_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
    current_user.password = pwd_hash

    db.session.commit()

    flash('Password changed successfully!', 'success')
    return redirect(url_for('user.profile'))

  return render_template('users/change_password.html', 
                         title='Change Password Page')