#!/usr/bin/env python
import os
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
        #if not params: --> napacno!
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("pretvornik.html")

    def post(self):
        stevilo = float(self.request.get("stevilo"))
        operacija = self.request.get("temperatura")
        rezultat = None
        if operacija == "ctof":
            rezultat = {"vnos": "Vnesel si {}&#176;C Pretvorba:".format(stevilo) ,"izpis": float(stevilo) * 9/5 + 32, "enota": "&#176;F"}
        if operacija == "ftoc":
            rezultat = {"vnos": "Vnesel si {}&#176;F Pretvorba:".format(stevilo) ,"izpis": float(stevilo -32 )* 5/9, "enota": "&#176;C"}
        if operacija == "ctok":
            rezultat = {"vnos": "Vnesel si {}&#176;C Pretvorba:".format(stevilo) ,"izpis": float(stevilo) + 273.15, "enota": "K"}
        if operacija == "ktoc":
            rezultat = {"vnos": "Vnesel si {}K Pretvorba:".format(stevilo) ,"izpis": float(stevilo) - 273.15, "enota": "&#176;C"}

        return self.render_template("pretvornik.html", params = rezultat)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
