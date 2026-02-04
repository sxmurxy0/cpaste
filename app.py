from flask import Flask
import json
from models import database


app = Flask(__name__)
app.config.from_file('config.json', json.load)

database.init_app(app)

@app.get('/')
def ping():
    return "Hello!", 200

if __name__ == '__main__':
    with app.app_context():
        database.create_all()
    
    app.run()