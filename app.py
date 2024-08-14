from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client['Library_management']
collection = db['books']

@app.route('/')
def index():
    books = collection.find()
    return render_template('index.html', books=books)

@app.route('/borrow_book', methods=['POST'])
def borrow_book():
    if request.method == 'POST':
        member_id = request.form['memberId']
        book_title = request.form['bookTitle']
        book_author = request.form['bookAuthor']
        
        collection.update_one({'title': book_title, 'author': book_author}, {'$inc': {'Copies': -1}})
        return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    copies = int(request.form['copies'])
    collection.insert_one({'Title': title, 'Author': author, 'Copies': copies})
    return redirect(url_for('index'))

@app.route('/delete/<book_id>')
def delete_book(book_id):
    collection.delete_one({'_id': ObjectId(book_id)})
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)