import csv

def fetch_id(item_name : str, table_name : str )->str:
    """
    fetches string id given item and table 
    
    Parameters
    ----------
    item_name : str 
        name of item whose id will be fetched 
    table_name : str
        name of table
    
    Returns
    ----------
    str 
        string id of menu item
    """
    with open(table_name + '.csv', mode="r", newline='') as csv_file:     
       for line in csv.reader(csv_file):
           if line[1] == item_name:
               return line[0]
    
    raise Exception(f"id of {item_name} not found")


with open("MenuItemCutlery.csv", mode="w") as csv_file:
    headers:list = ["menu_item_id", "cutlery_id", "quantity"] 
    writer : csv.DictWriter = csv.DictWriter(csv_file, fieldnames=headers)
    writer.writeheader()

    while True:
        opt : str = input("Opt: ")
        if opt == "a": 
            cutlery_name : str = input("cutlery: ")
            menu_item_name : str = input("menu item: ")
            quantity : str = input("quantity: ")
            
            try:
                cutlery_id = fetch_id(item_name = cutlery_name, table_name = "Cutlery")
            except:
                print("invalid cutlery item")
                continue

            try:
                menu_item_id = fetch_id(item_name = menu_item_name, table_name = "MenuItem")
            except:
                print("invalid menu item")
                continue

            writer.writerow({
                "menu_item_id" : menu_item_id,
                "cutlery_id" : cutlery_id,
                "quantity" : quantity
                }) 
        else:
            print("done!")
            break;
