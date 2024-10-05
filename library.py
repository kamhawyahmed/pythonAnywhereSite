from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)


class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'

with app.app_context(): #open the app
    db.create_all()

@app.route('/', methods=["GET","POST"])
def home():
    #all books
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars()
    all_books = list(db.session.execute(db.select(Book).order_by(Book.title)).scalars())
    # book = db.session.execute(db.select(Book).where(Book.title == "Harry Potter")).scalar()
    book_to_find = None
    if request.method == "POST":
        book_to_find = db.session.execute(db.select(Book).where(Book.title == request.form["title"])).scalar()
    return render_template("library_index.html", book_list=all_books, book_to_find=book_to_find)


@app.route("/add", methods=['GET','POST'])
def add():
    if request.method == "POST":
        new_book_db_entry = Book(title = request.form["title"], author = request.form["author"], rating = request.form["rating"])
        db.session.add(new_book_db_entry)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("library_add.html")

@app.route("/update/<id>", methods=['GET','POST'])
def update(id):
    if request.method == "POST":
        #book_to_update = db.get_or_404(Book, id)
        book_to_update = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
    return render_template("library_update.html", book=book)

@app.route("/delete/<id>", methods=['GET'])
def delete(id):
    book_to_delete = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


# with app.test_request_context():
#     print(url_for('update', username='John-Doe'))


if __name__ == "__main__":
    app.run(debug=True)