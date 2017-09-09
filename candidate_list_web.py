import BaseHTTPServer
import json
 
HTML_DOC = """
<html>
   <head><title>hello!</title></head>
   <body>
       hey there <em>{:}</em>!
   </body>
</html>
"""

logo = "http://www.pricelinegroup.com/wp-content/uploads/2014/03/5_Logo_Booking-435x71@2x-435x71@2x.png"
logo_scale = 0.2
 
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
    
    def do_badges(self):
        with open('data.json','r') as fh:
            candidates = json.load(fh)
        
        self.send_headers()
        self.wfile.write("""
            <html>
            <head>
                <title>Candidates list</title>
                <style>
                body {
                    font-family:Verdana;
                    font-size:18px;
                }
                .label {
                    width:10cm;
                    height:5cm;
                    border:0.25px solid black;
                    padding-top:5mm;
                    padding-left:5mm;
                    float:left;
                }
                .name {
                    margin-top:1cm;
                    margin-left:1cm;
                    font-weight:bold;  
                }
                .title {
                    margin-left:1cm;
                    font-variant:italic;
                    font-size:80%;
                }
                </style>
            </head>
            <body>"""
        )
        
        for candidate in sorted(candidates, key=lambda c: (c['last_name'], c['first_name'])):
            self.wfile.write("""
            <div class="label">
                <img src="{logo}" width="{width}" height="{height}">
                <div class="name">{first}&nbsp;{last}</div>
                <div class="title">{title}</div>
            </div>""".format(
                first=candidate['first_name'], last=candidate['last_name'], title=candidate['title'],
                logo=logo, width=870*logo_scale, height=142*logo_scale)
            )
        
        self.wfile.write("</body></html>")
        
    def do_GET(self):
        if self.path == "/":
            self.do_index()
        elif self.path.startswith("/hello/"):
            self.do_hello(self.path[7:])
        elif self.path == "/badges":
            self.do_badges()
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.send_header("Connection", "close")
            self.end_headers()
           
            self.wfile.write("huh?!")
           
def main():
    httpd = BaseHTTPServer.HTTPServer(('', 8080), Handler)
 
    print "Ctrl-c to quit..."
    try:
        httpd.serve_forever()
    except KeyboardInterrupt: pass
 
if __name__ == "__main__":
    main()
