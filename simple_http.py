import configparser
from http.server import HTTPServer, BaseHTTPRequestHandler
from functools import partial
import psycopg2


class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, cursor, *args, **kwargs):
        self.cursor = cursor
        super().__init__(*args, **kwargs)

    def add_row(self, html_str, title, img_url):
        pretty_title = ', '.join(title.replace('https://www.sreality.cz/detail/', '').split('/')[:-1])
        html_str += f'<tr><td><a href={title}>{pretty_title}</td>\n'
        html_str += f'<td><img src={img_url} alt=""/></td></tr>\n'
        return html_str

    def build_html(self):
        html_str = ''
        html_str += '<html><head><title>Luxonis test exercise.</title></head>\n'
        html_str += '<body><p>Images of SReality flats for sale.</p>\n'
        html_str += '<table border="1">\n'
        html_str += f'<tr><td>Flat</td>\n'
        html_str += f'<td>Image</td></tr>\n'
        
        self.cursor.execute("""SELECT title, url FROM img_urls ORDER BY title ASC""")
        res = self.cursor.fetchall()
        for item in res:
            html_str = self.add_row(html_str, item[0], item[1])
        
        html_str += '</table>\n'
        html_str += '</body></html>'
        return html_str

    def do_GET(self):
        html_str = self.build_html()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(html_str, "utf-8"))


def main():
    config = configparser.ConfigParser()
    config.read('db.ini')
    hostname = config.get('postgresql', 'hostname')
    username = config.get('postgresql', 'username')
    password = config.get('postgresql', 'password')
    database = config.get('postgresql', 'database')
    
    connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    cur = connection.cursor()
    
    handler = partial(MyHandler, cur)
    httpd = HTTPServer(('localhost', 8080), handler)
    try:
        httpd.serve_forever()
    except:
        httpd.close()
    
    cur.close()
    connection.close()

if __name__ == "__main__":
    main()

