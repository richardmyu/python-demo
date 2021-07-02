# -*- coding:utf-8 -*_

from http.server import BaseHTTPRequestHandler, HTTPServer
import sys, os


class RequestHandler(BaseHTTPRequestHandler):
    Page = """\
        <html>
        <body>
        <p>Hello wordl.</p>
        <p>Who are you?</p>
        <p>Where are you from?</p>
        <p>What do you want to do?</p>
        <table>
        <tr>  <td>Header</td>         <td>Value</td>          </tr>
        <tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
        <tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
        <tr>  <td>Client port</td>    <td>{client_port}</td>  </tr>
        <tr>  <td>Command</td>        <td>{command}</td>      </tr>
        <tr>  <td>Path</td>           <td>{path}</td>         </tr>
        </table>
        </body>
        </html>
    """

    def do_GET(self):
        # page = self.create_page()
        # self.send_content(page)
        try:
            full_path = os.getcwd() + self.path

            if not os.path.exists(full_path):
                raise ServerException('{0} not fund'.format(self.path))
            elif os.path.isfile(full_path):
                self.handle_file(full_path)
            else:
                raise ServerException('Unknown object "{0}"'.format(self.path))
        except Exception as msg:
            self.handle_error(msg)

    def create_page(self):
        values = {
            'date_time': self.date_time_string(),
            'client_host': self.client_address[0],
            'client_port': self.client_address[1],
            'command': self.command,
            'path': self.path
        }
        page = self.Page.format(**values)
        return page

    def send_content(self, page):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(page)))
        self.end_headers()
        # self.wfile.write(page.encode('utf-8'))
        self.wfile.write(page)

    def handle_file(self, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            self.send_content(content)
        except IOError as msg:
            msg = '"{0}" cannot be read: {1}'.format(self.path, msg)
            self.handle_error(msg)


class ServerException(Exception):
    Error_Page = """\
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
    """

    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content.encode('utf-8'))


if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()  # -*- coding:utf-8 -*_

from http.server import BaseHTTPRequestHandler, HTTPServer
import sys, os


class RequestHandler(BaseHTTPRequestHandler):
    Page = """\
        <html>
        <body>
        <p>Hello wordl.</p>
        <p>Who are you?</p>
        <p>Where are you from?</p>
        <p>What do you want to do?</p>
        <table>
        <tr>  <td>Header</td>         <td>Value</td>          </tr>
        <tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
        <tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
        <tr>  <td>Client port</td>    <td>{client_port}</td>  </tr>
        <tr>  <td>Command</td>        <td>{command}</td>      </tr>
        <tr>  <td>Path</td>           <td>{path}</td>         </tr>
        </table>
        </body>
        </html>
    """

    def do_GET(self):
        # page = self.create_page()
        # self.send_content(page)
        try:
            full_path = os.getcwd() + self.path

            if not os.path.exists(full_path):
                raise ServerException('{0} not fund'.format(self.path))
            elif os.path.isfile(full_path):
                self.handle_file(full_path)
            else:
                raise ServerException('Unknown object "{0}"'.format(self.path))
        except Exception as msg:
            self.handle_error(msg)

    def create_page(self):
        values = {
            'date_time': self.date_time_string(),
            'client_host': self.client_address[0],
            'client_port': self.client_address[1],
            'command': self.command,
            'path': self.path
        }
        page = self.Page.format(**values)
        return page

    def send_content(self, page):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(page)))
        self.end_headers()
        # self.wfile.write(page.encode('utf-8'))
        self.wfile.write(page)

    def handle_file(self, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            self.send_content(content)
        except IOError as msg:
            msg = '"{0}" cannot be read: {1}'.format(self.path, msg)
            self.handle_error(msg)


class ServerException(Exception):
    Error_Page = """\
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
    """

    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content.encode('utf-8'))


if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
