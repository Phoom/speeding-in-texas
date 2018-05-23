import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template

app = Flask(__name__)

#################################################
# Database Setup
#################################################
dbfile = os.path.join('speeding.sqlite')
engine = create_engine(f"sqlite:///{dbfile}")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Crashes = Base.classes.crashes
Demographics = Base.classes.demographics

# Create our session (link) from Python to the DB
session = Session(engine)

@app.route("/")
def index():
    """Return the homepage."""
    return render_template('index.html')


@app.route('/years')
def carYears():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    stmt = session.query(Crashes).statement
    df = pd.read_sql_query(stmt, session.bind)
    df.set_index('crash_year', inplace=True)

    # Return a list of the column names (sample names)
    return jsonify(list(df.columns))

@app.route('/census')
def demoYears():

    # Use Pandas to perform the sql query
    stmt = session.query(Demographics).statement
    df = pd.read_sql_query(stmt, session.bind)
    df.set_index('year', inplace=True)

    # Return a list of the column names (sample names)
    return jsonify(list(df.columns))


if __name__ == "__main__":
    app.run(debug=True)
