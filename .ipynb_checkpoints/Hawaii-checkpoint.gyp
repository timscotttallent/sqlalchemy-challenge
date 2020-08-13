import flask
import numpy as numpy
import pandas as pandas

import sqlalchemy
from sqalachemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#reflect an exsiting database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each tables
Measurement = Base.classes.Measurementstation = Base.classes.ststion
app = flask.Flask(_name_)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return """<h1>Hawaii Climate: Available APTs</h1>
<ul>
<li>/api/v1.0/percipation</li>
<li>/api/v1.0/stations</li>
<li>/api/v1.0/tobs</li>
<li>/api/v1.0/&ltstart&gt>/&ltend&gt</li>
</ul>
"""

app.run()

