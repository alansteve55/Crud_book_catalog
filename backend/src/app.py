from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId  # Import to handle ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/crudapp'
mongo = PyMongo(app)

CORS(app)

db = mongo.db.books

@app.route('/books', methods=['POST'])
def addbook():
    # Insert data into MongoDB
    result = db.insert_one({
        'title': request.json['title'],
        'author': request.json['author'],
        'published_date': request.json['published_date'],
        'isbn': request.json['isbn'],
        'genre': request.json['genre'],
    })
    
    # Return the ID of the inserted document
    return jsonify({'id': str(result.inserted_id), 'msg': "New Book added successfully"}), 201

@app.route('/books', methods=['GET'])
def getbook():
    books = []
    for doc in db.find():
        books.append({
            'id': str(doc['_id']),  # Convert ObjectId to string and return as id
            'title': doc['title'],
            'author': doc['author'],
            'published_date': doc['published_date'],
            'isbn': doc['isbn'],
            'genre': doc['genre'],
        })
    return jsonify(books)

@app.route('/book/<id>', methods=['GET'])
def getbookbyid(id):
    book = db.find_one({'_id': ObjectId(id)})
    if book:
        return jsonify({
            'id': str(book['_id']),  # Convert ObjectId to string and return as id
            'title': book['title'],
            'author': book['author'],
            'published_date': book['published_date'],
            'isbn': book['isbn'],
            'genre': book['genre'],
        })
    else:
        return jsonify({'error': 'Book not found'}), 404
    
@app.route('/book/<id>', methods=['DELETE'])
def deletebook(id):
    result = db.delete_one({'_id': ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({'msg': "Book deleted successfully"})
    else:
        return jsonify({'error': "Book not found"}), 404
    
@app.route('/book/<id>', methods=['PUT'])
def updatebook(id):
    # Find the book by its ID and update the fields
    result = db.update_one(
        {'_id': ObjectId(id)},
        {'$set': {
            'title': request.json['title'],
            'author': request.json['author'],
            'published_date': request.json['published_date'],
            'isbn': request.json['isbn'],
            'genre': request.json['genre']
        }}
    )
    # Check if the update was successful
    if result.matched_count > 0:
        return jsonify({'msg': "Book updated successfully"})
    else:
        return jsonify({'error': "Book not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
