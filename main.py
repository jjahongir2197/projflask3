from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'

db = SQLAlchemy(app)

# ================= MODELS =================

class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(
        db.String(200),
        nullable=False
    )

    age = db.Column(
        db.Integer,
        nullable=False
    )

    course = db.Column(
        db.String(100),
        nullable=False
    )

    grade = db.Column(
        db.String(10),
        nullable=False
    )

    def __repr__(self):
        return self.fullname

# ================= ROUTES =================

@app.route('/')
def home():

    students = Student.query.all()

    return render_template(
        'students.html',
        students=students
    )

@app.route('/add', methods=['GET', 'POST'])
def add_student():

    if request.method == 'POST':

        fullname = request.form['fullname']
        age = request.form['age']
        course = request.form['course']
        grade = request.form['grade']

        new_student = Student(
            fullname=fullname,
            age=age,
            course=course,
            grade=grade
        )

        db.session.add(new_student)
        db.session.commit()

        return redirect('/')

    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete_student(id):

    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):

    student = Student.query.get_or_404(id)

    if request.method == 'POST':

        student.fullname = request.form['fullname']
        student.age = request.form['age']
        student.course = request.form['course']
        student.grade = request.form['grade']

        db.session.commit()

        return redirect('/')

    return render_template(
        'edit.html',
        student=student
    )

# ================= MAIN =================

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)
