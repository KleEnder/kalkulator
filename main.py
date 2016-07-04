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
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):

        return self.render_template("hello.html")

    def post(self):

        number = float(self.request.get("input_number"))
        number2 = float(self.request.get("input_number_2"))
        operationa = self.request.get("input_operation")

        def operation(operationa):
            if operationa == "+":
                result = number + number2
                return round(result, 4)
            elif operationa == "-":
                result = number - number2
                return round(result, 4)
            elif operationa == "*":
                result = number * number2
                return round(result, 4)
            elif operationa == "/":
                result = number / number2
                return round(result, 4)
            elif operationa == "%":
                result = number % number2
                return round(result, 4)
            elif operationa == "^2":
                result = number ** number2
                return round(result, 4)

        enviornment = dict()

        enviornment['operation'] = operation(operationa)
        '''
        self.write("Entered was: " + str(number) + ". " + "Second enter was: " + str(number2) + ". " +
                   "Inputted operation was :" + str(operationa) + ". " + '\n' + "Result is: " + str(operation(operationa)))
        '''
        return self.render_template("hello.html", params=enviornment)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
