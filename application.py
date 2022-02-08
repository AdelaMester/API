from flask import Flask, jsonify
import sqlite3
from flask_restx import Api, Resource
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure application and Api
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Authentication required
authorizations = {
    'api': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}
api = Api(app, authorizations=authorizations, security='api', version='1.0', title='Bidnamic', description='Top 10 Search Terms by ROAS for a campaign structure_value or adgroup alias.')
ns = api.namespace('Data', description='Top 10 Search Terms by ROAS')

# Define campaign route and the placeholder for a structure value
@ns.route("/campaign/<string:structure_value>")
class Campaign(Resource):
    @api.doc(security='api')
    def get(self, structure_value):

        """ Returns the Top 10 Search Terms by ROAS for a campaign structure_value """

        # Connect to the database
        conn = sqlite3.connect('files.db')

        # Create a cursor object to execute queries on the database
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT conversion_value / cost AS roas, search_terms.search_term FROM search_terms JOIN campaigns ON search_terms.campaign_id = campaigns.campaign_id WHERE conversion_value !=0 AND cost != 0 AND campaigns.structure_value=? ORDER BY roas DESC LIMIT 10", (structure_value,))
        topTen = cursor.fetchall()

        #Closing the connection
        conn.close()
        return jsonify(topTen)
