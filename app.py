from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os
from datetime import datetime, timezone

app = Flask(__name__)

# Configure PostgreSQL Database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_user:Taco!995@localhost/prospects'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a model for storing the employee form data
class prospects(db.Model):
    __tablename__ = 'prospects'  # Specify table name
    employee_id = db.Column(db.String(8), primary_key=True)  # Custom employee ID
    ssn = db.Column(db.String(11), nullable=False, unique=True)  # Ensure SSN is unique
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    craft = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    nccer = db.Column(db.String(20), nullable=False)  # Yes or No for NCCER
    date_available = db.Column(db.String(10), nullable=False)

    # Use timezone-aware datetime for timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

# Create the PostgreSQL database tables
with app.app_context():
    db.create_all()

# Read crafts from CSV file using pandas
def get_crafts_from_csv():
    csv_path = os.path.join(app.root_path, 'static', 'data', 'craft.csv')
    try:
        df = pd.read_csv(csv_path)
        crafts = df['craft'].tolist()  # Ensure the column name is correct
        return crafts
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

@app.route('/')
def index():
    crafts = get_crafts_from_csv()  # Load crafts from the CSV file
    return render_template('prospects_form.html', crafts=crafts)

@app.route('/get_crafts')
def get_crafts():
    crafts = get_crafts_from_csv()
    return jsonify(crafts)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        ssn = request.form['ssn']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        craft = request.form['craft']
        phone = request.form['phone']
        email = request.form['email']
        nccer = request.form['nccer']
        date_available = request.form['date_available']

        # Generate employee ID (first 4 letters of last name in uppercase + last 4 digits of SSN)
        employee_id = last_name[:4].upper() + ssn[-4:]

        # Check if an employee with the same SSN already exists
        existing_employee = prospects.query.filter_by(ssn=ssn).first()

        if existing_employee:
            # Update existing record
            existing_employee.first_name = first_name
            existing_employee.last_name = last_name
            existing_employee.craft = craft
            existing_employee.phone = phone
            existing_employee.email = email
            existing_employee.nccer = nccer
            existing_employee.date_available = date_available
            existing_employee.employee_id = employee_id
            db.session.commit()
        else:
            # Insert new record
            new_employee = prospects(
                employee_id=employee_id,
                ssn=ssn,
                first_name=first_name,
                last_name=last_name,
                craft=craft,
                phone=phone,
                email=email,
                nccer=nccer,
                date_available=date_available
            )
            db.session.add(new_employee)
            db.session.commit()

        return redirect('/')




if __name__ == '__main__':
    app.run(debug=True)

