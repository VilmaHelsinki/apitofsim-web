from flask import Flask, render_template, redirect
from .forms import SettingsForm, HiddenInstrumentForm, InstrumentForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "a-secret-key"


@app.route("/", methods=["GET", "POST"])
def instrument():
    form = SettingsForm()
    if form.validate_on_submit():
        return redirect("/analysis")
    return render_template(
        "instrument.html",
        form=form,
        instruments=[HiddenInstrumentForm(), InstrumentForm()],
    )


@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


if __name__ == "__main__":
    app.run(debug=True)
