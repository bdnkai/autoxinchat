import time
import concurrent.futures
from flask import Flask, request, jsonify
from process_users import process_image
import requests

app = Flask(__name__)

# @app.route('/process', methods=['POST'])
# def process():
#     url = request.json['url']
#     usernames = get_usernames(url)
#     response = {'names': usernames}
#     return jsonify(response), 200


@app.route('/get_usernames', methods=['GET'])
def get_usernames():
    url = request.args.get('url')
    results = process_image(url)
    return jsonify(results), 200


if __name__ == '__main__':
    app.run(debug=True)


    