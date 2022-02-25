from flask import Flask,render_template,request
from mini import _genre_,release_date,_top_,similar,_info_,all_movies
app = Flask(__name__)

@app.route('/')
def home():
    top_movies,top_rate,top_genres=_top_()
    all=all_movies()
    return render_template('mini_page.html',top_movies=top_movies,top_rate=top_rate ,top_genres=top_genres,all=all)
@app.route('/gen')
def next():
    return render_template("genre.html",movies=[],rate=[])
@app.route('/date')
def next1():
    return render_template("year.html",movies=[],rate=[])
@app.route('/data',methods=['POST'])
def get_data():
        name=request.form['name']
        movies,rate=_genre_(name)
        return render_template('genre.html',movies=movies,rate=rate)
@app.route('/data1',methods=['POST'])
def get_data1():
    years=request.form['years']
    movies,rate=release_date(int(years))
    return render_template('year.html',movies=movies,rate=rate)
@app.route('/detail/<Movie_Name>',methods=['GET'])
def get_detail(Movie_Name):
    det=_info_(Movie_Name)
    sim,vote=similar(Movie_Name,0)
    return render_template("details.html" ,det=det,sim=sim,vote=vote) 
@app.route('/data2',methods=['POST'])
def movie_details():
    name=request.form['Search']
    name1=_info_(name)
    sim,vote=similar(name,0)
    return render_template('by_name.html' ,name1=name1,sim=sim,vote=vote) 
if __name__ =='__main__':
    app.run(debug=True)