from pymongo import MongoClient, errors
from bson.objectid import ObjectId

#mongodb+srv://rhett6butler:<db_password>@rdd.fgx0a.mongodb.net/?retryWrites=true&w=majority&appName=rdd

from pymongo.server_api import ServerApi

def get_db():
    """Connect to MongoDB"""
    try:
        client = MongoClient(
            "mongodb+srv://rhett6butler:p123456p@rdd.fgx0a.mongodb.net/?retryWrites=true&w=majority&appName=rdd",
            server_api=ServerApi('1')
        )
        #print(client.server_info())  # Check connection
        return client["cats_db"], client
    except errors.PyMongoError as e:
        print(f"Error connecting to MongoDB: {e}")
        return None, None

def create_cat(name, age, features):
    """Add a new cat to the collection"""
    db, client = get_db()
    if db is not None:
        try:
            cat = {"name": name, "age": age, "features": features}
            db.cats.insert_one(cat)
            print(f"Cat {name} added!")
        except errors.PyMongoError as e:
            print(f"Error adding cat: {e}")
        finally:
            client.close()

def read_all_cats():
    """Display all cats"""
    db, client = get_db()
    if db is not None:
        try:
            for cat in db.cats.find():
                print(cat)
        except errors.PyMongoError as e:
            print(f"Error reading data: {e}")
        finally:
            client.close()

def read_cat_by_name(name):
    """Find a cat by name"""
    db, client = get_db()
    if db is not None:
        try:
            cat = db.cats.find_one({"name": name})
            if cat:
                print(cat)
            else:
                print(f"Cat named {name} not found.")
        except errors.PyMongoError as e:
            print(f"Error searching for cat: {e}")
        finally:
            client.close()

def update_cat_age(name, new_age):
    """Update the age of a cat by name"""
    db, client = get_db()
    if db is not None:
        try:
            result = db.cats.update_one({"name": name}, {"$set": {"age": new_age}})
            if result.modified_count:
                print(f"Cat {name}'s age updated to {new_age} years.")
            else:
                print(f"Cat {name} not found.")
        except errors.PyMongoError as e:
            print(f"Error updating cat's age: {e}")
        finally:
            client.close()

def add_feature_to_cat(name, feature):
    """Add a new feature to a cat"""
    db, client = get_db()
    if db is not None:
        try:
            result = db.cats.update_one({"name": name}, {"$push": {"features": feature}})
            if result.modified_count:
                print(f"Feature '{feature}' added to cat {name}.")
            else:
                print(f"Cat {name} not found.")
        except errors.PyMongoError as e:
            print(f"Error adding feature: {e}")
        finally:
            client.close()

def delete_cat(name):
    """Delete a cat by name"""
    db, client = get_db()
    if db is not None:
        try:
            result = db.cats.delete_one({"name": name})
            if result.deleted_count:
                print(f"Cat {name} deleted.")
            else:
                print(f"Cat {name} not found.")
        except errors.PyMongoError as e:
            print(f"Error deleting cat: {e}")
        finally:
            client.close()

def delete_all_cats():
    """Delete all cats"""
    db, client = get_db()
    if db is not None:
        try:
            db.cats.delete_many({})
            print("All cats deleted.")
        except errors.PyMongoError as e:
            print(f"Error deleting all cats: {e}")
        finally:
            client.close()

# Usage examples
if __name__ == "__main__":
    create_cat("Barsik", 3, ["wears slippers", "allows petting", "ginger"])
    read_all_cats()
    read_cat_by_name("Barsik")
    update_cat_age("Barsik", 4)
    add_feature_to_cat("Barsik", "loves sleeping")
    delete_cat("Barsik")
    delete_all_cats()
