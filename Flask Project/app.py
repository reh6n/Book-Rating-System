
from flask import Flask, render_template, request
import pickle
import numpy as np


popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)



@app.route("/")
def index():
    return render_template('index.html', 
                    book_name = list(popular_df['Book-Title']),
                    book_author = list(popular_df['Book-Author']),
                    img_url = list(popular_df['Image-URL-L']),
                    voter = list(popular_df['Number_Rating']),
                    rating = list(round(popular_df['Average_Rating'], 2))
    )

@app.route('/recommend')
def recommend():
    return render_template('rec.html')

@app.route('/recommend_books', methods=['post'])
def recommend_books():
    requested_name = request.form.get('requested_name')
    index = np.where(pt.index==requested_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda X:X[1], reverse=True)[0:10]

    data =  []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    # print(data)

    return render_template('rec.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

