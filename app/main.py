from flask import Flask, request, render_template, redirect
from math import floor
import string
from urllib.parse import urlparse
from string import ascii_lowercase, ascii_uppercase
import base64
import psycopg2
import os
import logging

dbhost = os.environ.get("POSTGRES_DB_HOST")
dbuser = os.environ.get("POSTGRES_DB_USER")
dbpass = os.environ.get("POSTGRES_DB_PASSWORD")

connect_str = "dbname='shorturl' user='{}' host='{}' password='{}'".format(dbuser, dbhost, dbpass)


app = Flask(__name__)
host = 'http://0.0.0.0:5000/'


def table_check():
    try:
        conn = psycopg2.connect(connect_str)
        create_table = """
            CREATE TABLE WEB_URL(
            ID INT PRIMARY KEY AUTOINCREMENT,
            URL TEXT NOT NULL
            );
            """
        with conn:
            cursor = conn.cursor()
            try:
                cursor.execute(create_table)
            except Exception as ex:
                logging.error(ex)
    except Exception as e:
        logging.error(e)


def toBase62(num, b=62):
    if b <= 0 or b > 62:
        return 0
    base = string.digits + ascii_lowercase + ascii_uppercase
    r = num % b
    res = base[r]
    q = floor(num / b)
    while q:
        r = q % b
        q = floor(q / b)
        res = base[int(r)] + res
    return res


def toBase10(num, b=62):
    base = string.digits + ascii_lowercase + ascii_uppercase
    limit = len(num)
    res = 0
    for i in range(limit):
        res = b * res + base.find(num[i])
    return res


@app.route('/', methods=['GET', 'POST'])
def home():
    conn = psycopg2.connect(connect_str)
    if request.method == 'POST':
        original_url = str.encode(request.form.get('url'))
        if urlparse(original_url).scheme == '':
            url = 'http://' + original_url
        else:
            url = original_url
        with conn:
            cursor = conn.cursor()
            res = cursor.execute(
                'INSERT INTO WEB_URL (URL) VALUES (?)',
                [base64.urlsafe_b64encode(url)]
            )
            encoded_string = toBase62(res.lastrowid)
        return render_template('home.html', short_url=host + encoded_string)
    return render_template('home.html')


@app.route('/<short_url>')
def redirect_short_url(short_url):
    conn = psycopg2.connect(connect_str)
    decoded = toBase10(short_url)
    url = host  # fallback if no URL is found
    with conn:
        cursor = conn.cursor()
        res = cursor.execute('SELECT URL FROM WEB_URL WHERE ID=?', [decoded])
        try:
            short = res.fetchone()
            if short is not None:
                url = base64.urlsafe_b64decode(short[0])
        except Exception as e:
            logging.error(e)
    return redirect(url)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info("connect_str")
    logging.info(connect_str)
    table_check()
    app.run(host='0.0.0.0', port=5000)
