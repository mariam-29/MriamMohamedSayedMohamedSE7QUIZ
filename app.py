from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


employees = []


departments = ['HR', 'IT', 'Marketing']

# WHAT THE FUCK ?
class EmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    department = SelectField('Department', choices=[])
    role = StringField('Role', validators=[DataRequired()])
    submit = SubmitField('Add Employee')


@app.route('/')
def home():
    return redirect('/directory')


@app.route('/add-employee', methods=['GET', 'POST'])
def add_employee():
    form = EmployeeForm()
    form.department.choices = [(d, d) for d in departments]

    if form.validate_on_submit():
        employee = {
            'name': form.name.data,
            'department': form.department.data,
            'role': form.role.data
        }
        employees.append(employee)
        return redirect('/directory')

    return render_template('add_employee.html', form=form)


@app.route('/directory')
def directory():
    selected_dept = request.args.get('department')

    if selected_dept:
        filtered = [e for e in employees if e['department'] == selected_dept]
    else:
        filtered = employees

    return render_template(
        'directory.html',
        employees=filtered,
        departments=departments,
        selected_dept=selected_dept
    )


if __name__ == '__main__':
    app.run(debug=True)