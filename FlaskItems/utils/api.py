import FlaskItems.utils.database as db
import FlaskItems.utils.secrets as secrets
from flask_api import status
import requests
from config import USER_URL
import MySQLdb


def start_session(user_id, key, admin, device):
    print("in db.start_session()")
    print(user_id)
    print(admin)
    key_query = "INSERT INTO session_keys (user_id, session_key, active, admin, device) VALUES (%s, %s, 1, %s, %s)"
    db.execute_query(key_query, (user_id, key, admin, device))


def end_session(key):
    print("in db.end_session()")
    key_query = "UPDATE session_keys SET active = 0 WHERE session_key = %s"
    db.execute_query(key_query, (key, ))


def log_event(key, message):
    log_url = "{}/log/{}/event".format(USER_URL, key)
    post_data = {'session_key': key, 'event': message}
    log_text = requests.post(log_url, post_data).text
    print(log_text)


#  TODO: implement this
def session_active(key):
    return True


def get_events():
    print("in api.get_events()")
    events_qry = "SELECT * FROM events"
    rs = db.get_rs(events_qry)
    print(rs)
    events_json = "[ "
    for event in rs:
        event_id = str(event[0])
        event_name = str(event[1])
        event_date = str(event[2])
        event_desc = str(event[3])

        event_json = "{ \"id\": " + event_id + \
                     ", \"name\": \"" + event_name + \
                     "\", \"description\": \"" + event_desc + \
                     "\", \"date\": \"" + event_date + "\" }, "
        events_json += event_json
    if len(events_json) > 2:
        events_json = events_json[:-2] + " ]"
    else:
        events_json = events_json + "]"

    print("end of api.get_events(): ")
    print("events_json: ")
    print(events_json)

    return events_json


def admin_session(key):
    if session_active(key):
        admin_query = "SELECT admin FROM session_keys WHERE session_key = %s "
        rs = db.get_rs(admin_query, (key, ))
        try:
            return bool(rs[0])
        except ValueError:
            return False
    else:
        return False


def delete_event(event_id):
    delete_query = "DELETE FROM events WHERE event_id = %s"
    db.execute_query(delete_query, (event_id,))
    return "{ \"error\": false, \"message\": \"Event successfully deleted.\" }"


def add_event(event_name, event_date):
    add_query = "INSERT INTO events (name, date) VALUES ( %s, %s )"
    db.execute_query(add_query, (event_name, event_date))
    return "{ \"error\": false, \"message\": \"Event successfully added.\" }"


def get_items():
    print("in api.get_events()")
    items_qry = "SELECT * FROM items"
    rs = db.get_rs(items_qry)
    print(rs)
    items_json = "[ "
    for item in rs:
        item_id = str(item[0])
        item_name = str(item[1])
        item_price = str(item[2])
        event_desc = str(item[3])

        item_json = "{ \"item_id\": " + item_id + \
                    ", \"name\": \"" + item_name + \
                    "\", \"description\": \"" + event_desc + \
                    "\", \"price\": \"" + item_price + "\" }, "
        items_json += item_json
    if len(items_json) > 2:
        items_json = items_json[:-2] + " ]"
    else:
        items_json = items_json + "]"

    print("end of api.get_items(): ")
    print("items_json: ")
    print(items_json)

    return items_json


def get_event_items(event_id):
    items_query = ""\
    "SELECT " \
        "s.sale_id AS 'Sale ID', " \
        "s.item_id AS 'Item ID', " \
        "e.name AS Event, i.name AS Item, " \
        "i.description AS Description, " \
        "i.price AS Price, " \
        "s.number_sold AS 'Number Sold' " \
    "FROM items as i " \
        "JOIN items_sold as s ON i.item_id = s.item_id " \
        "JOIN events as e ON s.event_id = e.event_id " \
    "WHERE e.event_id = %s;"

    print(items_query)

    array_string = "[ "

    item_template = "\"sale_id\": {}, \"item_id\": {}, \"name\": \"{}\", " \
                    "\"description\": \"{}\", \"price\": {}, \"number_sold\": {}"

    rs = db.get_rs(qry=items_query, params=event_id)

    for row in rs:
        print("row: ")
        print(row)
        item = "{ " + item_template.format(row[0], row[1], row[3], row[4], row[5], row[6]) + " }"
        array_string += item + ", "

    if len(array_string) == 2:
        array_string += "]"
    else:
        array_string = array_string[:-2] + " ]"

    print(array_string)
    return array_string


def delete_item(item_id):
    delete_query = "DELETE FROM items WHERE item_id = %s"
    db.execute_query(delete_query, (item_id,))
    return "{ \"error\": false, \"message\": \"Item successfully deleted.\" }"


def add_item(item_name, item_description, item_price):
    add_query = "INSERT INTO items (name, description, price) VALUES ( %s, %s, %s )"
    try:
        db.execute_query(add_query, (item_name, item_description, item_price))
        return "{ \"error\": false, \"message\": \"Event successfully added.\" }"
    except MySQLdb.Error:
        return "{ \"error\": true, \"message\": \"MySQL Error.\" }"


def delete_event_item(event_id, item_id):
    print("in delete event item")
    delete_qry = "DELETE FROM items_sold WHERE event_id = %s AND item_id = %s"
    print(delete_qry)
    try:
        db.execute_query(delete_qry, (event_id, item_id))
        print("after execute")
        return "{ \"error\": false, \"message\": \"Item successfully deleted from event.\" }"
    except MySQLdb.Error as e:
        print("insxcept")
        print(e)
        return "{ \"error\": true, \"message\": \"MySQL Error.\" }"


def update_event_items_sold(event_id, item_id, count):
    sold_query = "UPDATE items_sold SET number_sold = %s WHERE event_id = %s AND item_id = %s"
    try:
        db.execute_query(sold_query, (count, event_id, item_id))
        return "{ \"error\": false, \"message\": \"Item sold quantity successfully updated.\" }"
    except MySQLdb.Error:
        return "{ \"error\": true, \"message\": \"MySQL Error.\" }"
