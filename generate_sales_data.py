import csv
from uuid import uuid1
import random
from datetime import datetime, timedelta

from tqdm import tqdm

def init_ordered_menu_item(): 
    headers = ['order_id', 'menu_item_id', 'quantity']

    with open('OrderedMenuItem.csv', mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader() 


def fetch_id(name):
    with open('MenuItem.csv', mode="r", newline='') as csv_file:     
       for line in csv.reader(csv_file):
           if line[1] == name:
               return line[0]
    
    raise Exception(f"id of {name} not found")


def generate_sale(order_id):
    order = list()
    total_price : float = 0.0
    order_num_prob = random.randint(0, 50)
    order_num = 1 if order_num_prob < 50 else 2  

    for _ in range(order_num):
        # select base
        base_id = random.randint(0, 2)
        if base_id == 0:
            order.append("pita")
        elif base_id == 1:
            order.append("brown rice")
        else:
            order.append("rice pilaf")

        # select protein
        protein_id = bool(random.randint(0, 1))
        if protein_id == 0:
            order.append("meatball")
            total_price += 6.89
        else:
            order.append("falafel")
            total_price += 5.89
    
        # select drink
        drink = bool(random.randint(0, 1))
        if drink:
            order.append("drink")
            total_price += 2.45

    
    # select toppings
    num_toppings = random.randint(0, 4)
    toppings = random.sample([
            'feta cheese', 'cucumber', 'tzatziki',
            'hot sauce', 'peppers', 'hummus',
            'olives', 'onion', 'tomato'
            ], num_toppings)
    
    for topping in toppings:
        order.append(topping)

    # select dressings
    dressing = random.choice([
        'greek yogurt',
        'aioli',
        'harissa',
        'tahini',
        'oregano'
        ])

    order.append(dressing)
   
    # select sides
    has_sides = bool(random.randint(0, 1))
    salad = bool(random.randint(0, 1)) if has_sides else False 
    if salad:
        total_price += 1.99
        order.append("salad")

    hummus = bool(random.randint(0, 1)) if has_sides else False
    if hummus:
        total_price += 3.99
        order.append("hummus and pita")
 
    # write to file
    with open('OrderedMenuItem.csv', mode='a') as ordered_menu_item_table:
        writer = csv.DictWriter(ordered_menu_item_table, fieldnames=["order_id", "menu_item_id", "quantity"])

        for ordered_menu_item in order:
            menu_item_id = fetch_id(ordered_menu_item) 
            writer.writerow({
                'order_id': order_id,
                'menu_item_id': menu_item_id,
                'quantity': 1
                })

    return total_price


def generate_sales_data():
    total_sales = 0

    init_ordered_menu_item()
    
    start_date = datetime.now() - timedelta(weeks=52)

    headers = ['id', 'date', 'total_price']

    with open('Order.csv', mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
 
        # for every day in the last year
        for day in tqdm (range (1, 365), desc="Loading..."):
            if day % 7 == 0:
                num_sales = random.randint(150, 200)
            else:
                num_sales = random.randint(300, 500)

            for _ in range(num_sales):
                order_id = uuid1() 
                order_datetime = start_date + timedelta(days=day, hours=random.randint(8, 20))
                total_price = generate_sale(order_id)
                writer.writerow({'id': order_id, 'date': order_datetime, 'total_price': total_price})
                total_sales += total_price
            print(total_sales) 
    
    print(total_sales)

generate_sales_data()
