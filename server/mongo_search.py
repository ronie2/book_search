from config.conf import mongo_cfg

def mongo_search(search_term, db_name=mongo_cfg["db_name"]):
    """mongo_search function searches over 'paragraph' collection and returns
    generator object of search result dicts

    Args:
        search_term (str): term to find in database
        db_name (str): name of mongodb database to use

    Returns:
        generator object of dicts like:
        {
            'result': get_search_results(paragraph),
             'search_term': search_term
         }
    """
    from pymongo import MongoClient
    client = MongoClient()
    db = client[db_name]
    collection = db["paragraphs"]

    def get_search_results(paragraph):
        """get_search_results coroutine creates search results dicts

        Args:
            paragraph (mongodb_cursor): cursor over search results

        Returns:
            Search result dict in this format:
            {
                "book": book["name"],
                "part": part["name"],
                "chapter": chapter["name"],
                "paragraph": count,
                "text": paragraph["text"]
            }
        """
        chapter = db["chapters"].find_one({"_id": paragraph["root"]})
        count = chapter["paragraphs"].index(paragraph["_id"]) + 1

        # Find paragraph position in chapter
        for index, item in enumerate(chapter["paragraphs"], start=1):
            if item == paragraph["_id"]:
                count = index
                break

        part = db["parts"].find_one({"_id": chapter["root"]})
        book = db["roots"].find_one({"_id": part["root"]})

        return {
            "book": book["name"],
            "part": part["name"],
            "chapter": chapter["name"],
            "paragraph": count,
            "text": paragraph["text"]
        }

    return ({"result": get_search_results(item), "search_term": search_term}
            for item in collection.find({"$text": {"$search": search_term}}))

if __name__ == "__main__":
    res = list(find_phrase("War"))
    pass