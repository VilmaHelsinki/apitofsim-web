from flask_wtf import FlaskForm, Form
from wtforms import SelectField, FloatField, FormField, HiddenField
from wtforms.validators import InputRequired
from vms.utils import PairedRangeInputWidget


def mk_voltage_field(label, **kwargs):
    return FloatField(
        label,
        **kwargs,
        validators=[InputRequired()],
        render_kw={
            "type": "range",
            "min": "-50",
            "max": "50",
            "step": "1",
        },
        widget=PairedRangeInputWidget(),
    )


class VoltageForm(Form):
    voltage1 = mk_voltage_field("Voltage 1", default=-19)
    voltage2 = mk_voltage_field("Voltage 2", default=-9)
    voltage3 = mk_voltage_field("Voltage 3", default=-7)
    voltage4 = mk_voltage_field("Voltage 4", default=-6)
    voltage5 = mk_voltage_field("Voltage 5", default=11)


def mk_instrument_form(hidden):
    def maybe_field(mk_field, *args, **kwargs):
        if hidden:
            return HiddenField(*args, **kwargs)
        else:
            return mk_field(*args, **kwargs)

    class InstrumentForm(Form):
        temperature_ = maybe_field(
            FloatField,
            "Temperature (K)",
            validators=[InputRequired()],
            default=300.0,
        )
        pressure_first_chamber = maybe_field(
            FloatField,
            "Pressure first chamber (Pa)",
            default=182.0,
            validators=[InputRequired()],
        )
        pressure_second_chamber = maybe_field(
            FloatField,
            "Pressure second chamber (Pa)",
            default=3.53,
            validators=[InputRequired()],
        )
        length_of_first_chamber = maybe_field(
            FloatField,
            "Length of 1st chamber (meters)",
            default=1.0e-3,
            validators=[InputRequired()],
        )
        length_of_skimmer = maybe_field(
            FloatField,
            "Length of skimmer (meters)",
            default=5.0e-4,
            validators=[InputRequired()],
        )
        length_between_skimmer_and_front_quadrupole = maybe_field(
            FloatField,
            "Length between skimmer and front quadrupole",
            default=2.44e-3,
            validators=[InputRequired()],
        )
        length_between_front_quadrupole_and_back_quadrupole = maybe_field(
            FloatField,
            "Length between front quadrupole and back quadrupole (meters)",
            default=0.101,
            validators=[InputRequired()],
        )
        length_between_back_quadrupole_and_2nd_skimmer = maybe_field(
            FloatField,
            "Length between back quadrupole and 2nd skimmer (meters)",
            default=4.48e-3,
            validators=[InputRequired()],
        )

    return InstrumentForm


HiddenInstrumentForm = mk_instrument_form(hidden=True)
InstrumentForm = mk_instrument_form(hidden=False)


class SettingsForm(FlaskForm):
    voltage = FormField(VoltageForm)
    chain = SelectField(
        "Compound chain",
        choices=[("1ABisopooh1brd1w", "1ABisopooh1brd1w")],
        validators=[InputRequired()],
    )
    instrument = FormField(InstrumentForm)
