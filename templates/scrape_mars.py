from flask import Flask, render_template

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo



# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)
mongo = pymongo(app)
#create route for html

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

#scrape

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful!"



if __name__ == "__main__":
    app.run(debug=True)
