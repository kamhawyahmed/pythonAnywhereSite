#PYTHONANYWHERE SETUP INSTRUCTIONS -
# migrate db if needed
# cd pythonAnywhereSite
# git pull
# source ../.virtualenvs/my-virtualenv/bin/activate - activate venc
# pip3.10 install -r requirements.txt or added modules
# error codes ignore

# TODO list
# TODO make frontend JS to update ayat while on surah page visually and store changes and only access backend once when leave surah page
# TODO style acct mngmt w/ tailwind css
# add delete user button
# separate out surah name surah page like surah list - not happening with input buttons
#  add deeper shade button click colour - DONE
#  change home page for surah mem user ayah - DONE
# check for better font - DONE - i like current (original) one
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

from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float, ForeignKey, MetaData, or_, and_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List
from flask_migrate import Migrate
from flask_login import LoginManager
import datetime as dt
from zoneinfo import ZoneInfo
import availability_scheduler
import Twilio




#Needed for flask migrate - not sure why but alas
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
#



app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = "328d8ac49c90850bb64a7d6bf762354fdbcb5f72ef37d198dfccf724e2ae116f"
login_manager = LoginManager()

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=naming_convention)
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quran_data.db" #default bind
app.config["SQLALCHEMY_BINDS"] = {
    "library": "sqlite:///new-books-collection.db"
}
# app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(model_class=Base) #naming convention for flask-migrate
migrate = Migrate(app, db,render_as_batch=True)
db.init_app(app)
migrate.init_app(app, db)




# login_manager.init_app(app)






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
    surah_name_roman: Mapped[str] = mapped_column(String, nullable=False)
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
    timestamp_memorized: Mapped[int] = mapped_column(Integer)
    users_ayah: Mapped[List["MemorizationUserAyah"]] = relationship(back_populates="ayah")
    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Ayah {self.surah_no}:{self.ayah_no_surah}>'

class MemorizationUserAyah(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String)
    ayah_no_quran: Mapped[int] = mapped_column(ForeignKey("ayah.ayah_no_quran"))
    ayah_memorized: Mapped[int] = mapped_column(Integer)
    timestamp_memorized: Mapped[int] = mapped_column(Integer)
    surah_memorized: Mapped[int] = mapped_column(Integer)
    ayah: Mapped[List["Ayah"]] = relationship(back_populates="users_ayah")
    def __repr__(self):
        return f'<User Record {self.name} (ID:{self.id}) - {self.ayah}>'
    
class Patient(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)




with app.app_context(): #open the app on script run
    db.create_all()


#vibecheck

# with app.app_context(): #open the app
    # print(Twilio.fetch_messages_to_list()[-1])
    # Twilio.fetch_and_log_messages()
    # Twilio.send_message("yoo", target_phone_number="+19172008360")

@app.route('/vibecheck', methods=['GET', 'POST'])
def vibecheck():
    incoming_messages = Twilio.fetch_messages_to_list()
    return render_template("vibecheck_home.html", incoming_messages=incoming_messages)

@app.route('/vibecheck/text', methods=['GET', 'POST'])
def sms():
    incoming_messages = Twilio.fetch_messages_to_list()
    return render_template("vibecheck_text.html", incoming_messages= incoming_messages)

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
    try:
        session["username"]
    except KeyError as e:
        print ('KeyError for key: "%s" - assigning username to Ahmed' % str(e))
        session["username"] = "Ahmed"
    result = db.session.execute(db.select(MemorizationUserAyah).where(MemorizationUserAyah.ayah.has(Ayah.ayah_no_surah == 1)).where(MemorizationUserAyah.name == session["username"]))
    user_first_ayat_of_surahs = result.scalars().all()
    return render_template("memorization_home.html", user_first_ayat_of_surahs = user_first_ayat_of_surahs)

@app.route('/memorization/auth', methods=['GET', 'POST'])
def memorization_auth():
    if request.method == 'POST':
        key = list(request.form.keys())[0]
        if "username" in key:
            session['username'] = request.form['username']
        elif "new_user" in key:
            session['username'] = request.form['new_user']
            for i in range(1,6237):
                new_user_ayah = MemorizationUserAyah(name = request.form["new_user"], ayah_no_quran = i, ayah_memorized = 0, timestamp_memorized = None, surah_memorized = 0)
                db.session.add(new_user_ayah)
            db.session.commit()
        elif "delete_user" in key:
            user_to_delete = request.form["delete_user"][7:]
            print(user_to_delete)
            result = db.session.execute(db.select(MemorizationUserAyah).where(MemorizationUserAyah.name == user_to_delete))
            records_to_delete = result.scalars().all()
            for record in records_to_delete:
                db.session.delete(record)
            db.session.commit()
            return redirect(url_for('memorization_auth'))

        return redirect(url_for('memorization_home'))
    user_names_ayat = db.session.execute(db.select(MemorizationUserAyah.name))
    user_names = list(set(user_names_ayat))

    return render_template("memorization_auth.html", user_names = user_names)

