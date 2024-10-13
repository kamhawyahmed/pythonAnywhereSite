#PYTHONANYWHERE SETUP INSTRUCTIONS -
# del folder
# git clone github
# pip3.10 install --user -r requirements.txt
# error codes ignore

# TODO list
# TODO check for better font
# TODO separate out surah name surah page like surah list
# TODO add deeper shade button click colour
# Make pretty home done
# Make pretty surah page done
# Reintegrate with pythonanywhere site done
# Add class for table even though never adding new records but to refer to them - DONE
#   maybe dont have to define all col's and maybe will crash if applying - found it 
# Convert from 1 page site to multi page - DONE
#   Home page with surah list DONE
#   subpages for surahs DONE
# - 1 button to view all memorized surah (get) DONE
# - 1 BUTTON TO SHOW BUTTONS DONE
# - 114 buttons for 114 chapters, click button - mark memorize DONE and change colour (put) DONE
#    #html loop for 114 buttons DONE
#    #integrate data from main.py DONE

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey
from typing import List
from flask_migrate import Migrate

import availability_scheduler

#


app = Flask(__name__)

class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quran_data.db" #default bind
app.config["SQLALCHEMY_BINDS"] = {
    "library": "sqlite:///new-books-collection.db"
}
# app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(model_class=Base)
migrate = Migrate(app, db)
db.init_app(app)
migrate.init_app(app, db)



# with app.app_context(): #open the app
#     db.reflect()


class Book(db.Model):
    __bind_key__ = "library"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'

class Surah(db.Model):
    __tablename__ = "surah"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    surah_no: Mapped[int] = mapped_column(Integer, unique=True)
    total_ayah_surah: Mapped[int] = mapped_column(Integer)
    juz_no: Mapped[int] = mapped_column(Integer)
    surah_name_roman: Mapped[str] = mapped_column(String)
    surah_name_en: Mapped[str] = mapped_column(String)
    surah_name_ar: Mapped[str] = mapped_column(String)
    place_of_revelation: Mapped[str] = mapped_column(String)
    surah_memorized: Mapped[int] = mapped_column(Integer)
    ayat: Mapped[List["Ayah"]] = relationship(back_populates="surah")
    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'< Surah {self.surah_no}, Ayat: {self.ayat} >'

class Ayah(db.Model): 
    __tablename__ = "ayah"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    surah_name_roman: Mapped[str] = mapped_column(String)
    surah_no: Mapped[int] = mapped_column(ForeignKey("surah.surah_no"))
    juz_no: Mapped[int] = mapped_column(Integer)
    ayah_no_surah: Mapped[int] = mapped_column(Integer)
    ayah_memorized: Mapped[int] = mapped_column(Integer)
    surah: Mapped["Surah"] = relationship(back_populates="ayat")
    ayah_ar: Mapped[str] = mapped_column(String)
    ayah_no_quran: Mapped[int] = mapped_column(Integer, unique=True)
    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Ayah {self.surah_no}:{self.ayah_no_surah}>'

class MemorizationUserAyah(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String)
    ayah_no_quran: Mapped[int] = mapped_column(Integer)
    ayah_memorized: Mapped[int] = mapped_column(Integer)
    def __repr__(self):
        return f'<User {self.id}: {self.name}'

with app.app_context(): #open the app on script run
    db.create_all()


#misc
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template("index.html")

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




#Library
@app.route('/library', methods=["GET","POST"])
def library_home():
    #all books
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars()
    all_books = list(db.session.execute(db.select(Book).order_by(Book.title)).scalars())
    # book = db.session.execute(db.select(Book).where(Book.title == "Harry Potter")).scalar()
    book_to_find = None
    if request.method == "POST":
        book_to_find = db.session.execute(db.select(Book).where(Book.title == request.form["title"])).scalar()
    return render_template("library_index.html", book_list=all_books, book_to_find=book_to_find)


@app.route("/library/add", methods=['GET','POST'])
def library_add():
    if request.method == "POST":
        new_book_db_entry = Book(title = request.form["title"], author = request.form["author"], rating = request.form["rating"])
        db.session.add(new_book_db_entry)
        db.session.commit()
        return redirect(url_for('library_home'))

    return render_template("library_add.html")

@app.route("/library/update/<id>", methods=['GET','POST'])
def library_update(id):
    if request.method == "POST":
        #book_to_update = db.get_or_404(Book, id)
        book_to_update = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('library_home'))
    book = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
    return render_template("library_update.html", book=book)

@app.route("/library/delete/<id>", methods=['GET'])
def library_delete(id):
    book_to_delete = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('library_home'))


#Quran Memorization
@app.route('/memorization/', methods=['GET'])
def memorization_home():
    result = db.session.execute(db.select(Surah))
    surahs = result.scalars().all()
    return render_template("memorization_home.html", surahs = surahs)

@app.route('/memorization/surah/<surah_no>', methods=['GET', 'POST'])
def memorization_surah(surah_no):
    result = db.session.execute(db.select(Surah).where(Surah.surah_no == surah_no))
    surah_selected = result.scalar()
    if request.method == 'POST':
        key = list(request.form.keys())[0]
        if "surah" in key:
            surah_selected.surah_memorized = 1 - surah_selected.surah_memorized
            ayat_selected = surah_selected.ayat
            for ayah in ayat_selected:
                ayah.ayah_memorized = surah_selected.surah_memorized
            db.session.commit()
        elif "ayah" in key:
            ayah_no = [int(s) for s in key.split("_") if s.isdigit()][0]
            ayah_selected = surah_selected.ayat[ayah_no - 1]
            ayah_selected.ayah_memorized = 1 - ayah_selected.ayah_memorized
            surah_selected.surah_memorized = calculate_surah_memorized(surah_selected)
            db.session.commit()
    return render_template("memorization_surah.html", surah_selected = surah_selected)


def calculate_surah_memorized(surah):
    surah_memorized = 1
    for ayah in surah.ayat:
        if ayah.ayah_memorized == 0:
            surah_memorized = 0
    return surah_memorized

def update_all_surah_memorized_manually():
    with app.test_request_context():
        result = db.session.execute(db.select(Surah))
        surah_list = result.scalars().all()
        for surah in surah_list:
            surah_memorized = 1
            for ayah in surah.ayat:
                if ayah.ayah_memorized == 0:
                    surah_memorized = 0
                    print(surah.surah_no, ayah.ayah_no_surah, ayah.ayah_memorized, surah_memorized)
            surah.surah_memorized = surah_memorized
        db.session.commit()
    return

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2000,debug=True)