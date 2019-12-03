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

class group5_wbpl_patrons(db.Model):
    patron_id = db.Column(db.Integer, primary_key=True)
    First_Name = db.Column(db.String(25))
    Last_Name = db.Column(db.String(25))
    Email = db.Column(db.String(50))
    Phone = db.Column(db.String(15))
    Address = db.Column(db.String(100))
    City = db.Column(db.String(25))
    State = db.Column(db.String(2))
    Zipcode = db.Column(db.String(5))
    Birthdate = db.Column(db.Date)
    created_at = db.Column(db.Date)


    def __repr__(self):
        return "id: {0} | First Name: {1} | Last Name: {2} | Email: {3} | Phone: {4} | Address: {5} | City: {6} | State: {7} | Zipcode: {8} | Birthdate: {9} | Created: {10}".format(self.patron_id, self.First_Name, self.Last_Name, self.Email, self.Phone, self.Address, self.City, self.State, self.Zipcode, self.Birthdate, self.created_at)

class group5_wbpl_circulation(db.Model):
    circulation_id = db.Column(db.Integer, primary_key=True)
    patron_id = db.Column(db.Integer, foreign_key=True)
    MaterialsID = db.Column(db.Integer, foreign_key=True)
    checked_out = db.Column(db.Boolean)
    title = db.Column(db.String)
    material_type = db.Column(db.String)
    checkout_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    
    def __repr__(self):
        return "CirculationID: {0} | PatronID: {1} | MaterialID: {2} | Checked Out: {3} | Title: {4} | Material Type: {5} | Checkout Date: {6} | Due Date: {7}".format(self.circulation_id, self.patron_id, self.MaterialsID, self.checked_out, self.title, self.material_type, self.checkout_date, self.due_date)
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

class PatronForm(FlaskForm):
    First_Name = StringField('First Name:', validators = [DataRequired()])
    Last_Name = StringField('Last Name', validators = [DataRequired()])
    Email = StringField('Email', validators = [DataRequired()])
    Phone = StringField('Phone', validators = [DataRequired()])
    Address = StringField('Address', validators = [DataRequired()])
    City = StringField('City:', validators = [DataRequired()])
    State = StringField('State:', validators = [DataRequired()])
    Zipcode = StringField('Zipcode:', validators = [DataRequired()])
    Birthdate = StringField('Birthdate:', validators = [DataRequired()])
    created_at = StringField('Created on:', validators = [DataRequired()])

class CirculationForm(FlaskForm):
    patron_id = IntegerField('Patron ID:', validators = [DataRequired()])
    MaterialsID = IntegerField('Material ID:', validators = [DataRequired()])
    checked_out = StringField('Checked Out:', validators = [DataRequired()])
    title = StringField('Title:', validators = [DataRequired()])
    material_type = StringField('Material Type:', validators = [DataRequired()])
    checkout_date = DateField('Checkout Date:', validators = [DataRequired()])
    due_date = DateField('Due Date:', validators = [DataRequired()])

@app.route('/')
def index():
    return render_template('index.html', pageTitle = 'West Branch Public Library')


@app.route('/AllMaterials', methods=['GET', 'POST'])
def AllMaterials():
    all_materials = group5_wbpl_materials.query.all()
    return render_template('AllMaterials.html', materials = all_materials, pageTitle = 'West Branch Public Library Catalogue')

@app.route('/searchMaterials', methods=['GET', 'POST'])
def searchMaterials():
        if request.method == 'POST':
            form = request.form
            search_value = form['search_string']
            search = "%{0}%".format(search_value)
            results = group5_wbpl_materials.query.filter(group5_wbpl_materials.Title.like(search)).all()
            return render_template('AllMaterials.html', materials = results, pageTitle = 'West Branch Public Library Catalogue', legend="Search Results")
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
        return redirect(url_for('AllMaterials', material_id=material.MaterialsID))
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
        return redirect("/AllMaterials")
    else: #if it's a GET request, send them to the home page
        return redirect("/AllMaterials")


