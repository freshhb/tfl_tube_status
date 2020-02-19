from flask import Flask, render_template, session, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)
from wtforms.validators import DataRequired
import json
import requests



'''
this connects to the TFL API, grabs the data of the tube lines, put it into a dictonary format:
all_lines = {'Bakerloo': 10, 'Central': 5, 'Circle': 10,}

And then processes the data on the values that are provided on the TFL status.
I'm then using flash to create colors for the tube line, this loops over all lines and then returns the output.

'''
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

class InfoForm(FlaskForm):
    '''
    This general class gets a lot of form about puppies.
    Mainly a way to go through many of the WTForms Fields.
    '''
    breed = StringField('AAAA?')
    submit = SubmitField('Submit')

def get_status():
    url = ('https://api.tfl.gov.uk/line/mode/tube,overground/status')
    b = requests.get(url)
    js = b.json()
    all_lines_status = {}

    for i in range(0, len(js)):
        status_code = js[i]["lineStatuses"][0]["statusSeverity"]
        line_name = js[i]["name"]
        all_lines_status[line_name] = status_code

    return all_lines_status


@app.route('/', methods=['GET', 'POST'])
def index():


    # all_lines = {'Bakerloo': 10,
    #             'Central': 5,
    #             'Circle': 10,
    #             }

    all_lines = get_status()

    form = InfoForm()
    # If the form is valid on submission (we'll talk about validation next)
    if form.validate_on_submit():

        for line in all_lines:
            print(line)

            if all_lines[line] == 10:
                print(line + ": Good Service")
                flash(f"{line} Good service", 'success', )
            elif all_lines[line] == 6:
                print(line + ": Severe Delays")
                flash(f"{line} Severe Delay", 'warning', )
            elif all_lines[line] == 9:
                print(line + ": Minor Delays")
                flash(f"{line} Minor Delays", 'warning', )
            elif all_lines[line] == 5:
                print(line + ": Part Closure")
                flash(f"{line} Part Closure", 'danger', )
            elif all_lines[line] == 20:
                print(line + ": Service Closed")
                flash(f"{line} Service Closed", 'danger', )
            else:
                print(line + ": Part Suspended")
                flash(f"{line} Part Suspended", 'danger', )

    return render_template('03-home.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
