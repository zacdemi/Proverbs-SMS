from flask import Flask, render_template, redirect, url_for, request, flash
from pforms import searchtag,UpdateSubscription,Phone,ConfirmCode,Subscribe
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
    form = searchtag()
    time = proverbs.proverbs_clock()
    if request.method == 'POST':
        if request.form['action'] == 'search' and form.validate_on_submit():
             search = form.search.data.lower()
             verses = proverbs.findtag(search)
             if not verses:
                 flash('There are no proverbs with tag '+ search,'ok')
             else:
                 return render_template('index.html',time=time,
                                        form=form, verses=verses)
    
    return render_template('index.html',time=time, form=form)

@app.route('/home/subscribe/',methods = ['GET','POST'])
def subscribe():
    form = Subscribe()

    if request.method == 'POST':
        phone = form.phone.data
        if request.form['action'] == "Subscribe!":
            if form.validate == False:
                flash("Please enter required fields")
            elif form.validate and proverbs.userexist(phone):
                flash("this phone number has already been subscribed. "
                      "to unsubscribe, go to the manage my subscription "
                      "on the home page")
                return render_template('subscribe.html',form=form)
            else:
                carrier = form.carrier.data
                frequency  = form.frequency.data
                tags = form.taglist.data
                #add user to database
                proverbs.adduser(phone,carrier,tags,frequency)
                proverbs.sendconfirm(phone)
                flash("Thank you for subscribing. You will recieve a "
                      "confirmation text now.")
                return redirect(url_for('confirmation',phone=phone))
        elif request.form['action'] == "Return Home":
            return redirect(url_for('home'))
    return render_template('subscribe.html',form=form)

@app.route('/home/subscribe/confirm/<int:phone>/',methods = ['GET','POST'])
def confirmation(phone):
    form = ConfirmCode()
    if request.method == 'POST':
        if form.validate == False:
            flash_errors(form)
        elif request.form['action'] == "Confirm Code":
            confirm_code = form.confirm_code.data
            if proverbs.checkconfirm(phone,confirm_code):
                proverbs.subscribe_user(phone,"Yes")
                proverbs.sendconfirm(phone)
                return redirect(url_for('success'))
            else:
                flash("Confirm code not found. Please try again")
        elif request.form['action'] == "Regenerate Confirm":
            proverbs.sendconfirm(phone)
            flash("A new confirm code has been sent to " + str(phone)) 
    return render_template('confirm.html',form=form)

@app.route('/home/subscribe/success',methods = ['GET','POST'])
def success():
    return render_template('success.html')


@app.route('/home/manage_my_subscription',methods = ['GET','POST'])
def manage():

    form = Phone()
    form1 = UpdateSubscription()

    if request.method == 'POST':
        phone = form.phone.data
        if request.form['action'] == "Return Home":
            return redirect(url_for('home'))
        elif form.validate() == False:
            flash_errors(form) 
        elif request.form['action'] == "Unsubscribe":
            proverbs.subscribe_user(phone,"No")
            flash("This number has been unsubscribed")
        elif request.form['action'] == "Update Subscription":
            return render_template('manage.html',update = True,form=form,form1=form1)
        elif request.form['action'] == "Submit Changes" and form1.validate_on_submit:
            if userexist == False:
                flash(str(phone) + " is not subscribed. Please subscribe first")
            else:
                taglist = form1.taglist.data
                frequency = form1.frequency.data
                proverbs.update_user(phone,taglist,frequency)
                flash("Your subscription has been successfully updated")
    return render_template('manage.html',form=form)

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
