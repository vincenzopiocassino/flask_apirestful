import json
from google.cloud import firestore


class Colors(object):
    def __init__(self):
        # Initialize Firestore client
        self.db = firestore.Client()

    def populate_db(self, filename):
        # Populate the Firestore database with data from the JSON file
        with open(filename) as f:
            color_data = json.load(f)
            for col in color_data:
                self.add_color(col['name'], col['red'], col['green'], col['blue'])

    def add_color(self, color_name, red, green, blue):
        # Add a color document to the 'colors' collection in Firestore
        colors_ref = self.db.collection('colors')
        colors_ref.document(color_name).set({'red': red, 'green': green, 'blue': blue})

    def get_colors(self):
        # Get a list of color names from the 'colors' collection in Firestore
        return [str(c.id) for c in self.db.collection('colors').stream()]

    def get_color_by_name(self, color_name):
        # Get the color document by name from the 'colors' collection in Firestore
        c = self.db.collection('colors').document(color_name).get()
        rv = c.to_dict() if c.exists else None
        return rv

    def delete_color_by_name(self, color_name):
        # Delete the color document by name from the 'colors' collection in Firestore
        self.db.collection('colors').document(color_name).delete()
        

if __name__ == '__main__':
    c = Colors()
    c.populate_db('colors.json')
    c.add_color('yellow', 255, 255, 0)
    print(c.get_colors())
    print(c.get_color_by_name('wisteria'))
