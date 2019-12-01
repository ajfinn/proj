from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets
#import os
#from datetime import date
"""
dbuser = os.environ.get('DBUSER')
dbpass = os.environ.get('DBPASS')
dbhost = os.environ.get('DBHOST')
dbname = os.environ.get('DBNAME')
"""


conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

"""
class group5_wbpl_materials(db.Model):
    MaterialsID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(25))
    Creator = db.Column(db.String(25))
    YearCreated = db.Column(db.Integer)
    Genre = db.Column(db.String(25))
    MaterialType = db.Column(db.Enum("Book", "Movie", "Music", "Magazine"))
    Available = db.Column(db.Boolean)
    DateAcquired = db.Column(db.Date)
    LastModified = db.Column(db.Date)
"""

class group5_wbpl_materials(db.Model):
    MaterialsID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(25))
    Creator = db.Column(db.String(25))
    YearCreated = db.Column(db.Integer)
    Genre = db.Column(db.String(25))
    MaterialType = db.Column(db.String(25))
    Available = db.Column(db.String(10))
    DateAcquired = db.Column(db.Date)
    LastModified = db.Column(db.Date)
    
    
    def __repr__(self):
        return "id: {0} | Title: {1} | Creator: {2} | Year Created: {3} | Genre: {4} | Type: {5} | Available: {6} | Date Acquired: {7} | Last Modified: {8}".format(self.MaterialsID, self.Title, self.Creator, self.YearCreated, self.Genre, self.MaterialType, self.Available, self.DateAcquired, self.LastModified)

"""
class MaterialForm(FlaskForm):
    Title = StringField('Title:', validators = [DataRequired()])
    Creator = StringField('Creator:', validators = [DataRequired()])
    YearCreated = IntegerField('Year Created:', validators = [DataRequired()])
    Genre = StringField('Genre:', validators = [DataRequired()])
    MaterialType = SelectField('Material Type:') #validators = [DataRequired()])
    Available = SelectField('Available:') #validators = [DataRequired()])
    DateAcquired = DateField('Date Acquired:', validators = [DataRequired()])
    LastModified = DateField('Last Modified On:', validators = [DataRequired()])
"""

class MaterialForm(FlaskForm):
    Title = StringField('Title:', validators = [DataRequired()])
    Creator = StringField('Creator:', validators = [DataRequired()])
    YearCreated = IntegerField('Year Created:', validators = [DataRequired()])
    Genre = StringField('Genre:', validators = [DataRequired()])
    MaterialType = StringField('Material Type:', validators = [DataRequired()])
    Available = StringField('Available:', validators = [DataRequired()])
    DateAcquired = DateField('Date Acquired:', validators = [DataRequired()])
    LastModified = DateField('Last Modified On:', validators = [DataRequired()])
    

@app.route('/')
def index():
    all_materials = group5_wbpl_materials.query.all()
    return render_template('index.html', materials = all_materials, pageTitle = 'West Branch Public Library Catalogue')

@app.route('/search', methods=['GET', 'POST'])
def search():
        if request.method == 'POST':
            form = request.form
            search_value = form['search_string']
            search = "%{0}%".format(search_value)
            results = group5_wbpl_materials.query.filter(group5_wbpl_materials.Title.like(search)).all()
            return render_template('index.html', materials = results, pageTitle = 'West Branch Public Library Catalogue', legend="Search Results")
        else:
            return redirect('/')

@app.route('/material/new', methods =['GET', 'POST'])
def add_materials():
    form = MaterialForm()
    if form.validate_on_submit():
        material = group5_wbpl_materials(Title = form.Title.data, Creator = form.Creator.data, YearCreated = form.YearCreated.data, Genre = form.Genre.data, MaterialType = form.MaterialType.data, Available = form.Available.data, DateAcquired = form.DateAcquired.data, LastModified = form.LastModified.data)
        db.session.add(material)
        db.session.commit()
        return redirect('/')
    
    return render_template('add_materials.html', form=form, pageTitle='Add a New Material', legend="Add a New Material")


@app.route('/material/<int:material_id>', methods=['GET','POST'])
def material(material_id):
    material = group5_wbpl_materials.query.get_or_404(material_id)
    return render_template('material.html', form=material, pageTitle='Material Details')

@app.route('/material/<int:material_id>/update', methods=['GET','POST'])
def update_material(material_id):
    material = group5_wbpl_materials.query.get_or_404(material_id)
    form = MaterialForm()
    if form.validate_on_submit():
        material.Title = form.Title.data
        material.Creator = form.Creator.data
        material.YearCreated = form.YearCreated.data
        material.Genre = form.Genre.data
        material.MaterialType = form.MaterialType.data
        material.Available = form.Available.data
        material.DateAcquired = form.DateAcquired.data
        material.LastModified = form.LastModified.data
        db.session.commit()
        flash('Your material has been updated.')
        return redirect(url_for('material', material_id=material.MaterialsID))
    #elif request.method == 'GET':
    form.Title.data = material.Title
    form.Creator.data = material.Creator
    form.YearCreated.data = material.YearCreated
    form.Genre.data = material.Genre
    form.MaterialType.data = material.MaterialType
    form.Available.data = material.Available
    form.DateAcquired.data = material.DateAcquired
    form.LastModified.data = material.LastModified
    return render_template('add_materials.html', form=form, pageTitle='Update Post',
                            legend="Update A Material")
    
@app.route('/material/<int:material_id>/delete', methods=['POST'])
def delete_material(material_id):
    if request.method == 'POST': #if it's a POST request, delete the friend from the database
        material = group5_wbpl_materials.query.get_or_404(material_id)
        db.session.delete(material)
        db.session.commit()
        flash('Material was successfully deleted!')
        return redirect("/")
    else: #if it's a GET request, send them to the home page
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)