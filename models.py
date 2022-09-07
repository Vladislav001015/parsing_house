import peewee
from settings_db import db

class House(peewee.Model): # models House for db
    
    id = peewee.PrimaryKeyField(null=False)
    title = peewee.CharField()
    location = peewee.CharField()
    description = peewee.TextField()
    price = peewee.DecimalField(max_digits=20, decimal_places=10)
    bedroom = peewee.CharField(max_length=50)
    posted_at = peewee.DateField(formats=['%d-%m-%Y'])
    image = peewee.CharField()
    currency = peewee.CharField()
    
    class Meta:
        database = db
        db_table = 'houses'
        order_by = ('id',)

db.connect()
House.create_table()


