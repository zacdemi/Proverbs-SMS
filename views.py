from flask import Flask, render_template, redirect, url_for, request, flash
from pforms import Phone,UserPreferences,ConfirmCode
import proverbs
import flask
import config

app = Flask(__name__)

@app.route('/')
def proverbs_page():
#redirect to home page!
    return redirect(url_for('home'))

@app.route('/home/',methods = ['GET','POST'])
def home():
    form = Phone()
    if request.method == 'POST' and form.validate():
        phone = form.phone.data
        if proverbs.userexist(phone):
            return redirect(url_for("preferences",phone=phone))
        else:
            proverbs.adduser(phone)
            proverbs.sendconfirm(phone)
        return redirect(url_for("confirmation",phone=phone))
    else:
        flash_errors(form) 
    return render_template('home.html',form=form)

@app.route('/home/confirm/<phone>/',methods = ['GET','POST'])
def confirmation(phone):
    form = ConfirmCode()
    if request.method == 'POST' and form.validate():
        confirm_code = form.confirm_code.data
        if proverbs.checkconfirm(phone,confirm_code):
            return redirect(url_for('preferences',phone=phone))
        else:
            flash("Confirm code not found. Please try again.")
    else:
        flash_errors(form)
    
    return render_template('confirm.html',form=form)

@app.route('/home/preferences/<phone>/',methods = ['GET','POST'])
def preferences(phone):
    form = UserPreferences()
    unsubscribe = proverbs.userexist(phone)
    if request.method == 'POST':
        if request.form["action"] == "SUBMIT" and form.validate():
            frequency = form.frequency.data
            taglist = form.taglist.data
            proverbs.update_user(phone,taglist,frequency)
            proverbs.subscribe_user(phone,"Yes")
            return redirect(url_for('success',phone=phone))
        elif request.form["action"] == "UNSUBSCRIBE":
            proverbs.subscribe_user(phone,"No")
            return redirect(url_for('success',phone=phone))
        else:
            flash_errors(form)
    
    return render_template('preferences.html',form=form,unsubscribe=unsubscribe)

@app.route('/home/success/<phone>/',methods = ['GET','POST'])
def success(phone):
    subscribe = proverbs.userexist(phone)
    if not subscribe:
       message = "You have been unsubscribed. Thank you for using get proverbs!"
    else:
       message = "Success! Thanks for signing up!" #proverbs.user_status(phone)
       proverbs.sendfirst(phone)
    flash(message)
    return render_template('success.html')

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text,error),'error')

if __name__ == "__main__":
    app.config.update(
      DEBUG = True,
      CSRF_ENABLED = True,
      SECRET_KEY = config.secret_key)
    app.run(host='104.131.27.56',port=5001)
