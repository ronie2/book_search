def book_parser(
        db_folder=
                "/home/ronie/PycharmProjects/book_search/server/db/"):
    """This def parses book content tree
    It creates tree for books with following markup:

    Title:
    Tree:
        - 'PART' NAME
        -- 'Chapter' NAME
        --- Text

    """
    from os import listdir
    from os.path import join

    return (parse_book(join(db_folder + file)) for file in listdir(db_folder))


def parse_book(filename):
    from copy import deepcopy
    from collections import deque
    import codecs

    # Define elements prototypes and create initial clean copies
    paragraph_prototype = {"text": []}
    chapter_prototype = {"name": None, "paragraphs": []}
    part_prototype = {"name": None, "chapters": []}
    book_prototype = {"name": None, "parts": []}

    book_dict = deepcopy(book_prototype)
    part = deepcopy(part_prototype)
    chapter = deepcopy(chapter_prototype)
    paragraph = deepcopy(paragraph_prototype)

    # Flags to remove 'publishers text' at start of a file
    ch_started = False
    pt_started = False
    par_started = False

    # Book title equals to file name
    book_dict["name"] = filename.split("/")[-1].split(".")[:-1]

    # Load book to deque of lines
    with codecs.open(filename, "r+", encoding="utf-8", errors='ignore') as f:
        book = deque([line for line in f])

    # While deque of lines has something
    while book:

        line = book.popleft()

        # PART detection and processing
        if "PART" in line:
            # If this is not first occurrence
            if pt_started:
                book_dict["parts"].append(part)
                part = deepcopy(part_prototype)

            # If this really is first occurrence
            pt_started = True
            words_list = line.split()
            part["name"] = " ".join(words_list[1:len(words_list)])

        # Chapter detection and processing
        if "Chapter" in line:
            # If this is not first occurrence
            if ch_started:
                part["chapters"].append(chapter)
                chapter = deepcopy(chapter_prototype)
            # If this really is first occurrence
            ch_started = True
            words_list = line.split()
            chapter['name'] = " ".join(words_list[1:len(words_list)])

        # CHAPTER TEXT detection and processing
        elif ch_started:

            if line != "\n":
                paragraph["text"].append(line)
                par_started = True

            if line == "\n" and par_started:
                paragraph_text = "".join(paragraph["text"]).replace("\n", " ")
                chapter["paragraphs"].append(paragraph_text)
                par_started = False
                paragraph = deepcopy(paragraph_prototype)

    return book_dict

if __name__ == "__main__":
    book = list(book_parser())
    pass