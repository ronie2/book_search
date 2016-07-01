def book_parser():
    """book_parser function returning generator object of parse_book() function

    Args:
        None

    Returns:
        generator object of parse_book() function.

    """
    from os import listdir
    from os.path import join
    import os.path

    # Full path to 'server' directory
    server_dir = os.path.abspath(__file__ + "/../")
    db_folder = server_dir + "/db/basic_data/"

    return (parse_book(join(db_folder + file)) for file in listdir(db_folder))


def parse_book(filename, title=None):
    """parse_book function returning book_tree dict with book content

    Args:
        filename (str): full path to file say '/book_search/server/db/book_name.txt'
        title (str): title of a book say "Anna Karenina". If not provided 'title' = filename 'book_name'

    Returns:
        dict 'book_tree' object in this format:

            book_tree = {
            "name": book_name,
            "parts": [{
                        "name": part_name,
                        "chapters": [{
                            "name": None,
                            "paragraphs": [{
                                "text": []
                                }]
                        }]
            }]
        }

    """

    from copy import deepcopy
    from collections import deque

    # Define elements prototypes
    paragraph_prototype = {"text": []}
    chapter_prototype = {"name": None, "paragraphs": []}
    part_prototype = {"name": None, "chapters": []}
    book_prototype = {"name": None, "parts": []}

    # Create initial clean copies
    book_tree = deepcopy(book_prototype)
    part = deepcopy(part_prototype)
    chapter = deepcopy(chapter_prototype)
    paragraph = deepcopy(paragraph_prototype)

    # Flags to remove 'publishers text' at start of a file
    ch_started = False
    pt_started = False
    par_started = False

    # If title is provided => use this title
    if title:
        book_tree["name"] = title

    # If no title => title equals to '*.txt' file name
    else:
        book_tree["name"] = filename.split("/")[-1].split(".")[:-1][0]

    # Load book to deque of lines
    with open(filename, "r", encoding="utf-8") as f:
        book = deque([line for line in f])

    # While deque of lines has something
    while book:

        # Take one line from the deque
        line = book.popleft()

        # PART detection and processing
        if "PART" in line:
            # If this is not first occurrence
            if pt_started:
                book_tree["parts"].append(part)
                part = deepcopy(part_prototype)
                words_list = line.split()
                part["name"] = " ".join(words_list[1:len(words_list)])
            # If this really is a first occurrence
            else:
                pt_started = True
                words_list = line.split()
                part["name"] = " ".join(words_list[1:len(words_list)])

        # Chapter detection and processing
        if ("Chapter" in line) or ("CHAPTER" in line):
            # If this is not first Chapter occurrence
            if ch_started:
                part["chapters"].append(chapter)
                chapter = deepcopy(chapter_prototype)
                words_list = line.split()
                chapter['name'] = " ".join(words_list[1:len(words_list)])
            # If this really is a first Chapter occurrence
            else:
                ch_started = True
                words_list = line.split()
                chapter['name'] = " ".join(words_list[1:len(words_list)])

        # Paragraphs detection and processing
        elif ch_started:
            # If this is NOT just a blank line => add it to paragraph
            if line != "\n":
                paragraph["text"].append(line)
                par_started = True
            # If this is just a blank line and paragraph started =>
            # add to chapter and create new paragraph
            if line == "\n" and par_started:
                paragraph_text = "".join(paragraph["text"]).replace("\n", " ")
                chapter["paragraphs"].append(paragraph_text)
                par_started = False
                paragraph = deepcopy(paragraph_prototype)

    # If reached end of file
    else:

        # Add current 'chapter' dict to part["chapters"] dict
        part["chapters"].append(chapter)

        # Add current part dict to 'book_tree["parts"]'
        book_tree["parts"].append(part)

    return book_tree
