#################################################
# Import Dependencies
# @TODO: Import necessary libraries
#################################################

from flask import Flask, render_template
import scrape_mars  
from pymongo import MongoClient

#################################################
# Flask Setup
# @TODO: Initialize your Flask app here
#################################################
app = Flask(__name__)

#################################################
# MongoDB Setup
# @TODO: Initialize your MongoDB app here
#################################################

client = MongoClient("mongodb://localhost:27017")
db = client.mission_to_mars

#################################################
# Flask Routes
# @TODO:  Create a route that takes in data from mongodb and renders index.html template
#################################################
@app.route("/")
def index():
    new_data = db.general.find_one()
    # MongoDB Mnipulation
    # @TODO: Scrape new data if first run
    if(new_data == None):
        output = scrape_mars.scrape()
        db.general.insert_one(output)
        new_data = db.general.find_one()
        
    # Get data from mongodb
    # Send the data to html template
    for k, v in new_data.items(): 
        if k == "news":
            news = v
        elif k == "weather":                
            weather = v
        elif k == "featured_image_url":
            featured_image_url = v
        elif k == "facts":
            facts = v
        elif k == "hemisphere_image_urls": 
            hemisphere_image_urls = v
    return render_template('index.html',news=news,weather=weather,featured_image_url=featured_image_url,facts=facts,hemisphere_image_urls=hemisphere_image_urls)

        
#################################################
# Flask Routes
# @TODO:  Create a route that scrapes new data from mongodb and renders success.html template on completion
#################################################
@app.route("/scrape")
def scrape_new():
    output = scrape_mars.scrape()
    db.general.remove({})
    db.general.insert_one(output)
    return render_template('success.html')

if __name__ == "__main__":
    app.run(debug=True)
