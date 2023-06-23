import pandas as pd
from flask import Flask, redirect, url_for, flash, request, render_template, flash, session, g
from flask_session import Session
import os.path
from werkzeug.utils import secure_filename
import utils
import sqlite3

#-------------------------------
#INIT SOME VARIABLES
#--------------------------------
tags_filename = "tags.json"
words_filename = "words.json"
upload_folder = './uploads'
db_file = "gervoc.db"
allowed_extensions = {'csv', 'txt'}


#--------------------------------
#NON-FLASK/APP FUNCTIONS
#--------------------------------
# def what_tag(ind):


def load_tags(filename):
    if os.path.exists(filename):
        tmp_tags = pd.read_json(filename)
    else:
        tmp = {'name': ['general', 'normal', 'non-normal', 'modal', 'general', 'female', 'male', 'neutral'],
               'category': ['verb', 'verb', 'verb', 'verb', 'noun', 'noun', 'noun', 'noun']}
        tmp_tags = pd.DataFrame(tmp)
        tmp_tags.to_json(filename)
    return tmp_tags



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def open_db():
    conn = getattr(g,'_database', None)
    if conn is None:
        conn = g._database = sqlite3.connect(db_file)
        conn.enable_load_extension(True)
    return conn


#--------------------------------
#APP FUNCTIONS FLASK START HERE
#--------------------------------
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_folder
app.debug = True

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def show_index():
    global conn
    conn = open_db()
    utils.initialize_database(conn)
    # utils.add_demo_content(conn)
    return render_template("index.html")

@app.route('/deleteall')
def delete_all():
    flash('Database will become empty')
    global conn
    conn = open_db()
    utils.delete_all_data(conn)
    return redirect("/")

@app.route('/demo')
def demo():
    flash('Demo content was added')
    global conn
    conn = open_db()
    utils.add_demo_content(conn)
    return redirect("/words")


@app.route('/words')
def show_words():
    global conn
    conn = open_db()
    words = utils.get_words_from_db(conn)
    return render_template("words.html", words=words)


@app.route('/import', methods=['POST', 'GET'])
def import_words():
    global conn
    conn = open_db()

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_words = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename), delimiter=":", header=None)
            new_words.rename(columns={0: 'page', 1:'word', 2: 'translation'}, inplace=True)
            for word in new_words.iterrows():
                a_word=word[1]
                the_word = {'word':a_word['word'],
                            'translation':a_word['translation'],
                            'from':'german',
                            'to':'greek'}
                utils.insert_word(conn, the_word)
                the_tag = {'page':a_word['page']}
                utils.tag_word_by_dict(conn, the_word, the_tag)
            conn.commit()
            return redirect("/words")
    return render_template("import.html")

@app.route('/tags', methods=['GET', 'POST'])
def tags():
    global conn
    conn = open_db()

    if request.method == 'POST':
        the_form = request.form
        if 'to_delete' in the_form.keys():
            tmp = the_form['to_delete'].split(":")
            the_tag = {tmp[0]:tmp[1]}
            utils.delete_tag(conn, the_tag)
            conn.commit()
        else:
            the_tag = {the_form['type']: the_form['tag']}
            utils.insert_tag_type(conn, the_tag, 'german')
            utils.insert_tag(conn, the_tag)
            conn.commit()
    tags = utils.get_tags_from_db(conn)
    return render_template("tags.html",tags=tags)


@app.route('/tagwords', methods=['GET', 'POST'])
def tag_words():
    global conn
    conn = open_db()
    if request.method == 'POST':
        the_form = request.form
        if 'filter' in the_form.keys():
            if the_form.get('case-sensitive'):
                filter = f"'{the_form['filter']}'"
            else:
                filter = f"'(?i){the_form['filter']}'"
            words = utils.get_words_from_db(conn,the_form['filter'])
            tags = utils.get_tags_from_db(conn)
            return render_template('tagwords.html', words=words, tags=tags)
        else:
            for word in the_form.items():
                form_info = word[0].split('-')
                word_id = form_info[0]
                the_tag = {form_info[1]:form_info[2]}
                utils.tag_word_by_id(conn, word_id, the_tag)
            conn.commit()
            return render_template('tagwords.html')
    else:
        return render_template('tagwords.html')


if __name__ == '__main__':
    conn = None
    app.secret_key = '@xm@164'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)
    app.run()
