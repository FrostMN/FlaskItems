import time
import datetime

drop_items = "DROP TABLE IF EXISTS items"
drop_events = "DROP TABLE IF EXISTS events"

drop_keys = "DROP TABLE IF EXISTS session_keys"

drop_sales = "DROP TABLE IF EXISTS items_sold"


create_items = "CREATE TABLE items ( " \
    "item_id INT NOT NULL AUTO_INCREMENT, " \
    "name VARCHAR(200) NOT NULL, " \
    "price DOUBLE NOT NULL, " \
    "description VARCHAR(500) NOT NULL, " \
    "creation_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, " \
    "language VARCHAR(10) NOT NULL DEFAULT 'eng', " \
    "PRIMARY KEY (item_id)" \
    ") "

create_events = "CREATE TABLE events ( " \
    "event_id INT NOT NULL AUTO_INCREMENT, " \
    "name VARCHAR(200) NOT NULL, " \
    "date DATETIME NOT NULL, " \
    "description VARCHAR(500), " \
    "creation_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, " \
    "language VARCHAR(10) NOT NULL DEFAULT 'eng', " \
    "PRIMARY KEY (event_id)" \
    ") "

create_keys = "CREATE TABLE session_keys( " \
     "user_id INT NOT NULL, " \
     "session_key VARCHAR(64), " \
     "active SMALLINT DEFAULT 1, " \
     "admin SMALLINT DEFAULT 0, " \
     "device VARCHAR(128) " \
     ") "

create_sales = "CREATE TABLE items_sold( " \
                    "sale_id INT NOT NULL AUTO_INCREMENT, " \
                    "event_id INT NOT NULL, " \
                    "item_id INT NOT NULL, " \
                    "number_sold INT NOT NULL, " \
                    "PRIMARY KEY (sale_id), " \
                    "FOREIGN KEY(event_id) REFERENCES events(event_id) ON DELETE CASCADE," \
                    "FOREIGN KEY(item_id) REFERENCES items(item_id) ON DELETE CASCADE" \
                    ") "

event_a_time = datetime.datetime.utcnow() + datetime.timedelta(days=5)
event_b_time = datetime.datetime.utcnow() + datetime.timedelta(days=10)

add_event_a = "INSERT INTO events " \
    "(name, date, description) " \
    "VALUES ('Concert in the Park', '{}', 'This is a test event.')".format(event_a_time)

add_event_b = "INSERT INTO events " \
    "(name, date, description) " \
    "VALUES ('Concert by the River', '{}', 'This is a test event.')".format(event_b_time)

add_item_one = "INSERT INTO items " \
    "(name, price, description) " \
    "VALUES ('Hat', 15.00, 'Baseball Cap')"

add_item_two = "INSERT INTO items " \
    "(name, price, description) " \
    "VALUES ('Band-T', 25.00, 'Printed band T-Shirt')"

add_item_three = "INSERT INTO items " \
    "(name, price, description) " \
    "VALUES ('Sticker', 5.00, 'Vinyl Band Logo')"

add_event_a_item_one = "INSERT INTO items_sold " \
    "(event_id, item_id, number_sold) " \
    "VALUES (1, 1, 5)"

add_event_a_item_two = "INSERT INTO items_sold " \
    "(event_id, item_id, number_sold) " \
    "VALUES (1, 2, 7)"

add_event_a_item_three = "INSERT INTO items_sold " \
    "(event_id, item_id, number_sold) " \
    "VALUES (1, 3, 2)"

add_event_b_item_one = "INSERT INTO items_sold " \
    "(event_id, item_id, number_sold) " \
    "VALUES (2, 1, 8)"

add_event_b_item_two = "INSERT INTO items_sold " \
    "(event_id, item_id, number_sold) " \
    "VALUES (2, 2, 4)"

add_event_b_item_three = "INSERT INTO items_sold " \
    "(event_id, item_id, number_sold) " \
    "VALUES (2, 3, 5)"


schema = (drop_sales, drop_items, drop_events, drop_keys, create_events, create_items, create_keys, add_item_one, add_item_two,
          add_item_three, create_sales, add_event_a, add_event_b, add_event_a_item_one, add_event_a_item_two,
          add_event_a_item_three, add_event_b_item_one, add_event_b_item_two, add_event_b_item_three)


if __name__ == '__main__':
    for qry in schema:
        print(qry)
