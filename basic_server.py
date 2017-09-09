#!/usr/bin/env python
 
import BaseHTTPServer
 
HTML_DOC = """
<html>
   <head><title>hello!</title></head>
   <body>
       hey there <em>{:}</em>!
   </body>
</html>
"""
 
class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def send_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Connection", "close")
        self.end_headers()
       
    def do_index(self):
        self.send_headers()
        self.wfile.write(HTML_DOC.format(self.client_address))
       
    def do_hello(self, whom):
        self.send_headers()
        self.wfile.write(HTML_DOC.format(whom))
 
    def do_GET(self):
        if self.path == "/":
            self.do_index()
        elif self.path.startswith("/hello/"):
            self.do_hello(self.path[7:])
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.send_header("Connection", "close")
            self.end_headers()
           
            self.wfile.write("huh?!")
           
 
def main():
    httpd = BaseHTTPServer.HTTPServer(('', 8080), Handler)
 
    print "Ctr-c to quit..."
    try:
        httpd.serve_forever()
    except KeyboardInterrupt: pass
 
if __name__ == "__main__":
    main()