@app.route('/AllPatrons', methods=['GET', 'POST'])
def AllPatrons():
    all_patrons = group5_wbpl_patrons.query.all()
    return render_template('AllPatrons.html', patrons = all_patrons, pageTitle = 'West Branch Public Library Patrons')

@app.route('/searchPatrons', methods=['GET', 'POST'])
def searchPatrons():
        if request.method == 'POST':
            form = request.form
            search_value = form['search_string']
            search = "%{0}%".format(search_value)
            results = group5_wbpl_patrons.query.filter(group5_wbpl_patrons.First_Name.like(search)).all()
            return render_template('AllPatrons.html', patrons = results, pageTitle = 'West Branch Public Library Patrons', legend="Search Results")
        else:
            return redirect('/')

@app.route('/patron/<int:patron_id>', methods=['GET','POST'])
def patron(patron_id):
    patron = group5_wbpl_patrons.query.get_or_404(patron_id)
    return render_template('patron.html', form=patron, pageTitle='Patron Details')

@app.route('/patron/<int:material_id>/update', methods=['GET','POST'])
def update_patron(patron_id):
    patron = group5_wbpl_patrons.query.get_or_404(patron_id)
    form = PatronForm()
    if form.validate_on_submit():
        patron.First_Name = form.First_Name.data
        patron.Last_Name = form.Last_Name.data
        patron.Email = form.Email.data
        patron.Phone = form.Phone.data
        patron.Address = form.Address.data
        patron.City = form.City.data
        patron.State = form.State.data
        patron.Zipcode = form.Zipcode.data
        patron.Birthdate = form.Birthdate.data
        patron.created_at = form.created_at.data
        db.session.commit()
        flash('Patron has been updated.')
        return redirect(url_for('AllPatrons', patron_id=patron.patron_id))
    #elif request.method == 'GET':
    form.First_Name.data = patron.First_Name
    form.Last_Name.data = patron.Last_Name
    form.Email.data = patron.Email
    form.Phone.data = patron.Phone
    form.Address.data = patron.Address
    form.City.data = patron.City
    form.State.data = patron.State
    form.Zipcode.data = patron.Zipcode
    form.Birthdate.data = patron.Birthdate
    form.created_at.data = patron.created_at
    return render_template('add_patrons.html', form=form, pageTitle='Update Patron',
                            legend="Update A Patron")


@app.route('/patron/<int:patron_id>/delete', methods=['POST'])
def delete_patron(patron_id):
    if request.method == 'POST': #if it's a POST request, delete the friend from the database
        patron = group5_wbpl_patrons.query.get_or_404(patron_id)
        db.session.delete(patron)
        db.session.commit()
        flash('Patron was successfully deleted!')
        return redirect("/AllPatrons")
    else: #if it's a GET request, send them to the home page
        return redirect("/AllPatrons")
    
@app.route('/AllCirculations', methods=['GET', 'POST'])
def AllCirculations():
    all_circulations = group5_wbpl_circulation.query.all()
    return render_template('AllCirculations.html', circulations = all_circulations, pageTitle = 'West Branch Public Library Circulations')

@app.route('/Check_Out', methods =['GET', 'POST'])
def check_out():
    form = CirculationForm()
    if form.validate_on_submit():
        circulation = group5_wbpl_circulation(checked_out = form.checked_out.data, title = form.title.data, material_type = form.material_type.data, checkout_date = form.checkout_date.data, due_date = form.due_date.data)
        db.session.add(circulation)
        db.session.commit()
        return redirect('/AllCirculations')
    
    return render_template('Check_Out.html', form=form, pageTitle='Check-out Material', legend="Check-Out")

@app.route('/Check_In', methods =['GET', 'POST'])
def check_in():
    form = CirculationForm()
    if form.validate_on_submit():
        circulation = group5_wbpl_circulation(checked_out = form.checked_out.data, title = form.title.data, material_type = form.material_type.data, checkout_date = form.checkout_date.data, due_date = form.due_date.data)
        db.session.add(circulation)
        db.session.commit()
        return redirect('/AllCirculations')
    
    return render_template('Check_In.html', form=form, pageTitle='Check-In Material', legend="Check-In")


if __name__ == '__main__':
    app.run(debug=True)
