from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets
#import os
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


class ewestby_animalsapp(db.Model):
    animalID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Country = db.Column(db.String(255))
    Weight = db.Column(db.Integer)
    Quantity = db.Column(db.Integer)
    
    def __repr__(self):
        return "id: {0} | Name: {1} | Country: {2} | Weight: {3} | Quantity: {4}".format(self.id, self.iName, self.Country, self.Weight, self.Quantity)


class AnimalForm(FlaskForm):
    Name = StringField('Animal Name:', validators=[DataRequired()])
    Country = StringField('Country:', validators = [DataRequired()])
    Weight = IntegerField('Weight:', validators = [DataRequired()])
    Quantity = IntegerField('Quantity:', validators = [DataRequired()])
    

@app.route('/')
def index():
    all_animals = ewestby_animalsapp.query.all()
    return render_template('index.html', animals = all_animals, pageTitle = 'Eric\'s Animals')

@app.route('/search', methods=['GET', 'POST'])
def search():
        if request.method == 'POST':
            form = request.form
            search_value = form['search_string']
            search = "%{0}%".format(search_value)
            results = ewestby_animalsapp.query.filter(ewestby_animalsapp.Country.like(search)).all()
            return render_template('index.html', animals = results, pageTitle = 'Eric\'s Animals', legend="Search Results")
        else:
            return redirect('/')

@app.route('/animal/new', methods =['GET', 'POST'])
def add_animal():
    form = AnimalForm()
    if form.validate_on_submit():
        animal = ewestby_animalsapp(Name = form.Name.data, Country = form.Country.data, Weight = form.Weight.data, Quantity = form.Quantity.data)
        db.session.add(animal)
        db.session.commit()
        return redirect('/')
    
    return render_template('add_animal.html', form=form, pageTitle='Add a New Animal', legend="Add a New Animal")


@app.route('/animal/<int:animal_id>', methods=['GET','POST'])
def animal(animal_id):
    animal = ewestby_animalsapp.query.get_or_404(animal_id)
    return render_template('animal.html', form=animal, pageTitle='Animal Details')

@app.route('/animal/<int:animal_id>/update', methods=['GET','POST'])
def update_animal(animal_id):
    animal = ewestby_animalsapp.query.get_or_404(animal_id)
    form = AnimalForm()
    if form.validate_on_submit():
        animal.Name = form.Name.data
        animal.Country = form.Country.data
        animal.Weight = form.Weight.data
        animal.Quantity = form.Quantity.data
        db.session.commit()
        flash('Your animal has been updated.')
        return redirect(url_for('animal', animal_id=animal.animalID))
    #elif request.method == 'GET':
    form.Name.data = animal.Name
    form.Country.data = animal.Country
    form.Weight.data = animal.Weight
    form.Quantity.data = animal.Quantity
    return render_template('add_animal.html', form=form, pageTitle='Update Post',
                            legend="Update An Animal")
    
@app.route('/animal/<int:animal_id>/delete', methods=['POST'])
def delete_animal(animal_id):
    if request.method == 'POST': #if it's a POST request, delete the friend from the database
        animal = ewestby_animalsapp.query.get_or_404(animal_id)
        db.session.delete(animal)
        db.session.commit()
        flash('Animal was successfully deleted!')
        return redirect("/")
    else: #if it's a GET request, send them to the home page
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)