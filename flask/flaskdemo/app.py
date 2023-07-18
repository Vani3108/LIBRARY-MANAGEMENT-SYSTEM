from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
db = "database.db"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    if request.method == 'POST':
        # Add a new book
        book_name = request.form['book_name']
        author_name = request.form['author_name']
        quantity = request.form['quantity']

        cursor.execute('INSERT INTO books (book_name, author_name, quantity) VALUES (?, ?, ?)',
                       (book_name, author_name, quantity))
        conn.commit()

    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()

    return render_template('books.html', books=books)

@app.route('/members', methods=['GET', 'POST'])
def members():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    if request.method == 'POST':
        # Add a new member
        member_name = request.form['member_name']
        cursor.execute('INSERT INTO members (member_name) VALUES (?)', (member_name,))
        conn.commit()

    cursor.execute('SELECT * FROM members')
    members = cursor.fetchall()
    conn.close()

    return render_template('members.html', members=members)

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    if request.method == 'POST':
        # Issue/return a book
        book_id = request.form['book_id']
        member_id = request.form['member_id']
        is_returned = request.form['is_returned']

        if is_returned == '0':
            # Issue a book
            cursor.execute('INSERT INTO transactions (book_id, member_id) VALUES (?, ?)',
                           (book_id, member_id))
        else:
            # Return a book
            cursor.execute('UPDATE transactions SET is_returned = 1 WHERE book_id = ? AND member_id = ?',
                           (book_id, member_id))

        conn.commit()

    cursor.execute('SELECT transactions.id, books.book_name, members.member_name, transactions.is_returned '
                   'FROM transactions '
                   'INNER JOIN books ON transactions.book_id = books.id '
                   'INNER JOIN members ON transactions.member_id = members.id')
    transactions = cursor.fetchall()
    conn.close()

    return render_template('transactions.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
