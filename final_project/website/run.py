from flask import Flask, render_template, request
import sys
import json
from operator import itemgetter

app = Flask(__name__)

genres = ['Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary',
          'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
          'Thriller', 'War', 'Western']

poll_data = {
   'question' : 'Which kinds of movie do you like?',
   'genres'   : genres
}

with open("./resource/movie_filter.json", 'r', encoding="utf8") as f:
    genres2movie = json.load(f, encoding="utf8")

with open("./resource/movie_infor.json", 'r', encoding="utf8") as f:
    movies2infor = json.load(f, encoding="utf8")

# name = "Ping.txt"

count_profile = 0
count_survey = 0

# root pages, render to index.html
@app.route('/')
def root():
    return render_template('index.html', data=poll_data)

@app.route('/poll')
def poll():

    name = request.args.get('name')

    vote = request.args.getlist('genres')

    print(name, file=sys.stderr)

    if len(vote) == 0:
        # Recommend best rating from all movies

        print("None", file=sys.stderr)

        movie2r = [(key, value['rating_ave'], value['rating_cnt']) for key, value in movies2infor.items()]
        sorted_movie2r = sorted(movie2r, key=itemgetter(2,1), reverse=True)

        top1_movie = sorted_movie2r[0]

        out = open(name, 'a')
        out.write(str(top1_movie) + '\n')
        out.close()

    else:
        # Recommend best rating from given genres

        print("Yes", file=sys.stderr)

        candidates = []

        for v in vote:
            candidates.extend(genres2movie[v])

        candidates = list(set(candidates))
        movie2r = [(key, movies2infor[key]['rating_ave'], movies2infor[key]['rating_cnt']) for key in candidates]
        sorted_movie2r = sorted(movie2r, key=itemgetter(2, 1), reverse=True)

        top1_movie = sorted_movie2r[0]

        out = open(name, 'a')
        out.write(str(top1_movie) + '\n')
        out.close()

        data_single_movie = movies2infor[top1_movie[0]].copy()
        data_single_movie['title'] = top1_movie[0]

    count_profile += 1

    return render_template('vote.html', data=data_single_movie)

@app.route('/starter')
def starter():




    return render_template('vote.html', data=data_single_movie)

if __name__ == "__main__":

    app.run(debug=True)