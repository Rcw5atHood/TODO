from flask import Flask, render_template, request, redirect
from models import db, StudentModel
import urllib.request
import json
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)



@app.before_first_request
def create_table():
    #db.drop_all()
    db.create_all()


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        skillset = request.form.getlist('skillset')
        skillset = " | ".join(map(str, skillset))
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        skillset = skillset
        focus = request.form['focus']
        students = StudentModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            gender=gender,
            skillset=skillset,
            focus=focus
        )
        db.session.add(students)
        db.session.commit()
        return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def retrieveList():
    global students
    if request.method == 'POST':
        if request.form.get('AtoZ') == 'Sort By Last Name A to Z':
            students = StudentModel.query.order_by(StudentModel.last_name).all()
        elif request.form.get('ZtoA') == 'Z-A':
            students = StudentModel.query.order_by(StudentModel.last_name.desc()).all()
    elif request.method == 'GET':
        students = StudentModel.query.order_by(StudentModel.last_name).all()
    return render_template('datalist.html', students=students)


@app.route('/<int:id>')
def retrieveStudent(id):
    students = StudentModel.query.filter_by(id=id).first()
    if students:
        return render_template('datalist.html', students=students)
    return f"Employee with id ={id} Doesnt exist"


@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def update(id):
    student = StudentModel.query.filter_by(id=id).first()

    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()

        skillset = request.form.getlist('skillset')
        skillset = " | ".join(map(str, skillset))
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        skillset = skillset
        focus = request.form['focus']

        student = StudentModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            gender=gender,
            skillset=skillset,
            focus=focus
        )
        db.session.add(student)
        db.session.commit()
        return redirect('/')
        # return f"Student with id = {id} Does not exist"

    return render_template('update.html', student=student)


@app.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    students = StudentModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if students:
            db.session.delete(students)
            db.session.commit()
            return redirect('/')
        # abort(404)
    # return redirect('/')
    return render_template('delete.html')


@app.route("/")
def get_movies():
    url = "https://api.themoviedb.org/3/discover/movie?api_key={}".format(os.environ.get("TMDB_API_KEY"))
    print(os.environ.get("TMDB_API_KEY"))
    response = urllib.request.urlopen(url)
    data = response.read()
    jsondata = json.loads(data)

    return render_template("movies.html", movies=jsondata["results"])


@app.route("/movies")
def get_movies_list():
    url = "https://api.themoviedb.org/3/movie/popular?api_key=18a017b1725a276ac9a9838ec5345147"

    response = urllib.request.urlopen(url)
    data = response.read()
    jsondata = json.loads(data)

    movie_json = []

    for movie in jsondata["results"]:
        movie = {
            "title": movie["title"],
            # "overview": movie["overview"], this eliminates the massive wall of text to just movie titles
        }

        movie_json.append(movie)
    print(movie_json)
    return render_template("allmovies.html", titles=movie_json)
    # return {"movie title": movie_json}


if __name__ == '__main__':
    app.run(debug=True)

app.run(host='localhost', port=5000)
