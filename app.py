# App

from pyreact import create_element, create_prop, get_prop, render_element
from Form import App




form = {
    "errors":[],
    "fields":[
        {
            "type": 'text',
            "label": 'Username',
            "value": 'python',
            "errors": [],
        },
        {
            "type": 'password',
            "label": 'Password',
            "errors": [
                'Your password is incorrect',
            ],
            "value": 'aoeu',
        },
    ]
}

a = App(form)
html = render_element(a)
print(html)

# Write output to html file
text_file = open("output.html", "w")
text_file.write(html)
text_file.close()

