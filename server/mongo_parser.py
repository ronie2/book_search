from book_tree_parser import book_parser

def mongo_parser(book_tree, db_name="hallo"):
    """This def inserts book tree into mongodb and return mongo '_id' root"""
    from pymongo import MongoClient
    import pymongo

    client = MongoClient()
    db = client[db_name]

    # Create text search index on 'paragraphs' collection
    collection = db["paragraphs"]
    collection.create_index([("text", pymongo.TEXT), ])

    # Insert 'basic protos' to 'roots' collection
    collection = db["roots"]
    book_root = collection.insert_one({"name": book_tree["name"],"parts": []})

    # For every 'part' in book tree
    for part in book_tree["parts"]:
        # Add current 'part' to 'parts' collection
        collection = db["parts"]
        part_cur = collection.insert_one({"name": part["name"],
                               "root": book_root.inserted_id,
                               "chapters": []})

        # Update 'roots' record with inserted 'part' '_id'
        collection = db["roots"]
        collection.find_one_and_update({'_id': book_root.inserted_id},
                                   {"$push": {"parts": part_cur.inserted_id}})

        # Add all 'chapters' to 'chapters' collection
        for chapter in part["chapters"]:
            collection = db["chapters"]
            chapter_cur = collection.insert_one({"name": chapter["name"],
                                   "paragraphs": [],
                                   "root": part_cur.inserted_id})

            # Add all 'paragraphs' to 'chapters' collection
            for paragraph in chapter["paragraphs"]:
                collection = db["paragraphs"]
                paragraph_cur = collection.insert_one({"text": paragraph,
                                         "root": chapter_cur.inserted_id})

                # Update 'chapter' record with inserted 'paragraphs' '_id's
                collection = db["chapters"]
                collection.find_one_and_update({"_id": chapter_cur.inserted_id},
                                               {"$push":
                                                    {"paragraphs": paragraph_cur.inserted_id}})

        # Update 'part' record with inserted 'chapters' '_id's
        collection = db["parts"]
        collection.find_one_and_update({'_id': part_cur.inserted_id},
                                   {"$push": {"chapters": chapter_cur.inserted_id}})

    return book_root.inserted_id

if __name__ == "__main__":
    mo = [mongo_parser(book) for book in book_parser()]
    pass