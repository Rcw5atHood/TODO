from flask import Flask, render_template, request, redirect
from models import db, StudentModel
import urllib.request, json
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        hobby = request.form.getlist('hobbies')
        # hobbies = ','.join(map(str, hobby))
        hobbies = ",".join(map(str, hobby)) # this line lets it be comma sep value tv, movie etc

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        hobbies = hobbies
        country = request.form['country']
        students = StudentModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            gender=gender,
            hobbies=hobbies,
            country=country
        )
        db.session.add(students)
        db.session.commit()
        return redirect('/')


@app.route('/')
def RetrieveList():
    students = StudentModel.query.order_by(StudentModel.last_name).all()
    print(students)
    return render_template('datalist.html', students=students)


@app.route('/<int:id>')
def RetrieveStudent(id):
    students = StudentModel.query.filter_by(id=id).first()
    if students:
        return render_template('data.html', students=students)
    return f"Employee with id ={id} Doenst exist"


@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def update(id):
    student = StudentModel.query.filter_by(id=id).first()

    # hobbies = student.hobbies.split(' ')
    # print(hobbies)
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
        #     tv = request.form['tv']
        #     if tv is None:
        #               pass

        #    # print('Form:' + str(request.form))

        #     cricket = request.form['cricket']
        #     movies = request.form['movies']
        #     hobbies = tv + ' ' +  cricket + ' ' + movies
        #     print('H' + hobbies)
        hobby = request.form.getlist('hobbies')
        # hobbies = ','.join(map(str, hobby))
        hobbies = ",".join(map(str, hobby))
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        hobbies = hobbies
        country = request.form['country']

        student = StudentModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            gender=gender,
            hobbies=hobbies,
            country=country
        )
        db.session.add(student)
        db.session.commit()
        return redirect('/')
        return f"Student with id = {id} Does not exist"

    return render_template('update.html', student=student)


@app.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    students = StudentModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if students:
            db.session.delete(students)
            db.session.commit()
            return redirect('/')
        #abort(404)
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
    #return {"movie title": movie_json}
if __name__ == '__main__':
    app.run(debug=True)

app.run(host='localhost', port=5000)
