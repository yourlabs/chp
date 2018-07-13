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
    {
        "author": "Thomas Pic",
        "content": "yourlabs love you",
    },
]

a = App(blog_posts, menu_links)
html = render_element(a)

# Write output to html file
text_file = open("output.html", "w")
text_file.write(html)
text_file.close()
