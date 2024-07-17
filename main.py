
from flask import Flask
from flask import render_template
from flask import request
import qurandatamanager
import availability_scheduler
import sqlite3



app = Flask(__name__)



#QuranMem setup
backend = qurandatamanager.DataManager()
surah_shown_index = 1
memorized_surahs = []
app_on = True
surah_list = backend.make_mock_surah_list()

##


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    message = "Hello world"
    return render_template("index.html", msg = message)

@app.route('/test', methods=['GET', 'POST'])
def test():
    message = "Hello world"
    return render_template("intro.html", msg = message)
@app.route('/sleep', methods=['GET', 'POST'])
def sleep_sync():
    message = "Hello world"
    return render_template("sleep.html", msg = message)

@app.route('/scheduler', methods=["GET","POST"])
def scheduler():
    output = ""
    if request.method == 'POST':
        for key in request.form.keys():
            month_num = key.split("_")[1] #number of month
        output = availability_scheduler.availability_calculator(availability_scheduler.month_parser(month_num))

    return render_template("scheduler.html", output=output)


@app.route('/memorization', methods=['GET', 'POST'])
def quran_memorization_page():
    if request.method == 'POST':
        print(request.form)
        if "app_on" in request.form:
            toggle_app()
        elif "show_memorized" in request.form:
            global memorized_surahs
            memorized_surahs = backend.show_memorized_surah()
        else:
            for key in request.form.keys():
                if key.split("_")[1] == "surah":
                    backend.toggle_memorized_surah(key)
                elif key.split("_")[1] == "ayah":
                    backend.toggle_memorized_ayah(key)
                elif key.split("_")[0] == "select":
                    global surah_shown_index
                    surah_shown_index = backend.select_surah(key)
    return update_memorization()

def toggle_app():
    global app_on
    app_on = not app_on
    return


def update_memorization():
    return render_template("memorization.html", memorized_surahs = memorized_surahs, backend = backend, app_on = app_on, surah_shown_index = surah_shown_index, surah_list = surah_list)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
