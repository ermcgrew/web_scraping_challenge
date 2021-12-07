#imports
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

#create flask instance
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'
# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)
# Connect to a database. Will create one if not already available.
db = client.mars_db



# Set root route
@app.route('/')
def index():
    #query mongo db
    ####### mars_data = db.website.find()
    return render_template('index.html', mars_data=mars_data)

###########################
@app.route('/scrape')
def scraper():
    
    info = scrape_mars.scrape()
    #store in mongo as dictionary
    website.update({}, info, upsert=True)
    return redirect("/", code=302)


    
if __name__ == "__main__":
    app.run(debug=True)