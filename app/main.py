from flask import Flask, request, render_template, redirect
from math import floor
import string
from urllib.parse import urlparse
from string import ascii_lowercase, ascii_uppercase
import psycopg2
import os
import logging

dbhost = os.environ.get("POSTGRES_DB_HOST")
dbuser = os.environ.get("POSTGRES_DB_USER")
dbpass = os.environ.get("POSTGRES_DB_PASSWORD")

connect_str = "dbname='shorturl' user='{}' host='{}' password='{}'".format(dbuser, dbhost, dbpass)

app = Flask(__name__)
host = 'http://127.0.0.1:5000/'
# to make it work on a VM or Kubernetes, the host has to be ip:port, or hostname port
# TODO: setup a static IP, create a DNS record and make this an environment variable


def table_check():
    try:
        conn = psycopg2.connect(connect_str)
        create_table = """
            CREATE TABLE if NOT EXISTS WEB_URL(
            ID SERIAL,
            URL TEXT NOT NULL
            );
            """
        with conn.cursor() as cursor:
            try:
                cursor.execute(create_table)
                conn.close()
            except psycopg2.Error as err1:
                logging.error('Error creating table: ' + err1)
    except psycopg2.Error as err2:
        logging.error('Error connecting to db: ' + err2)


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
    conn.autocommit = True
    if request.method == 'POST':
        original_url = request.form.get('url')
        if urlparse(original_url).scheme == '':
            url = 'http://' + original_url
        else:
            url = original_url
        try:
            with conn.cursor() as cursor:
                q = "INSERT INTO WEB_URL (URL) VALUES ('{}') RETURNING id;".format(url)
                cursor.execute(q)
                encoded_string = toBase62(cursor.fetchone()[0])
                conn.close()
                return render_template('home.html', short_url=host + encoded_string)
        except psycopg2.Error as err:
            logging.error('Database error: ' + err)
    return render_template('home.html')


@app.route('/<short_url>')
def redirect_short_url(short_url):
    conn = psycopg2.connect(connect_str)
    decoded = toBase10(short_url)
    url = host  # fallback if no URL is found
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT URL FROM WEB_URL WHERE ID={}".format(decoded))
            url = cursor.fetchone()[0]
    except psycopg2.Error as err:
        logging.error('Database error: ' + err)
    return redirect(url)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    table_check()
    app.run(host='0.0.0.0', port=5000)
