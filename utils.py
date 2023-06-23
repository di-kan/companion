import sqlite3
import random


def table_exists(cur, table_name):
    # get the count of tables with the name
    cnt = cur.execute(f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}' ''').fetchone()
    ret_value = False if cnt[0] == 0 else True
    return ret_value


def initialize_database(conn):
    cur = conn.cursor()
    if table_exists(cur, "language") == False:
        conn.execute('''CREATE TABLE language (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR NOT NULL,
        UNIQUE (name) ON CONFLICT IGNORE);''')
    if table_exists(cur, "word") == False:
        conn.execute('''CREATE TABLE word(
        id INTEGER PRIMARY KEY NOT NULL, 
        from_lang_id INTEGER KEY NOT NULL, 
        name VARCHAR NOT NULL,
        to_lang_id INTEGER KEY NOT NULL, 
        translation VARCHAR NOT NULL,
        FOREIGN KEY (from_lang_id) REFERENCES language(id),
        FOREIGN KEY (to_lang_id) REFERENCES language(id),                
        UNIQUE (name, translation) ON CONFLICT IGNORE
        );''')
    if table_exists(cur, "tag_type") == False:
        conn.execute('''CREATE TABLE tag_type (
        id INTEGER PRIMARY KEY NOT NULL,
        lang_id INTEGER KEY NOT NULL, 
        name VARCHAR NOT NULL,        
        FOREIGN KEY (lang_id) REFERENCES language(id),
        UNIQUE (lang_id, name) ON CONFLICT IGNORE
        );''')
    if table_exists(cur, "tag") == False:
        conn.execute('''CREATE TABLE tag (
        id INTEGER PRIMARY KEY NOT NULL, 
        tag_type_id INTEGER KEY NOT NULL, 
        name VARCHAR NOT NULL,
        FOREIGN KEY (tag_type_id) REFERENCES tag(id),
        UNIQUE (name) ON CONFLICT IGNORE
        );''')
    if table_exists(cur, "tagged") == False:
        conn.execute('''CREATE TABLE tagged (
        id INTEGER PRIMARY KEY NOT NULL,         
        word_id INTEGER KEY NOT NULL, 
        tag_id INTEGER KEY NOT NULL,
        FOREIGN KEY (word_id) REFERENCES word(id),
        FOREIGN KEY (tag_id) REFERENCES tag(id)
        );''')
    conn.commit()

def delete_table(conn, table):
    sql = f'DELETE FROM {table};'
    cur = conn.cursor()
    cur.execute(sql)

def delete_all_data(conn):
    delete_table(conn, 'word')
    delete_table(conn, 'tag_type')
    delete_table(conn, 'tag')
    delete_table(conn, 'tagged')
    conn.commit()

def add_demo_content(conn):
    insert_languages(conn)
    a_word = {"page":10, "word":"Hallo Welt", "translation":"Hello world"}
    the_word = {'word':a_word['word'],
                'translation':a_word['translation'],
                'from':'german',
                'to':'greek'}
    insert_word(conn, the_word)

    the_tag = {'page': a_word['page']}
    tag_word_by_dict(conn, the_word, the_tag)
    the_tag = {'count': random.randint(1000,2000)}
    tag_word_by_dict(conn, the_word, the_tag)

    a_word = {"page":10, "word":"Hallo Welt", "translation":"Hello over the world"}
    the_word = {'word':a_word['word'],
                'translation':a_word['translation'],
                'from':'german',
                'to':'greek'}
    insert_word(conn, the_word)

    the_tag = {'page': a_word['page']}
    tag_word_by_dict(conn, the_word, the_tag)
    the_tag = {'count': random.randint(1000,2000)}
    tag_word_by_dict(conn, the_word, the_tag)

    a_word = {"page": 10, "word": "Ja", "translation": "Yes"}
    the_word = {'word':a_word['word'],
                'translation':a_word['translation'],
                'from':'german',
                'to':'greek'}
    insert_word(conn, the_word)

    the_tag = {'page': a_word['page']}
    tag_word_by_dict(conn, the_word, the_tag)
    the_tag = {'count': random.randint(1000, 2000)}
    tag_word_by_dict(conn, the_word, the_tag)

    a_word = {"page": 10, "word": "genug", "translation": "Yes"}
    the_word = {'word':a_word['word'],
                'translation':a_word['translation'],
                'from':'german',
                'to':'greek'}

    insert_word(conn, the_word)
    the_tag = {'page': a_word['page']}
    tag_word_by_dict(conn, the_word, the_tag)
    the_tag = {'count': random.randint(1000, 2000)}
    tag_word_by_dict(conn, the_word, the_tag)
    conn.commit()


def insert_languages(conn):
    langs = ['german','greek']
    for lang in langs:
        sql = '''INSERT INTO language(name) VALUES(?)'''
        conn.execute(sql,(lang,))


def get_id(conn, table, criteria):
    #find the id of the name
    cur = conn.cursor()
    for key, value in criteria.items():
        key = key
        value = value
    sql = f"SELECT id FROM {table} WHERE {key}=?"
    ids = cur.execute(sql,(value,)).fetchall()
    if len(ids) == 1:
        ids = ids[0][0]
    else:
        ids = 0
    return ids


