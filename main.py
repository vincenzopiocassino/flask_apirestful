from flask import Flask, render_template, request
from wtforms import Form, IntegerField, SubmitField, validators
from colors_gcp import Colors

app = Flask(__name__, static_url_path='/static', static_folder='static')
colors_dao = Colors()


class Colorform(Form):
    red = IntegerField('Red', [validators.NumberRange(min=0, max=255)])
    green = IntegerField('Green', [validators.NumberRange(min=0, max=255)])
    blue = IntegerField('Blue', [validators.NumberRange(min=0, max=255)])
    submit = SubmitField('Submit')


# Create an object to encapsulate model (for form)
class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


@app.route('/colors/', methods=['GET'])
def get_colors():
    # Get the list of colors from the DAO and render the color_list.html template
    clist = colors_dao.get_colors()
    return render_template('color_list.html', colors=clist)


@app.route('/colors/<color>', methods=['GET', 'POST'])
def get_color(color):
    if request.method == 'POST':
        cform = Colorform(request.form)
        # Save the color data from the form using the DAO
        colors_dao.add_color(color, cform.red.data, cform.green.data, cform.blue.data)
    # Get the color data from the DAO
    c = colors_dao.get_color_by_name(color)
    if c is None:
        c = {'red': 0, 'green': 0, 'blue': 0}
    if request.method == 'GET':
        # Render the color.html template with the color data
        cform = Colorform(obj=Struct(**c))
    # Convert the RGB values to a color code
    rgbcode = '#%02X%02X%02X' % (c['red'], c['green'], c['blue'])
    return render_template('color.html', name=color, rgb=rgbcode, red=c['red'], green=c['green'], blue=c['blue'],
                           form=cform)


@app.errorhandler(404)
def page_not_found(e):
    # Render the 404.html template for page not found errors
    return render_template('404.html', path=request.path), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
