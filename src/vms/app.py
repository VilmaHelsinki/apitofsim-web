import os
from flask import Flask, render_template, redirect, request, abort
from .forms import SettingsForm, BuiltInInstrumentForm, CustomInstrumentForm
from .utils import parse_config_list

app = Flask(__name__)
app.config["SECRET_KEY"] = "a-secret-key"


CHAINS = parse_config_list(os.environ["CHAINS"])

from pprint import pprint

pprint(CHAINS)


def vibrations_plot(particle):
    from matplotlib import pyplot as plt
    from io import StringIO

    plt.figure()
    plt.hlines(1, 1, 20)
    plt.eventplot(
        particle["vibrational_temperatures"], orientation="horizontal", colors="b"
    )
    plt.axis("off")
    f = StringIO()
    plt.savefig(f, format="svg")
    particle["vibrations_plot"] = f.getvalue()


for chain in CHAINS.values():
    for particle in ["cluster", "first_product", "second_product"]:
        vibrations_plot(chain[particle])


@app.template_filter("join_abbrv")
def join_abbrv_filter(s, sep="<br>"):
    def joined(s):
        return sep.join((str(e) for e in s))

    if len(s) <= 5:
        return joined(s)
    else:
        return joined(s[:2] + ["..."] + s[-2:])


@app.route("/", methods=["GET", "POST"])
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        return redirect(
            "/analysis?realizations=" + str(form.simulation.realizations.data)
        )
    return render_template(
        "settings/settings.html",
        form=form,
        chain=CHAINS[form.chain.data],
    )


@app.route("/fragments/chain")
def chain_fragment():
    chain = request.args.get("chain")
    if chain in CHAINS:
        return render_template("_render_chain.html", chain=chain)
    else:
        abort(400, description="Invalid chain parameter")


@app.route("/fragments/instrument")
def instrument_fragment():
    instrument = request.args.get("instrument")
    # TODO:: Add prefix here
    if instrument == "custom":
        return render_template(
            "settings/_render_instrument.html",
            form=CustomInstrumentForm(prefix="instrument-"),
        )
    elif instrument == "default3000":
        return render_template(
            "settings/_render_instrument.html",
            form=BuiltInInstrumentForm(prefix="instrument-"),
        )
    else:
        abort(400, description="Invalid instrument parameter")


@app.route("/analysis")
def analysis():
    realizations = request.args.get("realizations")
    if realizations is None:
        abort(400, description="Missing realizations parameter")
    try:
        realizations = int(realizations)
    except ValueError:
        abort(400, description="Invalid realizations parameter")
    return render_template("analysis.html", iterations=realizations)


if __name__ == "__main__":
    app.run(debug=True)
