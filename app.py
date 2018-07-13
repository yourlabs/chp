# App

from pyreact import create_element, create_prop, get_prop, render_element
from components import App, Menu, Body

menu_links = [
    {
        "href": "yourlabs.org",
        "text": "yourlabs love you",
    },
    {
        "href": "novamedia.nyc",
        "text": "nova media",
    },
    {
        "href": "google.com",
        "text": "google",
    },
    {
        "href": "twitter.com",
        "text": "twitter",
    },
]


blog_posts = [
    {
        "author": "James Pic",
        "content": "yourlabs love you",
        "isError": False,
    },
    {
        "author": "James Pic",
        "content": "yourlabs love you",
        "isError": True,
    },
    {
        "author": "Thomas Pic",
        "content": "yourlabs love you",
        "isError": True,
    },
    {
        "author": "James Pic",
        "content": "yourlabs love you",
        "isError": True,
    },
]

a = App(blog_posts, menu_links)
html = render_element(a)
print(html)

# Write output to html file
text_file = open("output.html", "w")
text_file.write(html)
text_file.close()




form = dict(
    errors=list('Username does not match password'),
    fields=dict(
        username=dict(
            label='Username',
            value='python',
        ),
        password=dict(
            label='Password',
            errors=list(
                'Your password is incorrect',
            ),
            value='aoeu',
        ),
    )
)
