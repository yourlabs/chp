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

def AuthorNoError(author):
    return ce("div", [cp("class", "author")], [Text(author)])

def AuthorError(author):
    return ce("div", [cp("class", "author"), cp("style", "color: red")], [Text(author)])

def Author(author, isError):
    if isError:
        return AuthorError(author)
    else:
        return AuthorNoError(author)


def Content(content):
    return ce("div", [cp("class", "content")], [Text(content)])

def Post(author, content, isError, errorCb):
    if(isError):
        errorCb(author + " is in error")
    return ce("div", [cp("class", "post")], [Author(author, isError), Content(content)])

def Body(posts=[], links=[], is_error=False):
    c = [Menu(links)] # body children

    error_messages = []
    def getError(str):
        if not is_error:
            error_messages.append(str)

    for p in posts:
        error_state = is_error
        if not error_state:
            error_state = p["isError"]
        c.append(Post(p["author"], p["content"], error_state, getError))

    for e in error_messages:
        c.append(Text(e))

    return ce("body", [], c)

def App(posts=[], links=[], isError=False):
    return ce("html", [], [Body(posts, links, isError)])
