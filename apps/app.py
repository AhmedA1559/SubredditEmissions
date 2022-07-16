from flask import Flask, jsonify
from flask_caching import Cache

from api.client import Client

app = Flask(__name__)
client = Client(client_id="", client_secret="")

@app.route('/api/subreddit/<string:subreddit>', methods=['GET'])
def get_emissions(subreddit):
    return jsonify({'subreddit': subreddit, 'emissions':client.get_subreddit_emissions(subreddit)})

if __name__ == '__main__':
    app.run()