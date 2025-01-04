"""
Main App Script
"""
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

import pandas as pd

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////C:/Users/color/Workspace/finances/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///production.db'
# input(app.config['SQLALCHEMY_DATABASE_URI'])
app.config['SECRET_KEY'] = 'your_secret_key'

# C:\Users\color\Workspace\finances\app.py
db = SQLAlchemy(app)

@app.route('/', methods = ["GET"])
def home():
    """
    """
    return render_template('index.html')


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)


class ExpenseForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    source = StringField('Source', validators=[DataRequired()])
    value = FloatField('Value', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/expense', methods = ["GET", 'POST'])
def expense():
    last_date = datetime.today()

    form = ExpenseForm()
    if form.validate_on_submit():
        date = form.date.data
        category = form.category.data
        source = form.source.data
        value = form.value.data

        # Create and add new record to the database
        new_expense = Expense(
            date=date,
            category=category,
            source=source,
            value=value)
        db.session.add(new_expense)
        db.session.commit()

        last_date = date

    # Fetch all records for display
    expenses = Expense.query.all()

    return render_template('expense.html', form=form, expenses=expenses, last_date= last_date)

@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    # Query for the expense by ID
    expense = Expense.query.get_or_404(expense_id)
    
    # Delete the expense
    db.session.delete(expense)
    db.session.commit()

    return redirect(url_for('expense'))




class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)


class IncomeForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    source = StringField('Source', validators=[DataRequired()])
    value = FloatField('Value', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/income', methods = ["GET", 'POST'])
def income():
    form = IncomeForm()
    if form.validate_on_submit():
        date = form.date.data
        category = form.category.data
        source = form.source.data
        value = form.value.data

        # Create and add new record to the database
        new_income = Income(
            date=date,
            category=category,
            source=source,
            value=value)
        db.session.add(new_income)
        db.session.commit()

    # Fetch all records for display
    incomes = Income.query.all()

    return render_template('income.html', form=form, incomes=incomes)

@app.route('/delete_income/<int:income_id>', methods=['POST'])
def delete_income(income_id):
    # Query for the income by ID
    income = Income.query.get_or_404(income_id)
    
    # Delete the income
    db.session.delete(income)
    db.session.commit()

    return redirect(url_for('income'))


class TestForm(FlaskForm):
    action1 = SubmitField('Action 1') # populate the expense db table
    action2 = SubmitField('Action 2') # populate the incomes db table
    action3 = SubmitField('Action 3') # Back up the dbs

@app.route('/test',  methods = ["GET", 'POST'])
def test():
    form = TestForm()
    if form.validate_on_submit():
        if form.action1.data:
            print("Action 1")
            # Load in the Expenses Database table from the csv
            df = pd.read_csv('expenses.csv')
            print(df.to_string())
            for index, row in df.iterrows():
                d = datetime.strptime(row["Date"], "%Y-%m-%d")
                new = Expense(
                    date = d,
                    category = row["Category"],
                    source = row["Source"],
                    value = row["Amount"], 
                    )
                
                db.session.add(new)
                db.session.commit()

        elif form.action2.data:
            print("Action 2")
            # Load in the Incomes Database table from the csv
            df = pd.read_csv('incomes.csv')
            print(df.to_string())
            for index, row in df.iterrows():
                d = datetime.strptime(row["Date"], "%Y-%m-%d")
                new = Income(
                    date = d,
                    category = row["Category"],
                    source = row["Source"],
                    value = row["Amount"], 
                    )
                
                db.session.add(new)
                db.session.commit()
        elif form.action3.data:
            print("Action 3")
        # for i in range(29):print("WOWOWWEEEE")


        # # alright so I need to load in the expenses csv
        # df = pd.read_csv('expenses.csv')
        # print(df.to_string())
        # for index, row in df.iterrows():
        #     # print(row["Date"])
        #     # print(type(row["Date"]))
        #     d = datetime.strptime(row["Date"], "%Y-%m-%d")
        #     # print(d)
        #     # print(type(d))
        #     # print("")
        #     new = Expense(
        #         date = d,
        #         category = row["Category"],
        #         source = row["Source"],
        #         value = row["Amount"], 
        #         )
            
        #     db.session.add(new)
        #     db.session.commit()
        # # print(df.to_string())


        # # for row in rows:
        # db.session.add()

    return render_template('test.html', form = form)

if __name__ == '__main__':
    # Create tables within the application context
    with app.app_context():
        db.create_all()
    app.run(debug=True)
