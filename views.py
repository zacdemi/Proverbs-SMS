from flask import Flask, render_template, redirect, url_for, request, flash
from pforms import Phone,UserPreferences,ConfirmCode
from sendgmail import sendnotification
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
            user_id = proverbs.return_id(phone)
            return redirect(url_for("preferences",user_id=user_id))
        else:
            proverbs.adduser(phone)
            proverbs.sendconfirm(phone)
            user_id = proverbs.return_id(phone)
        return redirect(url_for("confirmation",user_id=user_id))
    else:
        flash_errors(form) 
    return render_template('home.html',form=form)

@app.route('/home/confirm/<user_id>/',methods = ['GET','POST'])
def confirmation(user_id):
    form = ConfirmCode()
    phone = proverbs.return_phone(user_id)
    if request.method == 'POST' and form.validate():
        confirm_code = form.confirm_code.data
        if proverbs.checkconfirm(phone,confirm_code):
            return redirect(url_for('preferences',user_id=user_id))
        else:
            flash("Confirm code not found. Please try again.")
    else:
        flash_errors(form)
    
    return render_template('confirm.html',form=form)

@app.route('/home/preferences/<user_id>/',methods = ['GET','POST'])
def preferences(user_id):
    form = UserPreferences()
    phone = proverbs.return_phone(user_id)
    userstatus = proverbs.userstatus(phone)
    if request.method == 'POST':
        if request.form["action"] == "SUBMIT" and form.validate():
            frequency = form.frequency.data
            taglist = form.taglist.data
            proverbs.update_user(phone,taglist,frequency)
            return redirect(url_for('success',user_id=user_id))
        elif request.form["action"] == "UNSUBSCRIBE":
            proverbs.subscribe_user(phone,"No")
            #send message to marketing manager
            sendnotification(phone,"unsubscribed")
            return redirect(url_for('success',user_id=user_id))
        else:
            flash_errors(form)
    
    return render_template('preferences.html',form=form,userstatus=userstatus)

@app.route('/home/success/<user_id>/',methods = ['GET','POST'])
def success(user_id):
    phone = proverbs.return_phone(user_id)
    status = proverbs.userstatus(phone)
    if status == "No":
        message = "You have been unsubscribed. Thank you for using get proverbs!"
    elif status == "Not Yet":
        message = "Success! Thanks for signing up!" #proverbs.user_status(phone)
        proverbs.subscribe_user(phone,"Yes")
        proverbs.sendfirst(phone)
        sendnotification(phone,"subscribed")
    elif status == "Yes":
        message = "Your preferences have been successfully updated!"  

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
    app.run(host='127.0.0.1',port=5001)
