from flask import Flask, render_template
import pymongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app)

# setup mongo connection  DO I STILL NEED THIS?
#conn = "mongodb://localhost:27017"
#client = pymongo.MongoClient(conn)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars 
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

#I copied all this, I HAVE NO IDEA WHAT I'M DOING