from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "a-secret-key"


def mk_voltage_field(label):
    return FloatField(
        label,
        validators=[InputRequired()],
        render_kw={"type": "range", "min": "-50", "max": "50", "step": "1"},
    )


class VoltageForm(FlaskForm):
    voltage1 = mk_voltage_field("Voltage 1")
    voltage2 = mk_voltage_field("Voltage 2")
    voltage3 = mk_voltage_field("Voltage 3")
    voltage4 = mk_voltage_field("Voltage 4")
    voltage5 = mk_voltage_field("Voltage 5")
    dropdown = SelectField(
        "Dropdown",
        choices=[("1ABisopooh1brd1w", "1ABisopooh1brd1w")],
        validators=[InputRequired()],
    )


@app.route("/instrument", methods=["GET", "POST"])
def instrument():
    form = VoltageForm()
    if form.validate_on_submit():
        # Process the form data
        pass
    return render_template("instrument.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
