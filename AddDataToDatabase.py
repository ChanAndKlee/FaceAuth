import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL" : "https://facelogin-5c710-default-rtdb.firebaseio.com/",
})

# Create Students folder
ref = db.reference('Students')

data = {
    "6188488":
    {
        "name" : "Joe Biden",
        "major" : "Arts",
        "starting_year" : "2000",
        "bloodType" : "AB",
        "year" : 4,
        "last_authenticated" : "2022-04-10 03:45:09"
    },
    "6288123":
    {
        "name" : "Donald Trump",
        "major" : "Law",
        "starting_year" : "1998",
        "bloodType" : "O",
        "year" : 2,
        "last_authenticated" : "2022-01-15 07:14:55"
    },
     "6388030":
    {
        "name" : "Kulawut Makkamoltham",
        "major" : "ICT",
        "starting_year" : "2020",
        "bloodType" : "A",
        "year" : 3,
        "last_authenticated" : "2022-02-22 12:00:01"
    },
    # "6388040":
    # {
    #     "name" : "Ariya Phengphon",
    #     "major" : "ICT",
    #     "starting_year" : "2020",
    #     "bloodType" : "B",
    #     "year" : 3,
    #     "last_authenticated" : "2022-12-26 11:45:00"
    # },
    "6388176":
    {
        "name" : "Prawit Wongsuwon",
        "major" : "ICT",
        "starting_year" : "2000",
        "bloodType" : "O",
        "year" : 10,
        "last_authenticated" : "2022-12-26 11:45:00"
    },
}

# Send data to the DB
for key, value in data.items():
    ref.child(key).set(value)