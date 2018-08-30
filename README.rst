=========================
Composable HTML in Python
=========================

Description
===========

Very basic Python functions to generate HTML in a composable way.

Usage
=====

Very much inspired from React.

A component is any function that returns the result of a
``create_element`` call. This function that the element name,

Let us first define a Text component. We will create a text element
without any attributes:

.. code:: python

   from chp import create_element, create_prop, render_element

   def Text(t):
       return create_element("span", [], t)

   t = Text("YourLabs")
   render_element(t)

   # outputs => "<span >YourLabs</span>"

Let's now use this component to display text inside a link:

.. code:: python

   def Link(href, children):
       href = create_prop("href", href)
       return create_element("a", [href], children)

   l = Link("yourlabs.org", [Text("YourLabs")])
   render_element(l)

   # outputs => "<a  href="yourlabs.org"><span >YourLabs</span></a>"

Let us now define a Menu component that will create links inside of a
``nav`` element based on some input. Let's also use the shorthand aliases to ``create_element`` and ``create_prop``: ``ce`` and ``cp`` respectively.

.. code:: python

   def Menu(links=[]):
       children = []  # in this case, the menu links array
       for l in links:
           el = Link(l["href"], [Text(l["text"])])
           children.append(el)

       return ce("nav", [cp("class", "menu")], children)

   links = [
       {
           "href": "yourlabs.org",
           "text": "YourLabs",
       },
       {
           "href": "novamedia.nyc",
           "text": "NovaMedia",
       },
   ]

   m = Menu(links)
   render_element(m)

   # outputs => <nav  class="menu"><a  href="yourlabs.org"><span >YourLabs</span></a><a  href="novamedia.nyc"><span >NovaMedia</span></a></nav>

Pretty printed, the final output is:

.. code:: html

   <nav class="menu">
     <a href="yourlabs.org">
       <span>YourLabs</span>
     </a>
     <a href="novamedia.nyc">
       <span>NovaMedia</span>
     </a>
   </nav>

Feel free to check out the ``app.py`` and ``components.py`` files to see
how a full page can be built easily using this method. The ``app.py``
file writes the HTML output to another file called ``output.html``.

Trying it
=========

.. code:: bash

   git clone git@github.com:tbinetruy/CHIP.git
   cd CHIP

   python app.py # write HTML to output.html file
   firefox output.html

Examples
========

To run the example project included in the module:

.. code:: bash

   pip install --user --editable path/to/chp[dev]
   yarn install; yarn start
   chp-django runserver
   py.test path/to/chp

.. code:: python

   import chp

   def FormSchema(is_checked):
       return chp.Form([
           chp.Row([
               chp.Input('username'),
               chp.CheckboxField(is_checked),
           ])
       ])

   class PostForm(forms.ModelForm):
       def render(self):
           is_checked = 'checked' # self.checked
           return mark_safe(FormSchema(is_checked).render_element(Form))

``_html`` becomes a string containing the following HTML code:

.. code:: html

   <form  class="mdc-layout-grid__cell">
     <div  class="mdc-layout-grid__inner">
       <input  class="mdc-input__native-control" type="text" id="{{ id }}" value="{{ value }}" name="username"></input>
       <div  class="mdc-form-field">
         <div  class="mdc-checkbox">
           <input  class="mdc-checkbox__native-control" type="checkbox" id="{{ id }}" name="password"></input>
           <div  class="mdc-checkbox-background"></div>
           <label  for="{{ id }}">{{ label }}</label>
         </div>
       </div>
     </div>
     <div >
       {% for error in form.non_field_errors %}
           {{ error }}
       {% endfor %}
     </div>
   </form>

TODOS
=====

-  Testing of the pyreact.py file. Some of the high level results were
   copy pasted into ``tests.org``.