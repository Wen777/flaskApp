# -*- coding: utf-8 -*-
from app import db
from models import BlogPost

# create the database and the db tables
db.create_all()

# insert

db.session.add(BlogPost('Good', "I\'m good."))
db.session.add(BlogPost('Well', "I\'m doing well."))

# commit the change

db.session.commit()