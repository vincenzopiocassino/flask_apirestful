from flask import Flask, request
from flask_restful import Resource, Api
from colors_gcp import Colors

# The colors object provides CRUD methods

# Create the Flask application instance
app = Flask(__name__, static_url_path='/static', static_folder='static')

# Create the main Flask-RESTful object
api = Api(app)
colors_dao = Colors()

# To comply with the specifications in the .yaml file
basePath = '/api/v1'

# Define two objects that extend the Resource class for binding

class ColorsResource(Resource):

    # Method for data validation
    def validate_colordata(self, colordata):
        # We need to validate three color components: red, green, and blue
        for key in ['red', 'green', 'blue']:
            if key not in colordata.keys():
                # If any of the components is missing, return False
                return False
            if not isinstance(colordata[key], int):
                # If the component is not an integer, return False
                return False
            # Check if the value is within the valid range (0-255)
            if colordata[key] < 0 or colordata[key] > 255:
                return False
        return True

    def get(self, colorname):
        # Convert the colorname to lowercase (non-case-sensitive)
        colorname = colorname.lower()
        # Get the color data from the DAO
        c = colors_dao.get_color_by_name(colorname)
        # If no match found, return 404, otherwise return 200 with the color data
        return (None, 404) if c is None else (c, 200)

    def post(self, colorname):
        # Accept JSON objects
        colordata = request.json
        print('got POST request' + str(colordata))
        # Validate the color data
        if not self.validate_colordata(colordata):
            return None, 400
        # Check if the color with the same name already exists (conflict)
        if colors_dao.get_color_by_name(colorname) is not None:
            return None, 409
        # Add the new color
        colors_dao.add_color(colorname, colordata['red'], colordata['green'], colordata['blue'])
        return None, 201

    def put(self, colorname):
        # Accept JSON objects
        colordata = request.json
        # Validate the color data
        if not self.validate_colordata(colordata):
            return None, 400
        # Check if the color with the specified name exists (not found)
        if colors_dao.get_color_by_name(colorname) is None:
            return None, 404
        # Update the existing color
        colors_dao.add_color(colorname, colordata['red'], colordata['green'], colordata['blue'])
        return None, 204

    def delete(self, colorname):
        # Check if the color with the specified name exists (not found)
        if colors_dao.get_color_by_name(colorname) is None:
            return None, 404
        # Delete the existing color
        colors_dao.delete_color_by_name(colorname)
        return None, 204


class ColorList(Resource):
    def get(self):
        # Return the list of colors with status code 200
        return colors_dao.get_colors(), 200


# Map the objects to URLs using the basePath
api.add_resource(ColorsResource, f'{basePath}/colors/<string:colorname>')
api.add_resource(ColorList, f'{basePath}/colors/')


if __name__ == '__main__':
    # Run the application
    app.run(host='127.0.0.1', port=8080, debug=True)
