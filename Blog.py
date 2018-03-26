from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from DataBase import *


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/new_post"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><head><meta charset='UTF-8'></head><body>"
                output += "<h1>Micro Blog</h1><h2 id='error' style='color:red;display:none'>Both fields are required</h2>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/new_post'><table><tr><td><label>Title</label></td><td><input id='title' name="Title" type="text"></td></tr><tr><td><label>Message</label></td><td><textarea id='mes' name="Message"> </textarea></td><tr><td><input type="submit" value="Post"></td><tr> </form>'''
                output += '''</body></html>'''
                self.wfile.write(bytes(output,"utf-8"))
                print (output)
                return
            elif self.path.endswith("/show_entries"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                session = Session()
                output = "<html><body><h1>Blog posts</h1>"

                for instance in session.query(User).order_by(User.Timestamp.desc()):
                    print(instance.Title, instance.Message)
                    output += "<div style='margin-bottom:20px;border-style:solid;border-radius:7px;border-color:#73716e;background:#fde9a2;padding:15px;'><h2>"+str(instance.Title)+" posted on "+str(instance.Timestamp)+"</h2>"
                    output += "<p>"+str(instance.Message)+"</p></div>"
                
                output += "</body></html>"
                self.wfile.write(bytes(output,"utf-8"))
                print (output)  
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
        except :
            output = ""
            output += "<html><body>"
            output += "<h1>No blog posts!!!</h1>"
            output += "</body></html>"
            self.wfile.write(bytes(output,"utf-8"))
            print (output)
            return

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                field1 = fields.get('Title')
                field2 = fields.get('Message')
            print(field1+field2)
            output = ""
            
            if str(field1[0],'utf-8') == "" and str(field2[0],'utf-8') == " ":
                print("inside")
                output += "<html><head><meta charset='UTF-8'></head><body>"
                output += "<h1>Micro Blog</h1><h2 id='error' style='color:red;'>Both fields are required</h2>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/new_post'><table><tr><td><label>Title</label></td><td><input id='title' name="Title" type="text"></td></tr><tr><td><label>Message</label></td><td><textarea id='mes' name="Message"> </textarea></td><tr><td><input onsubmit="return validateForm()"  type="submit" value="Post"></td><tr> </form>'''
                output += '''<script>
                                function validateForm()
                                {
                                    if( document.getElementById('mes').value == " " && document.getElementById('title').value == "")
                                    {   
                                        document.getElementByID('error').style.display=block;
                                        return false;
                                    }
                                    else
                                        return true;
                                }
                            </script></body></html>'''
                self.wfile.write(bytes(output,"utf-8"))
            else:
                p=User(str(field1[0],'utf-8'),str(field2[0],'utf-8'))    
                p.insert()
                output = ""
                output += "<html><body>"
                output += "<h2> Post successful...</h2>"            
                output += "<a href='/show_entries'>Show entries</a></body></html>"
                self.wfile.write(bytes(output,"utf-8"))
                print (output)            
        except:
            pass


def main():
    try:
        port = 8043
        server = HTTPServer(('', port), webServerHandler)
        print ("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()
