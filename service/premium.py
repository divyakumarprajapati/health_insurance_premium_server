from app import mongo
import uuid

db = mongo["premium"]

def calculate_premium(request):
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
        premiumRate = db.premiumRate.find_one({
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

    response = {"membersPremium": membersPremium, "total": total}

    return response

def create_premium(request):
    body = request.json
    premiumTotal = int(body["total"])
    premiumSplitData = body["membersPremium"]
    orderId = uuid.uuid4()
    data = {
        "premiumTotal":premiumTotal, 
        "premiumSplitData":premiumSplitData,
        "orderId":str(orderId)
    }

    db.premiumOrder.insert_one(document=data)

    res = {
        "total":data["premiumTotal"],
        "orderId":data["orderId"],
        "membersPremium":data["premiumSplitData"]
    }
    return res

def get_all_premium():
    allPremiums = db.premiumOrder.find({})
    premiumList = []

    for premium in allPremiums:
        res = {
            "total":premium["premiumTotal"],
            "orderId":premium["orderId"],
            "membersPremium":premium["premiumSplitData"]
        }
        premiumList.append(res)
    
    response = {
        "premiums":premiumList
    }
    return response