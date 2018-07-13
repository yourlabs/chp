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
    },
    {
        "author": "James Pic",
        "content": "yourlabs love you",
    },
    {
        "author": "James Pic",
        "content": "yourlabs love you",
    },
]

m = App(blog_posts, menu_links)
el = render_element(m)
print(el)