@app.route('/memorization/surah/<surah_no>', methods=['GET', 'POST'])
def memorization_surah(surah_no):
    result = db.session.execute(db.select(Surah).where(Surah.surah_no == surah_no))
    surah_selected = result.scalar() 

    result = db.session.execute(db.select(MemorizationUserAyah).where(and_(Ayah.surah_no == surah_no, MemorizationUserAyah.name == session["username"])).join(Ayah, Ayah.ayah_no_quran == MemorizationUserAyah.ayah_no_quran))
    user_ayat_selected = result.scalars().all()

    now = dt.datetime.now()
    if request.method == 'POST':
        key = list(request.form.keys())[0]
        if "surah" in key:
            for user_ayah in user_ayat_selected:
                user_ayah.surah_memorized = 1 - user_ayah.surah_memorized
                user_ayah.ayah_memorized = user_ayah.surah_memorized
                user_ayah.timestamp_memorized = int(now.timestamp())
            db.session.commit()
        elif "ayah" in key:
            ayah_no = [int(s) for s in key.split("_") if s.isdigit()][0]
            user_ayah_selected = user_ayat_selected[ayah_no - 1]
            user_ayah_selected.ayah_memorized = 1 - user_ayah_selected.ayah_memorized
            user_ayah_selected.timestamp_memorized = int(now.timestamp())
            for user_ayah in user_ayat_selected:
                user_ayah.surah_memorized = calculate_surah_memorized(user_ayah_selected)
            db.session.commit()
        return redirect(url_for('memorization_surah', surah_no= surah_no))
        
            

    surah_timestamp = 0
    for user_ayah in user_ayat_selected:
        ayah_timestamp = user_ayah.timestamp_memorized or 0
        surah_timestamp = max(ayah_timestamp, surah_timestamp)
    datetime_last_updated = dt.datetime.fromtimestamp(surah_timestamp)
    datetime_last_updated = datetime_last_updated.astimezone(ZoneInfo("America/New_York")) #is utc on server est on client but somehow it works for both ?? (dev client, no prod client timezone calc done here)
    datetime_last_updated = datetime_last_updated.strftime('%B %d, %Y %I:%M %p %Z')
    return render_template("memorization_surah.html",
                           user_ayat_selected = user_ayat_selected,
                           surah_selected = surah_selected, 
                           datetime_last_updated = datetime_last_updated)


#TODO move this to separate quranmemorization file and import direct or maybe to blueprint not sure how blueprint works with non-app fxn
def calculate_surah_memorized(user_ayah):
    """ user_ayah = user_ayah"""
    surah_memorized = 1
    #for relevant surah
    for ayah in user_ayah.ayah.surah.ayat: 
    #for all users
        for users_ayah in ayah.users_ayah:
            #make sure relevant user
            if users_ayah.name == user_ayah.name:
                #if user_ayah not mem
                if users_ayah.ayah_memorized == 0:
                    #surah not mem
                    surah_memorized = 0
    return surah_memorized

def update_all_surah_memorized_manually(app=app):
    with app.test_request_context():
        result = db.session.execute(db.select(MemorizationUserAyah))
        user_ayah_list = result.scalars().all()
        for user_ayah in user_ayah_list:
            surah_memorized = 1
                #for relevant surah
            for ayah in user_ayah.ayah.surah.ayat: 
            #for all users
                for users_ayah in ayah.users_ayah:
                    #make sure relevant user
                    if users_ayah.name == user_ayah.name:
                        #if user_ayah not mem
                        if users_ayah.ayah_memorized == 0:
                            #surah not mem
                            surah_memorized = 0
            #update mem to 0 or keep as 1
            user_ayah.surah_memorized = surah_memorized
        db.session.commit()
    return




if __name__ == "__main__":
    # update_all_surah_memorized_manually()
    app.run(host='0.0.0.0', port=2000,debug=True)