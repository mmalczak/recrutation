import pymongo


conn = pymongo.MongoClient()
db = conn.snort_db
db.add_user('milosz', 'milosz', roles=[{'role':'readWrite', 'db':'snort_db'}])

