def render_element(el):
    props = el["props"]

    children = False
    for p in props:
        if p["name"] == "children":
            children = p["value"]

    child = ""
    if not children:
        child = ""
    elif type(children) is str:
        child = children
    else:
        for c in children:
            child += render_element(c)

    name = el["name"]
    props_str = ""
    for p in props:
        if p["name"] != "children":
            props_str += (" " + p["name"] + "=\"" + p["value"] + "\"")

    return f"<{name} {props_str}>{child}</{name}>"

def create_element(name, props, children):
    props.append({
        "name": "children",
        "value": children,
    })

    return {
        "name": name,
        "props": props,
    }

def create_prop(name, value):
    return {
        "name": name,
        "value": value,
    }

def get_prop(props=[], name=[]):
    for p in props:
        try:
            if p["name"] == name:
                return p
        except KeyError:
            return None

ce = create_element
cp = create_prop
gp = get_prop

def Link(href, children):
    href = cp("href", href)
    return ce("a", [href], children)

def Text(t):
    return ce("span", [], t)

l = Link("google.com", [Text("yooohoo")])
el = render_element(l)
print(el)

def Menu(links=[]):
    c = [] # menu children links array
    for l in links:
        el = Link(l["href"], [Text(l["text"])])
        c.append(el)

    return ce("nav", [cp("class", "menu")], c)

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
m = Menu(menu_links)
el = render_element(m)
print(el)
