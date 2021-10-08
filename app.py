# emv/Script/activate.ps1 (to activate your virtual environment)
from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)


class Todo(db.Model):

    # global title
    sno= db.Column(db.Integer ,primary_key=True)
    title=db.Column(db.String(200) ,nullable=False)
    desc=db.Column(db.String(2000) ,nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        print("post")
        title =request.form['title']
        desc =request.form['desc']
        # print(request.form['title'])

        todo=Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    # print(allTodo)
    return render_template('index.html', allTodo=allTodo)

@app.route('/delete/<int:sno>')
def products(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    # print(allTodo)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title =request.form['title']
        desc =request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
    # return 'This is products'

# @app.route('/')
# def delete():
#     return 'This is products'

if __name__=="__main__":
    app.run(debug=True)
