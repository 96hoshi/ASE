from flakon import JsonBlueprint
from flask import abort, jsonify, request

from bedrock_a_party.classes.party import CannotPartyAloneError, Party, NotInvitedGuestError, \
    ItemAlreadyInsertedByUser, NotExistingFoodError

parties = JsonBlueprint('parties', __name__)

_LOADED_PARTIES = {}  # dict of available parties
_PARTY_NUMBER = 0  # index of the last created party


@parties.route("/parties", methods=['POST', 'GET'])
def all_parties():
    result = None

    if request.method == 'POST':
        # create a party
        try:
            result = create_party(request)
        except CannotPartyAloneError as e:
            abort(400, str(e))

    elif request.method == 'GET':
        result = get_all_parties()

    return result


@parties.route("/parties/loaded", methods=['GET'])
def loaded_parties():#
    # returns the number of parties currently loaded in the system
    global _LOADED_PARTIES
    result = jsonify({'loaded_parties': len(_LOADED_PARTIES)})

    return result


@parties.route("/party/<id>", methods=['GET', 'DELETE'])
def single_party(id):
    global _LOADED_PARTIES
    result = ""

    # check if the party is an existing one
    exists_party(id)
    if 'GET' == request.method:
        retrieved_party = _LOADED_PARTIES.get(id)
        result = jsonify(retrieved_party.serialize())

    elif 'DELETE' == request.method:
        _LOADED_PARTIES.pop(id)
        result = jsonify(msg="Party deleted!")

    return result


@parties.route("/party/<id>/foodlist", methods=['GET'])
def get_foodlist(id):
    # returns the the food-list of the id user
    global _LOADED_PARTIES
    result = ""

    exists_party(id)
    retrieved_party = _LOADED_PARTIES.get(id)
    if 'GET' == request.method:
        foodlist = retrieved_party.get_food_list()
        result = jsonify({'foodlist': foodlist.serialize()})

    return result


@parties.route("/party/<id>/foodlist/<user>/<item>", methods=['POST', 'DELETE'])
def edit_foodlist(id, user, item):
    global _LOADED_PARTIES

    exists_party(id)
    retrieved_party = _LOADED_PARTIES.get(id)
    result = ""

    if 'POST' == request.method:
        # add an item to food-list
        try:
            food_added = retrieved_party.add_to_food_list(item, user)
            result = jsonify(food_added.serialize())
        except NotInvitedGuestError as e:
            abort(401, str(e))
        except ItemAlreadyInsertedByUser as ee:
            abort(400, str(ee))

    if 'DELETE' == request.method:
        # delete an item to food-list
        try:
            retrieved_party.remove_from_food_list(item, user)
            result = jsonify(msg="Food deleted!")
        except NotExistingFoodError as e:
            abort(400, str(e))

    return result

#
# These are utility functions. Use them, DON'T CHANGE THEM!!
#

def create_party(req):
    global _LOADED_PARTIES, _PARTY_NUMBER

    # get data from request
    json_data = req.get_json()

    # list of guests
    try:
        guests = json_data['guests']
    except:
        raise CannotPartyAloneError("you cannot party alone!")

    # add party to the loaded parties lists
    _LOADED_PARTIES[str(_PARTY_NUMBER)] = Party(_PARTY_NUMBER, guests)
    _PARTY_NUMBER += 1

    return jsonify({'party_number': _PARTY_NUMBER - 1})


def get_all_parties():
    global _LOADED_PARTIES

    return jsonify(loaded_parties=[party.serialize() for party in _LOADED_PARTIES.values()])


def exists_party(_id):
    global _PARTY_NUMBER
    global _LOADED_PARTIES

    if int(_id) > _PARTY_NUMBER:
        abort(404)  # error 404: Not Found, i.e. wrong URL, resource does not exist
    elif not(_id in _LOADED_PARTIES):
        abort(410)  # error 410: Gone, i.e. it existed but it's not there anymore
