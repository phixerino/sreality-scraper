import psycopg2
import time
import configparser


class PostgresSQLPipeline:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('/usr/src/app/db.ini')
        hostname = config.get('postgresql', 'hostname')
        username = config.get('postgresql', 'username')
        password = config.get('postgresql', 'password')
        database = config.get('postgresql', 'database')
        
        time.sleep(5)
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

        self.cur = self.connection.cursor()
        self.cur.execute('''
        DROP TABLE IF EXISTS img_urls
        ''')
        self.cur.execute('''
        CREATE TABLE img_urls(
            id serial PRIMARY KEY,
            title text,
            url text
        )
        ''')

    def process_item(self, item, spider):
        self.cur.execute('''insert into img_urls (title, url) values (%s,%s)''', (item['title'], item['url']))
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

