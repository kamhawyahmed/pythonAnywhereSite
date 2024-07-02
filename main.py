from flask import Flask
from flask import render_template
from flask import request
import QuranDataManager
import availability_scheduler
import sqlite3



app = Flask(__name__)



#QuranMem setup
backend = QuranDataManager.DataManager()
surah_shown_index = 1
memorized_surahs = []
app_on = True
##


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    message = "Hello world"
    return render_template("index.html", msg = message)
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
            show_memorized_surah()
        else:
            for key in request.form.keys():
                if key.split("_")[1] == "surah":
                    toggle_memorized_surah()
                elif key.split("_")[1] == "ayah":
                    toggle_memorized_ayah()
                elif key.split("_")[0] == "select":
                    select_surah()
    return update_memorization()

def toggle_app():
    global app_on
    app_on = not app_on
    return

def show_memorized_surah():
    print("hi")
    global memorized_surahs
    memorized_surahs = []
    for surah_name in backend.return_memorized_ayat()["surah_name_roman"]:
        memorized_surahs.append(surah_name)
    memorized_surahs = list(set(memorized_surahs))

def select_surah():
    global surah_shown_index
    for key in request.form.keys():
        surah_shown_index = [int(s) for s in key.split("_") if s.isdigit()][0]
    return

def toggle_memorized_surah():
    for key in request.form.keys():
        surah_toggle_num = [int(s) for s in key.split("_") if s.isdigit()][0]
    ayat_to_toggle = list(range(1,backend.return_length_of_surah(surah_toggle_num)+1))
    backend.mark_ayah(surah_toggle_num, ayat_to_toggle)
    return

def toggle_memorized_ayah():
    for key in request.form.keys():
        surah_toggle_num, ayah_toggle_num = [int(s) for s in key.split("_") if s.isdigit()][0:2]
    backend.mark_ayah(surah_toggle_num, [ayah_toggle_num])
    return

def update_memorization():
    return render_template("memorization.html", memorized_surahs = memorized_surahs, backend = backend, app_on = app_on, surah_shown_index = surah_shown_index)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
