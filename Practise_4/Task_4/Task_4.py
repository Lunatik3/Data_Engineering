import sqlite3
import json

def parser_data(file_name):
    items = []
    with open(file_name, "r", encoding='utf-8') as f:
        lines = f.readlines()
    item = dict()
    for line in lines:
        if line == "=====\n":
            items.append(item)
            item = dict()
            item["category"] = "no"
        else:
            line = line.strip()
            split = line.split("::")

            if split[0] in ["views", "quantity"]:
                item[split[0]] = int(split[1])
            elif split[0] == "price":
                item[split[0]] = float(split[1])
            elif split[0] == "isAvailable":
                item[split[0]] = split[1] == "True"
            elif split[0] == "id":
                continue
            else:
                item[split[0]] = split[1]
    #print(items)
    return items

def read_file(file_name):
    items = []
    with open(file_name, 'rb') as file:
        data = json.load(file)
        for row in data:
            if len(row) == 0:
                continue
            item = dict()
            item["name"] = row["name"]
            item["method"] = row["method"]
            if item['method'] == 'available':
                item['param'] = row["param"] == "True"
            elif item['method'] != 'remove':
                item["param"] = float(row['param'])
            items.append(item)
    #print(items)
    return items


def connect(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
                    INSERT INTO products 
                    (
                        name,
                        price,
                        quantity,
                        category,
                        fromCity,
                        isAvailable,
                        views
                    )
                    VALUES
                    (:name, :price, :quantity, :category, :fromCity, :isAvailable, :views)
    """, data)
    db.commit()

def delete_name(db, name):
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE name = ?", [name])
    db.commit()


def update_price_by_percent(db, name, percent):
    cursor = db.cursor()
    cursor.execute('UPDATE products SET price = ROUND((price * (1 + ?)), 2) WHERE name = ?', [percent, name])
    cursor.execute('UPDATE products SET version = version + 1 WHERE name = ?', [name])
    db.commit()


def update_price(db, name, value):
    cursor = db.cursor()
    res = cursor.execute('UPDATE products SET price = (price + ?) WHERE (name = ?) AND ((price + ?) > 0)', [value, name, value])
    if res.rowcount > 0:
        cursor.execute("UPDATE products SET version = version + 1 WHERE name = ?", [name])
        db.commit()


def update_available(db, name, param):
    cursor = db.cursor()
    cursor.execute("UPDATE products SET isAvailable = ? WHERE (name = ?)", [param, name])
    cursor.execute("UPDATE products SET version = version + 1 WHERE name = ?", [name])
    db.commit()


def update_quantity(db, name, val):
    cursor = db.cursor()
    res = cursor.execute("UPDATE products SET quantity = (quantity + ?) WHERE (name = ?) AND ((quantity + ?) > 0)",
                         [val, name, val])
    if res.rowcount > 0:
        cursor.execute("UPDATE products SET version = version + 1 WHERE name = ?", [name])
        db.commit()


def handle_update(db, update_items):
    for item in update_items:
        method = item['method']
        if method == 'remove':
            print(f'deleting {item["name"]}')
            delete_name(db, item['name'])
        elif method == 'price_percent':
            print(f'update_price {item["name"]} {item["param"]} %')
            update_price_by_percent(db, item['name'], item['param'])
        elif method == "price_abs":
            print(f"update price {item['name']} {item['param']}")
            update_price(db, item['name'], item['param'])
        elif method == "available":
            print(f"update available {item['name']} {item['param']}")
            update_available(db, item['name'], item['param'])
        elif method == "quantity_add":
            print(f"update quantity {item['name']} {item['param']}")
            update_quantity(db, item['name'], item['param'])
        elif method == "quantity_sub":
            print(f"update quantity {item['name']} {item['param']}")
            update_quantity(db, item['name'], item['param'])
        else:
            print(f'unknow method {method}')


def top_update(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM products ORDER BY version DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    #print(items)
    return items

def charact_price(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
            category,
            SUM(price) as sum,
            AVG(price) as avg,
            MIN(price) as min,
            MAX(price) as max,
            COUNT(*) as total_count
        FROM products
        GROUP BY category
                        """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    #print(items)
    return items


def charact_quantity(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
            category,
            SUM(quantity) as sum,
            AVG(quantity) as avg,
            MIN(quantity) as min,
            MAX(quantity) as max,
            COUNT(*) as total_count
        FROM products
        GROUP BY category
                        """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    #print(items)
    return items

def filter_quantity(db):
    items = []
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM products
        WHERE category = 'cosmetics'
        ORDER BY quantity DESC
        """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    #print(items)
    return items


db = connect("third.db")
#items = parser_data("task_4_var_28_product_data.text")
#insert_data(db, items)
#items = read_file("task_4_var_28_update_data.json")
#charact_price(db)
#charact_quantity(db)
#filter_quantity(db)
#update = read_file('task_4_var_28_update_data.json')
#handle_update(db, update)
#update_price_by_percent(db, name, percent)

with open("products_top_update.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(top_update(db, 10), ensure_ascii=False))

with open("products_charact_price.json", 'w', encoding="utf-8") as f:
        f.write(json.dumps(charact_price(db), ensure_ascii=False))

with open("products_charact_quantity.json", 'w', encoding="utf-8") as f:
    f.write(json.dumps(charact_quantity(db), ensure_ascii=False))

with open("products_filter_quantity.json", 'w', encoding="utf-8") as f:
    f.write(json.dumps(filter_quantity(db), ensure_ascii=False))