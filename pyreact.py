def create_element(el):
    props = el["props"]

    children = False
    for x in props:
        if x["name"] == "children":
            children = x["value"]

    if children == False:
        child = ""
    elif type(children) is str:
        child = children
    else:
        child = create_element(children)

    name = el["name"]
    props_str = ""
    for p in props:
        if p["name"] != "children":
            props_str += (" " + p["name"] + "=\"" + p["value"] + "\"")

    return f"<{name} {props_str}>{child}</{name}>"

root_comp = {
    "name": "h1",
    "props": [
        {
            "name": "children",
            "value": {
                "name": "span",
                "props": [
                    {
                        "name": "class",
                        "value": "foo",
                    },
                    {
                        "name": "children",
                        "value": "I am a spanned h1",
                    },
                ]
            }
        },
    ]
}

root_comp_2 = {
    "name": "h1",
    "props": [
        {
            "name": "children",
            "value": {
                "name": "span",
                "props": [
                    {
                        "name": "children",
                        "value": {
                            "name": "h1",
                            "props": [
                                {
                                    "name": "id",
                                    "value": "yo",
                                },
                                {
                                    "name": "children",
                                    "value": "texting again !!",
                                },
                            ]
                        },
                    },
                    {
                        "name": "class",
                        "value": "foo",
                    },
                ]
            }
        },
    ]
}
# should return <h1><span class="foo">I am a spanned h1</span></h1>

root = create_element(root_comp)
root2 = create_element(root_comp_2)

print(root)
print(root2)
