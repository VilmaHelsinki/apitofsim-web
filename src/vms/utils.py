from markupsafe import escape, Markup
from wtforms.widgets import html_params


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
