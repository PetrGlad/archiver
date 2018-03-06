import os
from os.path import join, getsize
import hashlib
# import base64
import binascii
import sqlite3
import itertools
import sys


def iter_files(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            yield join(root, f)


# See also https://stackoverflow.com/a/3431835/117220
def hash_file(file_name):
    return hashlib.sha256(open(file_name, 'rb').read()).digest()


def open_db(file_db):
    db = sqlite3.connect(file_db)
    db.cursor().execute('''CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        path TEXT, 
        sha256 TEXT, 
        size INT)''')
    db.commit()
    return db


def insert_file(db, file_path, sha256, file_size):
    db.cursor().execute('''INSERT INTO files (path, sha256, size)
                           VALUES (?, ?, ?)''',
                        (file_path, sha256, file_size))
    db.commit()


def register_file(db, file_path):
    try:
        insert_file(db, file_path, binascii.b2a_hex(hash_file(file_path)), getsize(file_path))
    except FileNotFoundError:
        print('WARN File not found {}'.format(file_path), file=sys.stderr)


# from flask import Flask
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'


# if __name__ == '__main__':
#     app.run()

def scan_files(root_path, db_name):
    n = 0
    with open_db(db_name) as db:
        for file_path in iter_files(root_path):
            if os.path.isfile(file_path):
                register_file(db, file_path)
                print('OK', n, file_path)
            else:
                print('WARN Skipping special file {}'.format(file_path), file=sys.stderr)
            n += 1


def show_files(db):
    for r in db.cursor().execute('SELECT rowid, * FROM files'):
        print(r)


if __name__ == '__main__':
    scan_files('/home/petr/archive', 'archive-2018-02.db')
