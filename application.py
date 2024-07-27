from flask import Flask, request
from Flask_SQLAlchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), nullable=False)
    publisher = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"


@app.route('/')
def index():
    return 'Hello!'


@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()

    output = []
    for book in books:
        book_data = {'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher}
        output.append(book_data)

    return {"books": output}


@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"id": book.id, "book_name": book.book_name, "author": book.author, "publisher": book.publisher}


@app.route('/books', methods=['POST'])
def add_book():
    book_data = request.get_json()
    new_book = Book(book_name=book_data['book_name'], author=book_data['author'], publisher=book_data['publisher'])
    db.session.add(new_book)
    db.session.commit()
    return {'id': new_book.id}


@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    book_data = request.get_json()

    book.book_name = book_data['book_name']
    book.author = book_data['author']
    book.publisher = book_data['publisher']

    db.session.commit()
    return {"message": "Book updated"}


@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return {"message": "Book deleted"}


if __name__ == '__main__':
    app.run(debug=True)
