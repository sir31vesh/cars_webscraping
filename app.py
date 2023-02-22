from flask import request
import schedule
from flask import Flask, render_template
from DRIVER import *

time_input = "09:00"
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("Loginpage.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/',methods=['POST'])
def getvalue():
    carname = request.form['fname']
    fuel = request.form['fuel']
    Transmission = request.form['Transmission']
    mail_id = request.form['mail_id']

    print(carname+" "+Transmission+" "+fuel)
    scrape(carname, Transmission, fuel)
    send_mail(mail_id)

    def job():
        scrape(carname, Transmission, fuel)
        send_mail(mail_id)

        return render_template('index.html')

    # scheduler
    schedule.every().day.at(time_input).do(job)
    # schedules all pending tasks
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    app.run()


