from app import app, request, jsonify
from service import premium

@app.route('/ping', methods=['GET'])
def ping():
    return 'Pong! The API is up and running.'

@app.route('/premium', methods=['POST'])
def cal_premium():
    return jsonify(premium.calculate_premium(request))

@app.route("/premiums", methods=['POST'])
def create_premium():
    return jsonify(premium.create_premium(request))

@app.route("/premiums", methods=['GET'])
def get_all_premium():
    return jsonify(premium.get_all_premium())
