from app import app, mongo, request, jsonify

db = mongo.db

@app.route('/', methods=['GET'])
def ping():
    return 'Pong! The API is up and running.'

@app.route('/premium', methods=['POST'])
def get_premium():
    body = request.json
    cityTier = int(body['city_tier'])
    sumInsured = int(body['sum_insured'])
    tenure = int(body['tenure'])
    maxAgeIndex = 0
    members = body['members']
    maxAge = int(members[0]['age'])
    membersPremium = []
    for i in range(len(members)):
        if int(members[i]['age']) > maxAge:
            maxAge =  int(members[i]['age'])
            maxAgeIndex = i
            
    for index, member in enumerate(members):
        premiumRate = db.premiumRate.find_one_or_404({
            'city_tier': cityTier, 
            'sum_insured': sumInsured, 
            'tenure': tenure, 
            'age': int(member['age'])
        })
        premium = {
            'base_rate': premiumRate['rate'],
            'name': member['name'],
        }
        if(maxAgeIndex == index):
            premium['floater_discount_percentage'] = 0
            premium['discounted_rate'] = premiumRate['rate']
        else:
            premium['floater_discount_percentage'] = 50
            premium['discounted_rate'] = premiumRate['rate']/2
        membersPremium.append(premium)
    total = sum(member['discounted_rate'] for member in membersPremium)

    return jsonify({"membersPremium": membersPremium, "total": total})
