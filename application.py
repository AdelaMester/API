from flask import Flask, jsonify, request
import sqlite3
from flask_restx import Api, Resource
from werkzeug.middleware.proxy_fix import ProxyFix
import os

# Configure application and Api
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Authentication required
authorizations = {
    os.environ.get('secret'): {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}
api = Api(app, authorizations=authorizations, security=os.environ.get('secret'), version='1.0', title='Bidnamic', description='Top 10 Search Terms by ROAS for a campaign structure_value or adgroup alias.')
ns = api.namespace('Data', description='Top 10 Search Terms by ROAS')

# Define campaign route and the placeholder for a structure value
@ns.route("/campaign/<string:structure_value>")
class Campaign(Resource):
    @api.doc(security=os.environ.get('secret'))
    def get(self, structure_value):

        """ Returns the Top 10 Search Terms by ROAS for a campaign structure_value """

        # Check if the header exists
        if 'X-API-KEY' in request.headers:
            # Check if the header has the specific value
            if request.headers['X-API-KEY'] == os.environ.get('secret'):

                # Connect to the database
                conn = sqlite3.connect('files.db')

                # Create a cursor object to execute queries on the database
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT conversion_value / cost AS roas, search_terms.search_term FROM search_terms JOIN campaigns ON search_terms.campaign_id = campaigns.campaign_id WHERE conversion_value !=0 AND cost != 0 AND campaigns.structure_value=? ORDER BY roas DESC LIMIT 10", (structure_value,))
                topTen = cursor.fetchall()

                #Closing the connection
                conn.close()
                return jsonify(topTen)
            else:
                return({'message': 'Missing authentication'}), 401
        else:
            return({'message':'Missing authentication header'}), 401


# Define adgroup route and the placeholder for a alias
@ns.route("/adgroup/<string:alias>")
class Adgroup(Resource):
    @api.doc(security=os.environ.get('secret'))
    def get(self, alias):

        """ Returns the Top 10 Search Terms by ROAS for a adgroup alias """

        # Check if the header exists
        if 'X-API-KEY' in request.headers:
            # Check if the header has the specific value
            if request.headers['X-API-KEY'] == os.environ.get('secret'):

                # Connect to the database
                conn = sqlite3.connect('files.db')

                # Create a cursor object to execute queries on the database
                cursor = conn.cursor()

                # Query the database to display the top 10 search terms for a adgroup alias
                cursor.execute("SELECT DISTINCT conversion_value / cost AS roas, search_terms.search_term FROM search_terms JOIN adgroup ON search_terms.campaign_id = adgroup.campaign_id WHERE conversion_value !=0 AND cost != 0 AND adgroup.alias=? ORDER BY roas DESC LIMIT 10", (alias,))
                topTen = cursor.fetchall()

                # Closing the connection
                conn.close()
                return jsonify(topTen)
            else:
                return({'message': 'Missing authentication'}), 401
        else:
            return({'message':'Missing authentication header'}), 401

