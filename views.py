import csv
from models import House

def get_house():
    return House.select()

def write_csv(house):
    """write data in csv file"""   
    
    with open('house.csv', 'a') as csv_file:
        fieldnames = ['id', 'title', 'description', 'location', 'price', 'bedroom', 'posted_at', 'currency', 'image']
        writer = csv.DictWriter(csv_file, delimiter=',', fieldnames=fieldnames)
        
        for i in house:
            data = {
                'title': i.id,
                'description': i.description,
                'location': i.location,
                'price': i.price,
                'bedroom': i.bedroom,
                'posted_at': i.posted_at,
                'currency': i.currency,
                'image': i.image
            }
            writer.writerow(data)
