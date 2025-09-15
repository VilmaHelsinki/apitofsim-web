from markupsafe import escape, Markup
from wtforms.widgets import html_params
import json
from contextlib import chdir


def chop_prefix(string, prefix):
    return string.startswith(prefix) and string[len(prefix) :]


class PairedRangeInputWidget:
    def __init__(self):
        pass

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        if "value" not in kwargs:
            kwargs["value"] = field._value()
        if "required" not in kwargs and "required" in getattr(field, "flags", []):
            kwargs["required"] = True
        range_kwargs = {}
        number_kwargs = {}
        for k, v in kwargs.items():
            if k in ("min", "max", "step"):
                range_kwargs[k] = v
            elif new_k := chop_prefix(k, "range__"):
                range_kwargs[new_k] = v
            elif new_k := chop_prefix(k, "number__"):
                number_kwargs[new_k] = v
            else:
                range_kwargs[k] = v
                number_kwargs[k] = v
        range_params = html_params(name=field.name, **range_kwargs)
        number_params = html_params(name=field.name, **range_kwargs)
        return Markup(
            f"""
            <input type="range" oninput="this.nextElementSibling.value = this.value" {range_params}>
            <input type="number" oninput="this.previousElementSibling.value = this.value" {number_params}>
            """.strip()
        )


def read_dat(fn):
    return [float(line.strip()) for line in open(fn)]


def parse_config(fn):
    config = {}
    with open(fn) as f:
        for line in f:
            line = line.strip()
            if " " not in line:
                continue
            value, name = line.strip().split()
            config[name] = value
    result = {"config": config}
    for particle in ["cluster", "first_product", "second_product"]:
        particle_data = {}
        for quantity in [
            "vibrational_temperatures",
            "rotational_temperatures",
            "electronic_energy",
        ]:
            config_key = f"file_{quantity}_{particle}"
            particle_data[quantity] = read_dat(config[config_key])
            particle_data["name"] = (
                config[config_key].rsplit(".", 1)[0].rsplit("/", 1)[-1]
            )
        particle_data["atomic_mass"] = config[f"Atomic_mass_{particle}"]
        result[particle] = particle_data
    return result


def parse_config_list(fn):
    with open(fn) as f:
        config_dict = json.load(f)
        for k, conf_info in config_dict.items():
            with chdir(conf_info["cwd"]):
                config_dict[k] = parse_config(conf_info["config"])
    return config_dict
