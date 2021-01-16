#importing relevant modules
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#setting up my database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflecting my DB
Base = automap_base()

Base.perpare(engine, reflect=True)

#saving the references to the tables
m = Base.classes.measurement

s = Base.classes.station

#setting up my flask app
