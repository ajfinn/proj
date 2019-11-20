from flask import Flask
from flask import render_template, redirect, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import pymysql
import secrets
#import os

#dbuser = os.environ.get('DBUSER')
#dbpass = os.environ.get('DBPASS')
#dbhost = os.environ.get('DBHOST')
#dbname = os.environ.get('DBNAME')

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)

class group5_wbpl_materials(db.Model):
    MaterialsID = db.Column(db.String(15), primary_key=True)
    Title = db.Column(db.String(255))
    Creator = db.Column(db.String(255))
    YearCreated = db.Column(db.String(255))
    Genre = db.Column(db.String(255))
    MaterialType = db.Column(db.String(255))
    Available = db.Column(db.Boolean(True))
    DateAcquired = db.Column(db.Date())
    LastModified = db.Column(db.Date())



class MaterialsForm(FlaskForm):
    Title = StringField('Title:', validators=[DataRequired()])
    Creator = StringField('Creator:', validators=[DataRequired()])
    YearCreated = StringField('Year Created:', validators=[DataRequired()])
    Genre = StringField('Genre:', validators=[DataRequired()])
    MaterialType = StringField('MaterialType:', validators=[DataRequired()])
    Available = StringField('Available:', validators=[DataRequired()])
    DateAcquired = StringField('Date Acquired:', validators=[DataRequired()])
    LastModified = StringField('Last Modified:', validators=[DataRequired()])

@app.route('/')
def index():
    all_materials = group5_wbpl_materials.query.all()
    return render_template('index.html', material=all_materials, pageTitle="materials")

@app.route('/add_materials', methods=['GET','POST'])
def add_materials():
    form = MaterialsForm()
    avl = ['True', 'False']
    mtype = ['Book', 'Movie', 'Music', 'Magazine']
    if form.validate_on_submit():
        material = group5_wbpl_materials(Title=form.Title.data, Creator=form.Creator.data, YearCreated = form.YearCreated.data, Genre = form.Genre.data, MaterialType = form.MaterialType.data, Available = form.Available.data, DateAcquired=form.DateAcquired.data, LastModified=form.LastModified.data)
        db.session.add(material)
        db.session.commit()
        return redirect('/')

    return render_template('add_materials.html', form=form, pageTitle='Add materials')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        print('post method')
        form = request.form
        search_value = form['search_string']
        print(search_value)
        search = "%{0}%".format(search_value)
        print(search)
        results = group5_wbpl_materials.query.filter(or_(group5_wbpl_materials.Title.like(search), group5_wbpl_materials.Creator.like(search), group5_wbpl_materials.Genre.like(search))).all()
        print(results)
        return render_template('index.html', material = results, pageTitle='West Branch Public Library\'s materials', legend="Search Results")
    else:
        return redirect('/')

@app.route('/delete_material/<int:MaterialsID>', methods=['GET','POST'])
def delete_material(MaterialsID):
    if request.method == 'POST': #if it's a POST request, delete the friend from the database
        obj = group5_wbpl_materials.query.get_or_404(MaterialsID)
        db.session.delete(obj)
        db.session.commit()
        flash('Material was successfully deleted!')
        return redirect("/")

    else: #if it's a GET request, send them to the home page
        return redirect("/")

@app.route('/materials/<int:MaterialsID>', methods=['GET', 'POST'])
def get_material(MaterialsID):
    material = group5_wbpl_materials.query.get_or_404(MaterialsID)
    return render_template('materials.html', form=material, pageTitle = 'Materials')

@app.route('/materials/<int:MaterialsID>/update', methods=['GET', 'POST'])
def update_material(MaterialsID):
    material = group5_wbpl_materials.query.get_or_404(MaterialsID)
    form = MaterialsForm()
    if form.validate_on_submit():
        material.Title = form.Title.data
        material.Creator = form.Creator.data
        material.YearCreated = form.YearCreated.data
        material.Genre = form.Genre.data
        material.MaterialType = form.MaterialType.data
        material.Available = form.Available.data
        material.DateAcquired = form.DateAcquired.data
        material.LastModified = form.LastModified.data
        return redirect(url_for('get_material', MaterialsID = MaterialsID))
    form.Title.data = material.Title
    form.Creator.data = material.Creator
    form.YearCreated.data = material.YearCreated
    form.Genre.data = material.Genre
    form.MaterialType.data = material.MaterialType
    form.Available.data = material.Available
    form.DateAcquired.data = material.DateAcquired
    form.LastModified.data = material.LastModified
    return render_template('update_materials.html', form = form, pageTitle='Updated Materials')


if __name__ == '__main__':
    app.run(debug==False)
