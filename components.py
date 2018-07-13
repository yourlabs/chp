from pyreact import create_element, create_prop, render_element

ce = create_element
cp = create_prop

def Link(href, children):
    href = cp("href", href)
    return ce("a", [href], children)

def Text(t):
    return ce("span", [], t)

def Menu(links=[]):
    c = [] # menu children links array
    for l in links:
        el = Link(l["href"], [Text(l["text"])])
        c.append(el)

    return ce("nav", [cp("class", "menu")], c)

def Author(author):
    return ce("div", [cp("class", "author")], [Text(author)])

def Content(content):
    return ce("div", [cp("class", "content")], [Text(content)])

def Post(author, content):
    return ce("div", [cp("class", "post")], [Author(author), Content(content)])

def Body(posts=[], links=[]):
    c = [Menu(links)] # body children
    for p in posts:
        c.append(Post(p["author"], p["content"]))
    return ce("body", [], c)

def App(posts=[], links=[]):
    return ce("html", [], [Body(posts, links)])
