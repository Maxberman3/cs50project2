from flask import Flask,session,render_template,request,redirect,url_for,flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, NoneOf
from flask_socketio import SocketIO, emit
import os
import sys
from random import seed,randint
from collections import deque
import json
seed(1)
app=Flask(__name__)
app.secret_key=os.urandom(25)
Bootstrap(app)
socketio=SocketIO(app)
active_display_names=[]
channels={}

class displaynameform(FlaskForm):
    displayname=StringField('Display Name:',[DataRequired(),NoneOf(active_display_names)])
class channelnameform(FlaskForm):
    channelname=StringField('Channel Name:',[DataRequired()])
class Channel:
    def __init__(self,username,name):
        self.chatters=[username]
        self.name=name
        self.chathistory=deque([],maxlen=100)
        while True:
            id=randint(0,1000000000000)
            if id not in channels:
                self.id=id
                break


@app.route("/",methods=["GET","POST"])
def index():
    if "displayname" in session:
        return render_template("mainpage.html",channels=channels,displayname=session['displayname'])
    else:
        form=displaynameform()
        if form.validate_on_submit():
            session['displayname']=form.displayname.data
            active_display_names.append(session['displayname'])
            return redirect("/")
        return render_template("displayname.html",form=form)
@app.route("/newchannel",methods=["GET","POST"])
def newchannel():
    form=channelnameform()
    if form.validate_on_submit():
        newchan=Channel(session['displayname'],form.channelname.data)
        channels[newchan.id]=newchan
        flash('Channel succesfully created')
        return redirect(url_for('index'))
    return render_template('createchannel.html',form=form)
@app.route("/channel/<int:channelid>")
def displaychannel(channelid):
    return render_template('displaychannel.html',channelid=json.dumps(channelid))

@socketio.on('messagesend')
def messagerelay(data):
    msgtext=data['text']
    emit('message relay',{'text':msgtext},broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
