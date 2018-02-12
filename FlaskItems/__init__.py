from flask import Flask, render_template, request
from flask_api import status
import FlaskItems.utils.database as db
import FlaskItems.utils.api as api
from flask_api import status

import json

app = Flask(__name__)
app.config.from_object("config")


@app.route('/session', methods=['POST', 'GET'])
def session():
    print("in FlaskItems.session()")
    if request.method == "POST":
        request_data = request.get_data().decode("utf-8")
        print("request_data: ")
        print(request_data)

        req_dict = unpack_request(request_data)

        if "action" in req_dict.keys():
            if req_dict["action"] == "start":
                print("start")
                print(req_dict)
                api.start_session(req_dict["user_id"], req_dict["session_key"], req_dict["admin"], req_dict["device"])
            else:
                print("stop")
                api.end_session(req_dict["session_key"])
        else:
            return "{ \"error\": \"false\", \"message\": \"Missing parameters\" }", status.HTTP_400_BAD_REQUEST
        return "{ \"error\": \"false\", \"message\": \"It Worked!\" }", status.HTTP_200_OK
    else:
        return "{ \"error\": \"false\", \"message\": \"Method not Allowed\" }", status.HTTP_405_METHOD_NOT_ALLOWED


@app.route('/api/v1/<key>/add/events', methods=['POST'])
def add_event(key):
    print(key)
    request_data = request.get_data().decode("utf-8")
    req_dict = unpack_request(request_data)

    if api.session_active(key):
        if api.admin_session(key):
            add_json = api.add_event(req_dict["event_name"], req_dict["event_date"])
            message = "event created"
            api.log_event(key, message)
            return add_json
        else:
            return "{ \"error\": true, \"message\": \"User is not admin\" }", status.HTTP_401_UNAUTHORIZED
    else:
        return "{ \"error\": true, \"message\": \"Session key is inactive\" }", status.HTTP_401_UNAUTHORIZED


@app.route('/api/v1/<key>/delete/events/<event_id>', methods=['POST'])
def delete_event(key, event_id):
    print(key)
    print(event_id)
    if api.session_active(key):
        if api.admin_session(key):
            print("in delete_event() if api.admin_session()")
            delete_json = api.delete_event(event_id)
            message = "event deleted"
            api.log_event(key, message)
            return delete_json, status.HTTP_200_OK
        else:
            return "{ \"error\": true, \"message\": \"User is not admin\" }", status.HTTP_401_UNAUTHORIZED
    else:
        return "{ \"error\": true, \"message\": \"Session key is inactive\" }", status.HTTP_401_UNAUTHORIZED


@app.route('/api/v1/<key>/events', methods=['GET'])
def get_events(key):
    print("get_events")
    print(key)
    if api.session_active(key):
        events = api.get_events()
        message = "Session is active."
        response_json = "{ \"error\": false, \"message\": \"" + message + "\", \"events\": " + events + " }"
        print("message: ")
        print(message)
        print("events: ")
        print(events)
        print("respnse_json: ")
        print(response_json)
        return response_json, status.HTTP_200_OK
    else:
        message = "Session is not active."
        print(message)
        return "{ \"error\": \"true\", \"message\": \"" + message + "\" }"


@app.route('/api/v1/<key>/items', methods=['GET'])
def get_items(key):
    print("get_items")
    print(key)
    if api.session_active(key):
        items = api.get_items()
        message = "Session is active."
        response_json = "{ \"error\": false, \"message\": \"" + message + "\", \"items\": " + items + " }"
        print("message: ")
        print(message)
        print("items: ")
        print(items)
        print("response_json: ")
        print(response_json)
        return response_json, status.HTTP_200_OK
    else:
        message = "Session is not active."
        print(message)
        return "{ \"error\": \"true\", \"message\": \"" + message + "\" }", status.HTTP_401_UNAUTHORIZED


@app.route('/api/v1/<key>/items', methods=['POST'])
def add_item(key):
    print("in add_items(key)")
    print(key)
    request_data = request.get_data().decode("utf-8")
    req_dict = unpack_request(request_data)

    if api.session_active(key):
        if api.admin_session(key):
            add_json = api.add_item(req_dict["item_name"], req_dict["item_description"], req_dict["item_price"])
            message = "event created"
            api.log_event(key, message)
            return add_json
        else:
            return "{ \"error\": true, \"message\": \"User is not admin\" }", status.HTTP_401_UNAUTHORIZED
    else:
        return "{ \"error\": true, \"message\": \"Session key is inactive\" }", status.HTTP_401_UNAUTHORIZED


@app.route('/api/v1/<key>/delete/items/<item_id>', methods=['POST'])
def delete_item(key, item_id):
    print(key)
    print(item_id)
    if api.session_active(key):
        if api.admin_session(key):
            print("in delete_event() if api.admin_session()")
            delete_json = api.delete_item(item_id)
            message = "event deleted"
            api.log_event(key, message)
            return delete_json, status.HTTP_200_OK
        else:
            return "{ \"error\": true, \"message\": \"User is not admin\" }", status.HTTP_401_UNAUTHORIZED
    else:
        return "{ \"error\": true, \"message\": \"Session key is inactive\" }", status.HTTP_401_UNAUTHORIZED


@app.route('/api/v1/<key>/event/<event_id>/items', methods=['GET'])
def get_event_items(key, event_id):
    if api.session_active(key):
        response_template = "\"error\": false, \"message\": \"it worked\", \"items\": {}"
        items_text = api.get_event_items(event_id)
        response_json = "{ " + response_template.format(items_text) + " }"
        print(response_json)
        return response_json
    else:
        return "{ \"error\": true, \"message\": \"Session key is inactive\" }", status.HTTP_401_UNAUTHORIZED


@app.route('/api/v1/<key>/event/<event_id>/delete/items/<item_id>', methods=['POST'])
def delete_event_item(key, event_id, item_id):
    print("in delete_event_item()")
    if api.session_active(key):
        print("active")
        if api.admin_session(key):
            print("admin")
            return api.delete_event_item(event_id, item_id)
        else:
            return "{ \"error\": true, \"message\": \"Account is not admin\" }"


@app.route('/api/v1/<key>/items/<item_id>', methods=['POST', 'GET'])
def test(key, item_id):
    print("it worked")
    if request.method == "POST":
        print("its a post")
        request_data = request.data.decode("utf-8")
        print(request_data)
        print(key)
        print(item_id)
        req_dict = unpack_js_request(request_data)

        print(req_dict)

        update_text = api.update_event_items_sold(req_dict["event_id"], req_dict["item_id"], req_dict["count"])
        print("update_text: ")
        print(update_text)
        return "it worked"
    else:
        return "{ \"error\": \"false\", \"message\": \"Method not Allowed\" }", status.HTTP_405_METHOD_NOT_ALLOWED


def unpack_request(data):
    print(type(data))
    try:
        req_json = json.loads(data)
        req_dict = dict(req_json)
        print(req_dict)
    except ValueError:
        req_dict = request.form
        print(req_dict)
    return req_dict


def unpack_js_request(data):
    split_req = data.split("&")
    print(split_req)
    req_dict = dict()
    for param in split_req:
        k_v_pair = param.split("=")
        req_dict[k_v_pair[0]] = k_v_pair[1]
    return req_dict


if __name__ == '__main__':
    app.run(port=8090)
