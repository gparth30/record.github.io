from flask import Flask,render_template ,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
if locals():
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost:3306/db"
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost:3306/db"


db=SQLAlchemy(app)


class List(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(20), nullable=False)
    content=db.Column(db.String(500), nullable=False)
    phone=db.Column(db.String(12), nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

    def __repr__(self) ->  str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        title=request.form['title']
        content=request.form['content']
        phone=request.form['phone']
        entry=List(title=title, content=content, phone=phone)
        db.session.add(entry)
        db.session.commit()
        return redirect("/")
    alllist=List.query.all()
    return render_template('index.html', alllist=alllist)
@app.route("/delete/<int:sno>")
def delete(sno):
    list=List.query.filter_by(sno=sno).first()
    db.session.delete(list)
    db.session.commit()
    return redirect("/")
@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    list=List.query.filter_by(sno=sno).first() 
    if request.method=='POST':
        title=request.form['title']
        content=request.form['content']
        phone=request.form['phone']
        list=List.query.filter_by(sno=sno).first()
        list.title=title
        list.content=content
        list.phone=phone 
        db.session.add(list)
        db.session.commit()
        return redirect("/")   
    return render_template('update.html' , list=list)
if __name__== "__main__":
    app.run(debug=True)