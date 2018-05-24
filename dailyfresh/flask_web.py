# -*- coding: utf-8 -*-
from flask import *
from application import picture as pic, train_ticket as tic
from model import *
import config
import random
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index1():
    return redirect(url_for('index'))


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/ticket',methods =['GET','POST'])
def find_ticket():
    if request.method == 'GET':
        return render_template('ticket.html')
    elif request.method == 'POST':
        # print(Ticket.query.all())
        from_station= request.form.get('from_station')
        to_station = request.form.get('to_station')
        date = request.form.get('date')
        from_station1 = Ticket.query.filter_by(name = from_station).all()[0].name_en
        to_station1 = Ticket.query.filter_by(name= to_station).all()[0].name_en
        # print(from_station1,to_station1,date)
        station_info = (from_station1, to_station1,date)
        # print(station_info)
        ticket = tic.Ticket(station_info)
        tickets = ticket.ticket_informatin()
        # print(tickets)
        return render_template('ticketajax.html',tickets=tickets,date=date,from_station=from_station,to_station=to_station)
@app.route('/picture')
def picture():
    page = random.randint(0,200)
    pic1 = pic.Spaider(page, 'nihao')
    pictures = pic1.start()
    return render_template('picture.html',pictures=pictures)

@app.route('/pictureajax.html')
def pictureajax():
    page = random.randint(0, 200)
    pic1 = pic.Spaider(page, 'nihao')
    pictures = pic1.start()
    return render_template('pictureajax.html', pictures=pictures)


if __name__ == '__main__':
    app.run()
