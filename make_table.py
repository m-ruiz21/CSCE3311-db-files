import csv
import uuid

# Open the CSV file
with open('MenuItem.csv', 'r') as csv_file:
    # Create a CSV reader
    reader = csv.reader(csv_file)
    # Get the header row and store the fieldnames
    header = next(reader)
    fieldnames = header.copy()
    # Create a list to hold the updated data
    updated_data = [header]
    # Loop through each row in the CSV file
    for row in reader:
        # Generate a UUID if the row has an 'id' field
        if row[0].strip() != '' and row[0].strip() != 'id':
            row[0] = str(uuid.uuid1())
        # Generate a UUID if the row has an 'ingredient_id' field
        if len(row) == 5 and row[4].strip() != '' and row[4].strip() != 'ingredient_id':
            row[4] = str(uuid.uuid1())
        # Add the updated row to the list
        updated_data.append(row)

# Open the CSV file for writing
with open('MenuItem.csv', 'w', newline='') as csv_file:
    # Create a CSV writer
    writer = csv.writer(csv_file)
    # Write the updated data to the CSV file
    writer.writerows(updated_data)