def tag_word_by_dict(conn, a_word, a_tag):
    cur = conn.cursor()
    #get word_id in combination with translation_id
    sql = "SELECT word.id FROM word WHERE word.name=? AND word.translation=?"
    word_ids = cur.execute(sql,(a_word['word'], a_word['translation'],)).fetchall()

    #check if tag_type exists
    the_key = list(a_tag.keys())[0]
    tag_type_id = get_id(conn, 'tag_type',{'name':the_key})
    # tag_type was not found in the db
    if tag_type_id == 0:
        insert_tag_type(conn, a_tag, a_word['from'])

    #check if tag_id exists
    tag_id = get_id(conn, 'tag', {'name': a_tag[the_key]})
    if tag_id == 0:
        insert_tag(conn, a_tag)
        tag_id = get_id(conn, 'tag', {'name': a_tag[the_key]})

    #finally tag word
    for word_id in word_ids:
        sql = "INSERT INTO tagged(word_id, tag_id) VALUES(?,?)"
        cur.execute(sql, (word_id[0], tag_id, ))


def tag_word_by_id(conn, word_id, a_tag):
    cur = conn.cursor()

    the_key = list(a_tag.keys())[0]
    tag_type_id = get_id(conn, 'tag_type',{'name':the_key})
    tag_id = get_id(conn, 'tag', {'name': a_tag[the_key]})

    #finally tag word
    sql = "INSERT INTO tagged(word_id, tag_id) VALUES(?,?)"
    cur.execute(sql, (word_id, tag_id, ))


def delete_tag(conn, a_tag):
    cur = conn.cursor()
    for key, value in a_tag.items():
        key = key
        value = value
    #Get tag type id
    sql = f"SELECT id FROM tag_type WHERE name=?"
    ids = cur.execute(sql, (key,)).fetchall()
    if len(ids) == 1:
        tag_type_id = ids[0][0]
    else:
        tag_type_id = 0
    sql = "DELETE FROM tag WHERE tag.name = ? AND tag.tag_type_id=?"
    ids = cur.execute(sql,(value, tag_type_id,)).fetchall()
    #Check if type tag has been orfan and delete it if so
    sql = "SELECT COUNT(id) FROM tag WHERE tag.tag_type_id = ?"
    ids = cur.execute(sql, (tag_type_id,)).fetchall()
    count = -1
    if len(ids) == 1:
        count = ids[0][0]
    if count == 0:
        sql = "DELETE FROM tag_type WHERE id = ?"
        cur.execute(sql, (tag_type_id,))



def insert_tag(conn, a_tag):
    cur = conn.cursor()
    sql = "INSERT INTO tag(name, tag_type_id) VALUES(?,?)"
    the_key = list(a_tag.keys())[0]
    tag_type_id = get_id(conn, 'tag_type', {'name':the_key})
    cur.execute(sql, (a_tag[the_key], tag_type_id,))


def insert_tag_type(conn, a_tag, lang):
    cur = conn.cursor()
    sql = "INSERT INTO tag_type(name, lang_id) VALUES(?,?)"
    the_key = list(a_tag.keys())[0]
    lang_id = get_id(conn,'language',{'name':lang})
    cur.execute(sql, (the_key, lang_id,))


def insert_word(conn, a_word):
    cur = conn.cursor()

    #find the id of the languages
    to_lang_id = get_id(conn,'language', {'name': a_word['to']})
    from_lang_id = get_id(conn,'language', {'name': a_word['from']})

    #insert word to the word table
    sql = "INSERT INTO word(name, from_lang_id, translation, to_lang_id) VALUES(?,?,?,?)"
    cur.execute(sql, (a_word['word'], from_lang_id, a_word['translation'], to_lang_id))
    return cur.lastrowid

def get_word_dict(conn, the_id):
    cur = conn.cursor()
    sql = "SELECT * FROM word WHERE id=?"
    cur.execute(sql, (the_id,))
def get_words_from_db(conn, filter = ""):
    cur = conn.cursor()
    if filter == "":
        sql = "SELECT word.id, word.name, word.translation, " \
              "GROUP_CONCAT(tag.id), GROUP_CONCAT(tag.name), GROUP_CONCAT(tag_type.name) " \
              "FROM word, tagged, tag, tag_type " \
              "WHERE word.id=tagged.word_id AND " \
              "tagged.tag_id=tag.id AND " \
              "tag_type.id=tag.tag_type_id " \
              "GROUP BY word.id"
    else:
        sql = "SELECT word.id, word.name, word.translation, " \
              "GROUP_CONCAT(tag.id), GROUP_CONCAT(tag.name), GROUP_CONCAT(tag_type.name) " \
              "FROM word, tagged, tag, tag_type " \
              "WHERE word.id=tagged.word_id AND " \
              "tagged.tag_id=tag.id AND " \
              "tag_type.id=tag.tag_type_id AND " \
              f"word.name LIKE '%{filter}%' " \
              "GROUP BY word.id"
    words = cur.execute(sql,).fetchall()
    ret_value = []
    for word in words:
        tag_ids = word[3].split(',')
        tag_vals = word[4].split(',')
        tag_keys = word[5].split(',')
        the_tags = []
        for i in range(0,len(tag_ids)):
            tmp_tag = {"tagid":tag_ids[i], tag_keys[i]:tag_vals[i]}
            the_tags.append(tmp_tag)
        word_row = {'id': word[0],
                    'word': word[1],
                    'translation': word[2],
                    'tags': the_tags}
        ret_value.append(word_row)
    return ret_value

def get_tags_from_db(conn):
    cur = conn.cursor()
    sql = "SELECT tag_type.name, GROUP_CONCAT(tag.name) " \
          "FROM tag, tag_type " \
          "WHERE tag.tag_type_id=tag_type.id " \
          "GROUP BY tag_type.name"
    tags = cur.execute(sql,).fetchall()
    ret_value = [{tag[0]:tag[1].split(',')} for tag in tags]
    return ret_value
