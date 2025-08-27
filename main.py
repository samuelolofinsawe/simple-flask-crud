import datetime
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task.db"
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)
class Task(db.Model):
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    content:Mapped[str]=mapped_column(String,nullable=False)
    completed:Mapped[bool]=mapped_column(Boolean,default=False)
    created_at:Mapped[datetime]=mapped_column(DATETIME,default=datetime.datetime.now(datetime.UTC))
with app.app_context():
    db.create_all()
@app.route("/")
def home():
    task = Task.query.all()
    return render_template("index.html",tasks=task)
@app.route("/add",methods=["POST","GET"])
def adding_task():
        if request.method == "GET":
            return render_template("add_task.html")
        elif request.method == "POST":
            task= Task(
                content=request.form["title"]
            )
            db.session.add(task)
            db.session.commit()

            return redirect("/")
@app.route("/edit/<int:task_ident>",methods=["POST","GET"])
def edit_task(task_ident):
    task=Task.query.get_or_404(task_ident)
    if request.method == "GET":
        return render_template("edit.html",taskinfo=task)
    elif request.method == "POST":
        task.content = request.form["title"]
        print(task.content)
        db.session.commit()
        return redirect("/")
@app.route("/delete/<int:task_ident>",methods=["POST","GET"])
def delete_task(task_ident):
    task=Task.query.get_or_404(task_ident)
    if request.method == "GET":
        return render_template("delete.html")
    if request.method == "POST":
        db.session.delete(task)
        db.session.commit()
        return redirect("/")




if __name__ == "__main__":
    app.run(debug=True)