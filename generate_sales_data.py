"""
CSV sales data generation

Andres Mateo Ruiz Flores
02/28/23
"""

import csv
from uuid import UUID, uuid1
import random
from datetime import datetime, timedelta
from decimal import getcontext, Decimal, ROUND_HALF_UP

from tqdm import tqdm

CENT = Decimal('.01') 

def init_ordered_menu_item() -> None:
    """
    initiates the ordered menu items table
    """
    headers = ['order_id', 'menu_item_id', 'quantity']

    with open('OrderedMenuItem.csv', mode='w') as csv_file:
        writer : csv.DictWriter = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader() 


def fetch_id(name : str)->str:
    """
    fetches string id given menu item name
    
    Parameters
    ----------
    name : str 
        name of menu item

    Returns
    ----------
    str 
        string id of menu item
    """
    with open('MenuItem.csv', mode="r", newline='') as csv_file:     
       for line in csv.reader(csv_file):
           if line[1] == name:
               return line[0]
    
    raise Exception(f"id of {name} not found")


def generate_sale(order_id : UUID) -> Decimal:
    """
    generates a random sale 
    
    Parameters
    ----------
    order_id : UUID 
        order_id of the sale being created 

    Returns 
    ----------
    total_price : Decimal 
        total price of the order
    """

    order : list = list()
    total_price : Decimal = Decimal(0)
    order_num_prob : int = random.randint(0, 50)
    order_num : int = 1 if order_num_prob < 50 else 2  

    for _ in range(order_num):
        # select base
        base_id :int = random.randint(0, 2)
        if base_id == 0:
            order.append("pita")
        elif base_id == 1:
            order.append("brown rice")
        else:
            order.append("rice pilaf")

        # select protein
        protein_id : bool = bool(random.randint(0, 1))
        if protein_id == 0:
            order.append("meatball")
            total_price += Decimal(6.89)
        else:
            order.append("falafel")
            total_price += Decimal(5.89)
    
        # select drink
        drink : bool = bool(random.randint(0, 1))
        if drink:
            order.append("drink")
            total_price += Decimal(2.45)

    
    # select toppings
    num_toppings : int = random.randint(0, 4)
    toppings : list = random.sample([
            'feta cheese', 'cucumber', 'tzatziki',
            'hot sauce', 'peppers', 'hummus',
            'olives', 'onion', 'tomato'
            ], num_toppings)
    
    for topping in toppings:
        order.append(topping)

    # select dressings
    dressing : str = random.choice([
        'greek yogurt',
        'aioli',
        'harissa',
        'tahini',
        'oregano'
        ])

    order.append(dressing)
   
    # select sides
    has_sides : bool = bool(random.randint(0, 1))
    salad : bool = bool(random.randint(0, 1)) if has_sides else False 
    if salad:
        total_price += Decimal(1.99)
        order.append("salad")

    hummus : bool = bool(random.randint(0, 1)) if has_sides else False
    if hummus:
        total_price += Decimal(3.99)
        order.append("hummus and pita")
 
    # write to file
    with open('OrderedMenuItem.csv', mode='a') as ordered_menu_item_table:
        writer : csv.DictWriter = csv.DictWriter(ordered_menu_item_table, fieldnames=["order_id", "menu_item_id", "quantity"])

        for ordered_menu_item in order:
            menu_item_id : str = fetch_id(ordered_menu_item) 
            writer.writerow({
                'order_id': order_id,
                'menu_item_id': menu_item_id,
                'quantity': 1
                })
   
    total_price = total_price.quantize(CENT, rounding=ROUND_HALF_UP)    
    return total_price


def generate_sales_data() -> None:
    """
    main driver code, generates sales data through the last 365 days
    """
    total_sales : Decimal = Decimal(0)      # tracks total revenue made in year

    init_ordered_menu_item()
    
    start_date : datetime = datetime.now() - timedelta(weeks=52)

    headers : list = ['id', 'date', 'total_price']

    with open('Order.csv', mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
 
        # for every day in the last year
        for day in tqdm (range (1, 365), desc="Generating Yearly Sales"):
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
    
    print(f"\nTotal Yearly Revenue: ${total_sales.quantize(CENT, rounding=ROUND_HALF_UP):,}")


generate_sales_data()
