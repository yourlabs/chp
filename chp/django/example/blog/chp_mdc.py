from . import chp_html
from . import chp

cp = chp.create_prop
Div = chp_html.Div

def Grid(children):
    children = children or []
    props = [
        cp('class', 'mdc-layout-grid')
    ]
    return Div(props, children)

def GridInner(children):
    children = children or []
    props = [
        cp('class', 'mdc-layout-grid__inner')
    ]
    return Div(props, children)

def Cell(span, children):
    children = children or []
    props = [
        cp('class', 'mdc-layout-grid__cell--span-' + span)
    ]
    return Div(props, children)

def Row(children):
    children = children or []
    return Cell("12", children)

def Field(children):
    children = children or []
    props = [
        cp('class', 'mdc-layout-field')
    ]
    return Div(props, children)


def Checkbox(is_checked):
    props = [
        cp('class', 'mdc-checkbox__native-control'),
        cp('type', 'checkbox'),
        cp('id', '{{ id }}'),
        cp('checked' if is_checked else '', ''),
    ]
    return chp_html.Input(props)

def CheckboxField(isChecked):
    def c(context):
        children = []
        props = [
            cp('class', 'mdc-form-field')
        ]
        children.append(Div(
                [cp("class", "mdc-checkbox")],
                [
                    Checkbox(isChecked),
                    Div(
                        [cp("class", "mdc-checkbox-background")],
                        []
                    ),
                    chp_html.Label('Checkbox'),
                    chp_html.Label(context["label"])
                ]
            ))
        return Div(props, children)
    return c
