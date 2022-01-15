import re
import os
import sys
import glob
import time
import json
import pytz
import random
import _thread
import datetime
import grequests
import cloudscraper
#   from requests_html import HTMLSession
from inspect import currentframe as SourceCodeLine
from flask import Flask, json, jsonify, request, redirect, session, send_from_directory, Response, make_response, render_template
import gc

# IMPORT FOR keep_alive
from keep_alive import keep_alive
keep_alive()

# IMPORT FOR PYREPLIT
import typer, requests, zipfile, shutil, logging
import snow_pyrepl as pyrepl

timedate = datetime.datetime
timezone = pytz.timezone

#   requestsHTML = HTMLSession()

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("snow_pyrepl").setLevel(logging.WARNING)
#   logging.getLogger("requests").addHandler(logging.NullHandler())
#   requests_log.propagate = False

app = Flask(
    __name__, 
    static_url_path = '', 
    static_folder   = 'static',
    template_folder = 'templates'
)

__version__ = "1.1.9"

try:
	__sid__ = 's%3AiRnjOZamIqSXYxyaNvTWsL_6gVfI6QeP.%2FnMg%2F6SW3Hz7AnUyRcxNXiYARSCyY%2FVaSIUuLiiO9mc'
except:
	__sid__ = None

app = typer.Typer()



def grequests_except_handler(request, excetion):
    print(f'{ timedate.now() } EXCEPT : HANDLER { request.url }')




def get_json(user, name, sid):
	headers = {
		'Content-Type'      : 'application/json',
		'connect.sid'       : sid,
		'X-Requested-With'  : 'https://replit.com',
		'Origin'            : 'https://replit.com',
        'referer'           : f'https://replit.com/@{ user }/{ name }',
		'User-Agent'        : 'Mozilla/5.0', 
        'Cookie'            : f'connect.sid={ sid }; ',
	}
	cookies = {
		"connect.sid"       : sid
	}
	r = requests.get(
        f"https://replit.com/data/repls/@{ user }/{ name }", 
        headers = headers, 
        cookies = cookies, 
        timeout = 16
    )
	return r.json()['id']

def get_token(user, name, sid):
    r = cloudscraper.create_scraper(
        delay   = 32
    ).get(
        f'https://replit.com/@{ user }/{ name }', 
        headers = {
    		'Content-Type'      : 'application/json',
    		'connect.sid'       : sid,
    		'X-Requested-With'  : 'https://replit.com',
    		'Origin'            : 'https://replit.com',
            'referer'           : f'https://replit.com/@{ user }/{ name }',
            'Cache-Control'     : 'no-cache',
            'Cookie'            : f'connect.sid={ sid }; ',
        },
    	cookies = {
    		'connect.sid'       : sid
    	},
        timeout = 32
    )
    #   print( r )
    #   print( r.content )
    data = json.loads(r.text.split("<script id=\"__NEXT_DATA__\" type=\"application/json\">")[1].split("</script>")[0])['props']['pageProps']['connectionMetadata']
    return data['token'], f"{data['gurl']}/wsv2/{data['token']}"

def chk_token(user, name, sid):
    try:
        r = cloudscraper.create_scraper(
            delay   = 32
        ).get(
            f'https://replit.com/@{ user }/{ name }', 
            headers = {
        		'Content-Type'      : 'application/json',
        		'connect.sid'       : sid,
        		'X-Requested-With'  : 'https://replit.com',
        		'Origin'            : 'https://replit.com',
                'referer'           : f'https://replit.com/@{ user }/{ name }',
                'Cache-Control'     : 'no-cache',
                'Cookie'            : f'connect.sid={ sid }; ',
            },
        	cookies = {
        		'connect.sid'       : sid
        	},
            timeout = 32
        )
        #   print( r )
        #   print( r.content )
        #   data = json.loads(r.text.split("<script id=\"__NEXT_DATA__\" type=\"application/json\">")[1].split("</script>")[0])['props']['pageProps']['connectionMetadata']
        #   return data['token'], f"{data['gurl']}/wsv2/{data['token']}"
        
        #   ren_token(user, name, sid, r.request.headers['User-Agent'])

        print(f'{ timedate.now() } CHECK :: { SourceCodeLine().f_lineno } :: { user } { name } - { r.status_code }')
        return r.status_code
    except:
        print(f'{ timedate.now() } CHECK :: { SourceCodeLine().f_lineno } :: { user } { name } - 503')
        return 503

#   def ren_token(user, name, sid, uag):
#       try:
#           r = requestsHTML.get(
#               f'https://replit.com/@{ user }/{ name }', 
#               headers = {
#           		'Content-Type'      : 'application/json',
#           		'connect.sid'       : sid,
#           		'X-Requested-With'  : 'https://replit.com',
#           		'Origin'            : 'https://replit.com',
#                   'referer'           : f'https://replit.com/@{ user }/{ name }',
#                   'Cache-Control'     : 'no-cache',
#                   'Cookie'            : f'connect.sid={ sid }; ', 
#                   'User-Agent'        : uag
#               },
#           	cookies = {
#           		'connect.sid'       : sid
#           	},
#               timeout = 32
#           )
#           #   print( r )
#           #   print( r.content )
#           #   data = json.loads(r.text.split("<script id=\"__NEXT_DATA__\" type=\"application/json\">")[1].split("</script>")[0])['props']['pageProps']['connectionMetadata']
#           #   return data['token'], f"{data['gurl']}/wsv2/{data['token']}"
#           print(f'{ timedate.now() } PRINT :: { SourceCodeLine().f_lineno } :: { user } { name } - { r.status_code }')
#           return r.status_code
#       except:
#           print(f'{ timedate.now() } PRINT :: { SourceCodeLine().f_lineno } :: { user } { name } - 503')
#           return 503

@app.command(help="Output the current version for Replit CLI")
def version():
	typer.echo(__version__)






class PYREPLIT():
    def __init__(
        self, 
        repl:str, 
        #   code:str
    ):
        
        self.repl = repl
        #   self.code = code
        
    def operation(
        self
    ):
        
        _thread.start_new_thread(self.shell, ())

    def connect(
        self, 
        vals
    ):
        
        while True:

            # GET REPLIT ID
            try:
                if self.id == None:
                        self.id                 = get_json(self.user, self.name, self.key)
            except Exception as e:
                print(f'{ timedate.now() } ERROR :: { SourceCodeLine().f_lineno } :: NOT SHARED REPLIT { self.user } { self.name } { e }')
                time.sleep(4)
                continue
            break
        
        while True:

            # GET REPLIT TOKEN AND URL
            try:
                if self.token == None or self.url == None or random.randrange(100) >= 64:
                    self.token, self.url    = get_token(self.user, self.name, self.key)
                    open(f'{ self.user }_{ self.name }.json', 'w').write(json.dumps({
                            'id'    : self.id,
                            'token' : self.token,
                            'url'   : self.url
                    }, indent = 4))
            except Exception as e:
                self.token      = None
                self.url        = None
                self.client     = None
                self.runner     = None
                print(f'{ timedate.now() } ERROR :: { SourceCodeLine().f_lineno } :: NOT TOKEN REPLIT { self.user } { self.name } { e }')
                time.sleep(4)
                continue
        
            try:
                self.client             = pyrepl.Client(self.token, self.id, self.url)
            except Exception as e:
                self.token      = None
                self.url        = None
                self.client     = None
                self.runner     = None
                print(f'{ timedate.now() } ERROR :: { SourceCodeLine().f_lineno } :: NOT CLIENT REPLIT { self.user } { self.name } - { e }')
                time.sleep(4)
                continue
        
            try:
                self.runner             = self.client.open(vals, '')
            except Exception as e:
                self.token      = None
                self.url        = None
                self.client     = None
                self.runner     = None
                print(f'{ timedate.now() } ERROR :: { SourceCodeLine().f_lineno } :: NOT RUNNER REPLIT { self.user } { self.name } - { e }')
                time.sleep(4)
                continue
            break
        
        
        print( timedate.now(), 'USER  ::::', self.user )
        print( timedate.now(), 'NAME  ::::', self.name )
        print( timedate.now(), 'ID    ::::', self.id )
        print( timedate.now(), 'SOCK  :::: run_', self.runner )
        #   print( 'KEY   ::::', self.key )
        #   print( 'TOKEN ::::', self.token )
        #   print( 'URL   ::::', self.url )
    def shell(
        self
    ):
        
        self.user               = self.repl.split("/")[0]
        self.name               = self.repl.split("/")[1]
        self.key                = __sid__.strip()
        self.token              = None if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['token']
        self.url                = None if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['url']
        self.client             = None
        self.id                 = None if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['id']
        self.runner             = None
        
        self.connect('shellrun2')
        
        while True:
                
            try:
                if random.randrange(100) >= 86:
                    self.output = self.runner.run({
                        'clear':{
                        }
                    }); #   print( self.output )

                    time.sleep(10)

                self.output = self.runner.run({
                    'runMain':{
                    }
                }); #   print( self.output )

                time.sleep(5)

                self.output = self.runner.run({
                    'runMain':{
                    }
                }); #   print( self.output )

                time.sleep(5)

                self.output = self.runner.run({
                    'runMain':{
                    }
                }); #   print( self.output )
                
            except Exception as e:
                print(f'{ timedate.now() } ERROR :: { SourceCodeLine().f_lineno } :: { self.user } { self.name } - { e }')
            
            break

    def kills(
        self
    ):
        
        self.user               = self.repl.split("/")[0]
        self.name               = self.repl.split("/")[1]
        self.key                = __sid__.strip()
        self.token              = None if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['token']
        self.url                = None if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['url']
        self.client             = None
        self.id                 = None if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['id']
        self.runner             = None
        
        self.connect('exec')

        while True:
                
            try:
                
                self.output = self.runner.run({
		            "exec": {
		            	"args": random.choice([['busybox', 'reboot']] + [['kil',  '1']])
		            }
                }); #   print( self.output )
                time.sleep(5)
                
            except Exception as e:
                print(f'{ timedate.now() } ERROR :: { SourceCodeLine().f_lineno } :: { self.user } { self.name } - { e }')
            
            break

    def gits(
        self
    ):
        
        self.user               = self.repl.split("/")[0]
        self.name               = self.repl.split("/")[1]
        self.key                = __sid__.strip()
        self.token              = None if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['token']
        self.url                = None if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['url']
        self.client             = None
        self.id                 = None if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['id']
        self.runner             = None
        
        self.connect('exec')

        while True:
                
            try:
                
                self.output = self.runner.run({
		            "exec": {
		            	"args": [ 'git', 'fetch' '--all' ]
		            }
                }); #   print( self.output )
                time.sleep(5)
                self.output = self.runner.run({
		            "exec": {
		            	"args": [ 'git', 'reset', '--hard' ]
		            }
                }); #   print( self.output )
                time.sleep(5)
                self.output = self.runner.run({
		            "exec": {
		            	"args": [ 'git', 'reset', '--hard', 'origin/master' ]
		            }
                }); #   print( self.output )
                time.sleep(5)
                self.output = self.runner.run({
		            "exec": {
		            	"args": [ 'git', 'stash', 'save', "''" ]
		            }
                }); #   print( self.output )
                time.sleep(5)
                self.output = self.runner.run({
		            "exec": {
		            	"args": [ 'git', 'pull']
		            }
                }); #   print( self.output )
                time.sleep(5)

            except Exception as e:
                print(f'{ timedate.now() } ERROR :: { SourceCodeLine().f_lineno } :: { self.user } { self.name } - { e }')
            
            break

#   git fetch --all; git reset --hard; git reset --hard origin/master; git stash save ''; git pull; 
















class WEBCHECK():
    def __init__(
        self, 
        data = [], 
        mode = 'run'
    ):
        
        self.data = data
        self.mode = mode
        
    def thread(
        self
    ):
        if self.mode == 'run':
            self.thread = _thread.start_new_thread(self.run, ())
        if self.mode == 'chk':
            self.thread = _thread.start_new_thread(self.chk, ())
        if self.mode == 'ace':
            self.thread = _thread.start_new_thread(self.ace, ())
        if self.mode == 'get':
            self.get()
      

    def run(
        self
    ):

        time.sleep(random.uniform(0.11, 5.64))

        #   while True:
        
        self.load = []
        self.resp = []
        self.list = []
        self.gate = []
        self.root = []
        
        for self.base in self.data:
            self.user               = self.base.split("/")[0]
            self.name               = self.base.split("/")[1]
            self.load.append(grequests.get(
                f'https://{ self.name }.{ self.user }.repl.co/login', 
                timeout = 16
            ))
            self.gate.append(f'https://{ self.name }.{ self.user }.repl.co')
            try:
                self.root.append(f'https://{0}.repl.co/login'.format(
                    "" if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['id']
                ))
            except:
                os.remove(f'{ self.user }_{ self.name }.json')
                self.root.append(f'https://{0}.repl.co/login'.format("" ))
            #   self.root                 = 
            #   self.runner             = None
            
        self.resp.append(
            grequests.map(self.load)
        )
        self.resp.append(
            grequests.map(self.load)
        )
        self.resp.append(
            grequests.map(self.load)
        )
        
        for self.aaaa, self.bbbb in enumerate( self.resp ):
            
            self.list.append([])
            
            for self.cccc, self.dddd in enumerate( self.resp[ self.aaaa ] ):
                try:
                    self.list[self.aaaa].append( self.resp[self.aaaa][self.cccc].status_code )
                except:
                    self.list[self.aaaa].append( 502 )
        
        for self.aaaa, self.bbbb in enumerate( self.list ):
            for self.cccc, self.dddd in enumerate( self.list[ self.aaaa ] ):
                
                if (len([
                    self.eeee[ self.cccc ] for self.eeee in self.list if self.eeee[ self.cccc ] == 200
                ]) <= 1 or not ([
                    self.eeee[ self.cccc ] for self.eeee in self.list
                ][-1] == 200)) and not self.gate[self.cccc] == None:
                    
                    self.gate[self.cccc] = None
                    
                    print( f'{ timedate.now() } { self.thread } 503 : {self.cccc:02n}', self.load[self.cccc].url, [
                        self.eeee[ self.cccc ] for self.eeee in self.list
                    ] )
                    
                    PYREPLIT(
                        repl = '/'.join([
                            re.split('/|\.', self.load[self.cccc].url)[3], 
                            re.split('/|\.', self.load[self.cccc].url)[2]
                        ])
                    ).gits()
                    if random.randrange(100) >= 86:
                        PYREPLIT(
                            repl = '/'.join([
                                re.split('/|\.', self.load[self.cccc].url)[3], 
                                re.split('/|\.', self.load[self.cccc].url)[2]
                            ])
                        ).kills()
                    time.sleep(8)
                    #   chk_token(
                    #       re.split('/|\.', self.load[self.cccc].url)[3], 
                    #       re.split('/|\.', self.load[self.cccc].url)[2], 
                    #       __sid__.strip()
                    #   )
                    
                    PYREPLIT(
                        repl = '/'.join([
                            re.split('/|\.', self.load[self.cccc].url)[3], 
                            re.split('/|\.', self.load[self.cccc].url)[2]
                        ])
                    ).shell()
                    
                    try     : 
                        if not self.root[self.cccc] == '':
                            #   _thread.start_new_thread(requests.get(self.root[self.cccc]) , ())
                            _thread.start_new_thread(requests.get(self.load[self.cccc].url.replace('/login', '/__tail'), timeout = 16), ())
                    except  : pass
                    try     : 
                        if not self.root[self.cccc] == '':
                            _thread.start_new_thread(requests.get(f'https://render-tron.appspot.com/screenshot/{ self.root[self.cccc] }', timeout = 16), ())
                    except  : pass

                elif (len([
                    self.eeee[ self.cccc ] for self.eeee in self.list if self.eeee[ self.cccc ] == 200
                ]) >= 1 or ([
                    self.eeee[ self.cccc ] for self.eeee in self.list
                ][-1] == 200)) and not self.gate[self.cccc] == True:
                
                    self.gate[self.cccc] = True
                    

                    print( f'{ timedate.now() } { self.thread } 200 : {self.cccc:02n}', self.load[self.cccc].url )

                    #   if random.randrange(100) >= 50:
                    #       chk_token(
                    #           re.split('/|\.', self.load[self.cccc].url)[3], 
                    #           re.split('/|\.', self.load[self.cccc].url)[2], 
                    #           __sid__.strip()
                    #       )
                    
                    try     : 
                        if not self.root[self.cccc] == '':
                            _thread.start_new_thread(requests.get(self.root[self.cccc], timeout = 16) , ())
                    except  : pass
                    #   try     : 
                    #       if not self.root[self.cccc] == '':
                    #           _thread.start_new_thread(requests.get(f'https://render-tron.appspot.com/screenshot/{ self.root[self.cccc] }'), ())
                    #   except  : pass
                    
                    try     : 
                        if re.search('awcloud-token', self.load[self.cccc].url):
                            _thread.start_new_thread(requests.get(self.load[self.cccc].url.replace('/login', ''), timeout = 16), ())
                        else:
                            _thread.start_new_thread(requests.get(self.load[self.cccc].url.replace('/login', '/run'), timeout = 16), ())
                    except  : pass
                    #   try     : _thread.start_new_thread(requests.post(self.load[self.cccc].url.replace('/login', ''), timeout = 16), ())
                    #   except  : pass
                    #   try     : _thread.start_new_thread(requests.get(f'https://render-tron.appspot.com/screenshot/{ self.load[self.cccc].url.replace("/login", "") }', timeout = 16), ())
                    #   except  : pass
                    
        print('\n'.join([str( f'{ timedate.now() } { self.thread } DONE ' + str(x) ) for x in self.list]))
        #   time.sleep( random.randrange( 80, 160 ) )
    
    
    def get(
        self
    ):

        time.sleep(random.uniform(0.11, 5.64))

        #   while True:
        
        self.load = []
        self.resp = []
        self.list = []
        self.gate = []
        self.root = []
        
        for self.base in self.data:
            self.user               = self.base.split("/")[0]
            self.name               = self.base.split("/")[1]
            self.load.append(grequests.get(
                f'https://{ self.name }.{ self.user }.repl.co', 
                timeout = 16
            ))
            self.gate.append(f'https://{ self.name }.{ self.user }.repl.co')
            try:
                self.root.append(f'https://{0}.repl.co'.format(
                    "" if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['id']
                ))
            except:
                os.remove(f'{ self.user }_{ self.name }.json')
                self.root.append(f'https://{0}.repl.co'.format("" ))
            #   self.root                 = 
            #   self.runner             = None
            
        self.resp.append(
            grequests.map(self.load)
        )
        self.resp.append(
            grequests.map(self.load)
        )
        self.resp.append(
            grequests.map(self.load)
        )
        for self.aaaa, self.bbbb in enumerate( self.resp ):
            
            self.list.append([])
            
            for self.cccc, self.dddd in enumerate( self.resp[ self.aaaa ] ):
                try:
                    self.list[self.aaaa].append( self.resp[self.aaaa][self.cccc].status_code )
                except:
                    self.list[self.aaaa].append( 502 )
        
        for self.aaaa, self.bbbb in enumerate( self.list ):
            for self.cccc, self.dddd in enumerate( self.list[ self.aaaa ] ):
                
                if (len([
                    self.eeee[ self.cccc ] for self.eeee in self.list if self.eeee[ self.cccc ] == 200
                ]) <= 1 or not ([
                    self.eeee[ self.cccc ] for self.eeee in self.list
                ][-1] == 200)) and not self.gate[self.cccc] == None:
                    
                    self.gate[self.cccc] = None
                    
                    print( f'{ timedate.now() } 503 : {self.cccc:02n}', self.load[self.cccc].url, [
                        self.eeee[ self.cccc ] for self.eeee in self.list
                    ] )
                    
                    #   PYREPLIT(
                    #       repl = '/'.join([
                    #           re.split('/|\.', self.load[self.cccc].url)[3], 
                    #           re.split('/|\.', self.load[self.cccc].url)[2]
                    #       ])
                    #   ).gits()
                    if random.randrange(100) >= 86:
                        PYREPLIT(
                            repl = '/'.join([
                                re.split('/|\.', self.load[self.cccc].url)[3], 
                                re.split('/|\.', self.load[self.cccc].url)[2]
                            ])
                        ).kills()
                    time.sleep(8)
                    #   chk_token(
                    #       re.split('/|\.', self.load[self.cccc].url)[3], 
                    #       re.split('/|\.', self.load[self.cccc].url)[2], 
                    #       __sid__.strip()
                    #   )
                    
                    PYREPLIT(
                        repl = '/'.join([
                            re.split('/|\.', self.load[self.cccc].url)[3], 
                            re.split('/|\.', self.load[self.cccc].url)[2]
                        ])
                    ).shell()
                    
                    #   try     : 
                    #       if not self.root[self.cccc] == '':
                    #           #   _thread.start_new_thread(requests.get(self.root[self.cccc]) , ())
                    #           _thread.start_new_thread(requests.get(f'{ self.load[self.cccc].url }/__tail', timeout = 16), ())
                    #   except  : pass
                    #   try     : 
                    #       if not self.root[self.cccc] == '':
                    #           _thread.start_new_thread(requests.get(f'https://render-tron.appspot.com/screenshot/{ self.root[self.cccc] }', timeout = 16), ())
                    #   except  : pass

                elif (len([
                    self.eeee[ self.cccc ] for self.eeee in self.list if self.eeee[ self.cccc ] == 200
                ]) >= 1 or ([
                    self.eeee[ self.cccc ] for self.eeee in self.list
                ][-1] == 200)) and not self.gate[self.cccc] == True:
                
                    self.gate[self.cccc] = True
                    
                    print( f'{ timedate.now() } 200 : {self.cccc:02n}', self.load[self.cccc].url )

                    #   if random.randrange(100) >= 50:
                    #       chk_token(
                    #           re.split('/|\.', self.load[self.cccc].url)[3], 
                    #           re.split('/|\.', self.load[self.cccc].url)[2], 
                    #           __sid__.strip()
                    #       )
                    
                    #   try     : 
                    #       if not self.root[self.cccc] == '':
                    #           _thread.start_new_thread(requests.get(self.root[self.cccc], timeout = 16) , ())
                    #   except  : pass
                    #   try     : 
                    #       if not self.root[self.cccc] == '':
                    #           _thread.start_new_thread(requests.get(f'https://render-tron.appspot.com/screenshot/{ self.root[self.cccc] }'), ())
                    #   except  : pass
                    
                    #   try     : 
                    #       
                    #       _thread.start_new_thread(requests.get(f'{ self.load[self.cccc].url }/__tail', timeout = 16), ())
                    #   except  : pass
                    #   try     : _thread.start_new_thread(requests.post(self.load[self.cccc].url.replace('/login', ''), timeout = 16), ())
                    #   except  : pass
                    #   try     : _thread.start_new_thread(requests.get(f'https://render-tron.appspot.com/screenshot/{ self.load[self.cccc].url.replace("/login", "") }', timeout = 16), ())
                    #   except  : pass
                    
        print('\n'.join([str( f'{ timedate.now() } DONE ' + str(x) ) for x in self.list]))
        #   time.sleep( random.randrange( 80, 160 ) )
        
        
    def chk(
        self
    ):

        time.sleep(random.uniform(0.11, 5.64))
        
        while True:

            self.load = []
            self.resp = []
            self.list = []
            self.gate = []
            self.root = []

            for self.base in self.data:
                self.user               = self.base.split("/")[0]
                self.name               = self.base.split("/")[1]
                self.load.append(grequests.get(
                    f'https://{ self.name }.{ self.user }.repl.co', 
                    timeout = 12
                ))
                self.gate.append(f'https://{ self.name }.{ self.user }.repl.co')
                try:
                    self.root.append(f'https://{0}.repl.co'.format(
                        "" if not os.path.isfile( f'{ self.user }_{ self.name }.json' ) else json.load(open( f'{ self.user }_{ self.name }.json' ))['id']
                    ))
                except:
                    os.remove(f'{ self.user }_{ self.name }.json')
                    self.root.append(f'https://{0}.repl.co'.format(""))
                #   self.root                 = 
                #   self.runner             = None

            self.resp.append(
                grequests.map(self.load)
            )
            self.resp.append(
                grequests.map(self.load)
            )
            self.resp.append(
                grequests.map(self.load)
            )

            for self.aaaa, self.bbbb in enumerate( self.resp ):

                self.list.append([])

                for self.cccc, self.dddd in enumerate( self.resp[ self.aaaa ] ):
                    try:
                        self.list[self.aaaa].append( self.resp[self.aaaa][self.cccc].status_code )
                    except:
                        self.list[self.aaaa].append( 502 )

            for self.aaaa, self.bbbb in enumerate( self.list ):
                for self.cccc, self.dddd in enumerate( self.list[ self.aaaa ] ):

                    if (len([
                        self.eeee[ self.cccc ] for self.eeee in self.list if self.eeee[ self.cccc ] == 200
                    ]) <= 1 or not ([
                        self.eeee[ self.cccc ] for self.eeee in self.list
                    ][-1] == 200)) and not self.gate[self.cccc] == None:

                        self.gate[self.cccc] = None

                        print( f'{ timedate.now() } { self.thread } 503 : {self.cccc:02n}', self.load[self.cccc].url, [
                            self.eeee[ self.cccc ] for self.eeee in self.list
                        ] )

                        if random.randrange(100) >= 86:
                            PYREPLIT(
                                repl = '/'.join([
                                    re.split('/|\.', self.load[self.cccc].url)[3], 
                                    re.split('/|\.', self.load[self.cccc].url)[2]
                                ])
                            ).kills()
                            time.sleep(8)
                        #   if random.randrange(100) >= 16:
                        #       chk_token(
                        #           re.split('/|\.', self.load[self.cccc].url)[3], 
                        #           re.split('/|\.', self.load[self.cccc].url)[2], 
                        #           __sid__.strip()
                        #       )

                        PYREPLIT(
                            repl = '/'.join([
                                re.split('/|\.', self.load[self.cccc].url)[3], 
                                re.split('/|\.', self.load[self.cccc].url)[2]
                            ])
                        ).shell()

                        try     : 
                            if not self.root[self.cccc] == '':
                                #   _thread.start_new_thread(requests.get(self.root[self.cccc]) , ())
                                _thread.start_new_thread(requests.get(f'{ self.load[self.cccc] }/__tai',  timeout = 16), ())
                        except  : pass
                        try     : 
                            if not self.root[self.cccc] == '':
                                _thread.start_new_thread(requests.get(f'https://render-tron.appspot.com/screenshot/{ self.root[self.cccc] }', timeout = 16), ())
                        except  : pass

                    elif (len([
                        self.eeee[ self.cccc ] for self.eeee in self.list if self.eeee[ self.cccc ] == 200
                    ]) >= 1 or ([
                        self.eeee[ self.cccc ] for self.eeee in self.list
                    ][-1] == 200)) and not self.gate[self.cccc] == True:

                        self.gate[self.cccc] = True


                        print( f'{ timedate.now() } { self.thread } 200 : {self.cccc:02n}', self.load[self.cccc].url )

                        #   if random.randrange(100) >= 50:
                        #       chk_token(
                        #           re.split('/|\.', self.load[self.cccc].url)[3], 
                        #           re.split('/|\.', self.load[self.cccc].url)[2], 
                        #           __sid__.strip()
                        #       )

                        #   try     : _thread.start_new_thread(requests.post(self.load[self.cccc].url), ())
                        #   except  : pass
                        try     : _thread.start_new_thread(requests.get(f'https://render-tron.appspot.com/screenshot/{ self.load[self.cccc].url }', timeout = 16), ())
                        except  : pass

            print('\n'.join([str( f'{ timedate.now() } { self.thread } DONE ' + str(x) ) for x in self.list]))
            time.sleep( random.randrange( 10, 60 ) )

    def ace(
        self
    ):
        
        time.sleep(random.uniform(0.11, 5.64))
        
        while True:

            self.load = []
            self.resp = []
            self.list = []
            self.gate = []

            for self.base in self.data:
                self.addr               = self.base
                self.load.append(grequests.get(
                    f'{ self.addr }', 
                    headers = {
                        'User-Agent'        : random.choice([
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 slurp', 
                            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 
                            'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.5277.764 Mobile Safari/537.36'
                        ]), 
                        'Accept'            : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 
                        'Accept-Language'   : 'en-US,en;q=0.9'
                    }, 
                    timeout = 20
                ))
                self.gate.append(f'{ self.addr }')

            self.resp.append(
                grequests.map(self.load)
            )
            self.resp.append(
                grequests.map(self.load)
            )
            self.resp.append(
                grequests.map(self.load)
            )

            for self.aaaa, self.bbbb in enumerate( self.resp ):

                self.list.append([])

                for self.cccc, self.dddd in enumerate( self.resp[ self.aaaa ] ):
                    try:
                        self.list[self.aaaa].append( self.resp[self.aaaa][self.cccc].status_code )
                    except:
                        self.list[self.aaaa].append( 502 )

            for self.aaaa, self.bbbb in enumerate( self.list ):
                for self.cccc, self.dddd in enumerate( self.list[ self.aaaa ] ):

                    if (len([
                        self.eeee[ self.cccc ] for self.eeee in self.list if self.eeee[ self.cccc ] == 200
                    ]) <= 1 or not ([
                        self.eeee[ self.cccc ] for self.eeee in self.list
                    ][-1] == 200)) and not self.gate[self.cccc] == None:

                        self.gate[self.cccc] = None

                        print( f'{ timedate.now() } { self.thread } 503 : {self.cccc:02n}', self.load[self.cccc].url, [
                            self.eeee[ self.cccc ] for self.eeee in self.list
                        ] )

                        for count in range(0, 6):
                            try         :
                                _thread.start_new_thread(requests.get(f'https://render-tron.appspot.com/screenshot/{ self.load[self.cccc].url }', timeout = 16), ())
                            except      :
                                pass
                            time.sleep( random.randrange(8) )

                    elif (len([
                        self.eeee[ self.cccc ] for self.eeee in self.list if self.eeee[ self.cccc ] == 200
                    ]) >= 1 or ([
                        self.eeee[ self.cccc ] for self.eeee in self.list
                    ][-1] == 200)) and not self.gate[self.cccc] == True:

                        self.gate[self.cccc] = True

                        print( f'{ timedate.now() } { self.thread } 200 : {self.cccc:02n}', self.load[self.cccc].url )

                        if random.randrange(100) >= 64:
                            try     :
                                _thread.start_new_thread(requests.get(f'https://render-tron.appspot.com/screenshot/{ self.load[self.cccc].url }', timeout = 16), ())
                            except  :
                                pass

            print('\n'.join([str( f'{ timedate.now() } { self.thread } DONE ' + str(x) ) for x in self.list]))
            time.sleep( random.randrange(120) )


while True:
    i = []
    for x in [
        #    'PatiwatNumbut/awcloud-data-patiwatnumbut-',
        #    'PatiwatNumbut/awcloud-data-FFPREMIUM',
        #    'PatiwatNumbut/awcloud-data-00001FFPREMIUM',
        #    'PatiwatNumbut/awcloud-data-00002FFPREMIUM',
        #    'PatiwatNumbut/awcloud-data-00003FFPREMIUM',
        #-   'PatiwatNumbut/awcloud-data-00001artwisut', 
        #-   'PatiwatNumbut/awcloud-data-00002artwisut', 
        #-   'PatiwatNumbut/awcloud-data-sakchaipingsran', 
        #-   'PatiwatNumbut/awcloud-data-00001sakchaipingsran', 
        #-   'PatiwatNumbut/awcloud-data-00002sakchaipingsran', 
        #-   'PatiwatNumbut/awcloud-data-00003sakchaipingsran', 
        #-   'PatiwatNumbut/awcloud-data-lifferty', 
        #-   'PatiwatNumbut/awcloud-data-00001lifferty', 
        'PatiwatNumbut/awcloud-data-Praniti99', 
        'PatiwatNumbut/awcloud-data-00001Praniti99', 
        'PatiwatNumbut/awcloud-data-00002Praniti99', 
        'PatiwatNumbut/awcloud-data-00003Praniti99', 
        #-   'PatiwatNumbut/awcloud-data-fourz', 
        #-   'PatiwatNumbut/awcloud-data-jo1232', 
        #-   'PatiwatNumbut/awcloud-data-00001jo1232', 
        #-   'PatiwatNumbut/awcloud-data-boomswxx945', 
        'PatiwatNumbut/awcloud-data-kuk1990', 
        'PatiwatNumbut/awcloud-data-00001kuk1990', 
        'PatiwatNumbut/awcloud-data-00002kuk1990', 
        'PatiwatNumbut/awcloud-data-00003kuk1990', 
        'PatiwatNumbut/awcloud-data-fluffy1004', 
        'PatiwatNumbut/awcloud-data-00001fluffy1004', 
        'PatiwatNumbut/awcloud-data-00002fluffy1004', 
        'PatiwatNumbut/awcloud-data-mikemaesod', 
        'PatiwatNumbut/awcloud-data-00001mikemaesod', 
        'PatiwatNumbut/awcloud-data-00002mikemaesod', 
        'PatiwatNumbut/awcloud-data-00003mikemaesod',
        #-   'PatiwatNumbut/awcloud-data-tee51551',  
        'PatiwatNumbut/awcloud-data-Thanachai12',  
        #-   'PatiwatNumbut/awcloud-data-supernop',  
        #-   'PatiwatNumbut/awcloud-data-aorsai5',  
        #-   'PatiwatNumbut/awcloud-data-00001aorsai5', 
        #-   'PatiwatNumbut/awcloud-data-00002aorsai5', 
        #-   'PatiwatNumbut/awcloud-data-00003aorsai5', 
        #-   'PatiwatNumbut/awcloud-data-najabangaras',  
        #-   'PatiwatNumbut/awcloud-data-bowonratkitisak',  
        #-   'PatiwatNumbut/awcloud-data-akepordee',  
        #-   'PatiwatNumbut/awcloud-data-songeiei1',  
        'PatiwatNumbut/awcloud-data-nunkh0ng',  
        #-   'PatiwatNumbut/awcloud-data-golfgappz',  
        #-   'PatiwatNumbut/awcloud-data-00001golfgappz', 
        #-   'PatiwatNumbut/awcloud-data-la12va',  
        #-   'PatiwatNumbut/awcloud-data-la12va-00001', 
        #-   'PatiwatNumbut/awcloud-data-khowglong2',  
        #-   'PatiwatNumbut/awcloud-data-00001khowglong2', 
        #-   'PatiwatNumbut/awcloud-data-awjate',  
        #-   'PatiwatNumbut/awcloud-data-starshiprs',  
        #-   'PatiwatNumbut/awcloud-data-man88',  
        #-   'PatiwatNumbut/awcloud-data-dhongerus',  
        #-   'PatiwatNumbut/awcloud-data-awduchbot1',  
        #-   'PatiwatNumbut/awcloud-data-00001awduchbot1', 
        'PatiwatNumbut/awcloud-data-aongseal',  
        'PatiwatNumbut/awcloud-data-00001aongseal', 
        #-   'PatiwatNumbut/awcloud-data-catsince',  
        #-   'PatiwatNumbut/awcloud-data-00001catsince', 
        #-   'PatiwatNumbut/awcloud-data-00002catsince', 
        #-   'PatiwatNumbut/awcloud-data-e25icl',  
        #-   'PatiwatNumbut/awcloud-data-tongatipbk',  
        'PatiwatNumbut/awcloud-data-micvbn',  
        #-   'PatiwatNumbut/awcloud-data-domminic11',  
        #-   'PatiwatNumbut/awcloud-data-onibrku10',  
        #-   'PatiwatNumbut/awcloud-data-aphichai123',  
        'PatiwatNumbut/awcloud-data-aengkung1234',  
        'PatiwatNumbut/awcloud-data-00001aengkung1234', 
        'PatiwatNumbut/awcloud-data-00002aengkung1234', 
        'PatiwatNumbut/awcloud-data-00003aengkung1234', 
        #-   'PatiwatNumbut/awcloud-data-ae9041a',  
        #-   'PatiwatNumbut/awcloud-data-mustaza300',  
        'PatiwatNumbut/awcloud-data-yaizaq',  
        'PatiwatNumbut/awcloud-data-00001yaizaq', 
        #-   'PatiwatNumbut/awcloud-data-pppeach',  
        #-   'PatiwatNumbut/awcloud-data-thanaphol2123',  
        'PatiwatNumbut/awcloud-data-soongusto',  
        'PatiwatNumbut/awcloud-data-appleblue1',  
        'PatiwatNumbut/awcloud-data-teeraporn12519',  
        'PatiwatNumbut/awcloud-data-jakkarinninpan',  
        #-  'PatiwatNumbut/awcloud-data-kolokden01',  
        #-  'PatiwatNumbut/awcloud-data-00001kolokden01', 
        'PatiwatNumbut/awcloud-data-pattarasakphuan',  
        'PatiwatNumbut/awcloud-data-00001pattarasakphuan', 
        'PatiwatNumbut/awcloud-data-00002pattarasakphuan', 
        'PatiwatNumbut/awcloud-data-00003pattarasakphuan', 
        #-   'PatiwatNumbut/awcloud-data-idspoon',  
        #-   'PatiwatNumbut/awcloud-data-maxnoizas',  
        'PatiwatNumbut/awcloud-data-biskittlm',  
        'PatiwatNumbut/awcloud-data-00001biskittlm', 
        'PatiwatNumbut/awcloud-data-00002biskittlm', 
        'PatiwatNumbut/awcloud-data-00003biskittlm', 
        'PatiwatNumbut/awcloud-data-joetk074',  
        #-   'PatiwatNumbut/awcloud-data-wealthme01',  
        #-   'PatiwatNumbut/awcloud-data-bb4747',  
        'PatiwatNumbut/awcloud-data-pond37611',  
        'PatiwatNumbut/awcloud-data-trananhquan',  
        'PatiwatNumbut/awcloud-data-00001trananhquan', 
        'PatiwatNumbut/awcloud-data-00002trananhquan', 
        'PatiwatNumbut/awcloud-data-00003trananhquan', 
        #-   'PatiwatNumbut/awcloud-data-pongtanaanon789',  
        #-   'PatiwatNumbut/awcloud-data-00001pongtanaanon789', 
        #-   'PatiwatNumbut/awcloud-data-00002pongtanaanon789', 
        #-   'PatiwatNumbut/awcloud-data-mostok002',  
        'PatiwatNumbut/awcloud-data-TranAnhQuan0001',  
        'PatiwatNumbut/awcloud-data-00001TranAnhQuan0001', 
        'PatiwatNumbut/awcloud-data-00002TranAnhQuan0001', 
        'PatiwatNumbut/awcloud-data-00003TranAnhQuan0001', 
        'PatiwatNumbut/awcloud-data-TranAnhQuan0002',  
        'PatiwatNumbut/awcloud-data-00001TranAnhQuan0002', 
        'PatiwatNumbut/awcloud-data-00002TranAnhQuan0002', 
        'PatiwatNumbut/awcloud-data-00003TranAnhQuan0002', 
        'PatiwatNumbut/awcloud-data-TranAnhQuan0003',  
        'PatiwatNumbut/awcloud-data-00001TranAnhQuan0003', 
        'PatiwatNumbut/awcloud-data-00002TranAnhQuan0003', 
        'PatiwatNumbut/awcloud-data-00003TranAnhQuan0003', 
        'PatiwatNumbut/awcloud-data-sg3000',  
        'PatiwatNumbut/awcloud-data-00001sg3000', 
        'PatiwatNumbut/awcloud-data-00002sg3000', 
        'PatiwatNumbut/awcloud-data-00003sg3000', 
        #-  'PatiwatNumbut/awcloud-data-alienbot15',  
        #-  'PatiwatNumbut/awcloud-data-bas120741',  
        #-  'PatiwatNumbut/awcloud-data-replitbotaw01',  
        #-  'PatiwatNumbut/awcloud-data-awcloud-cpanel00001.replitbotaw01', 
        #-  'PatiwatNumbut/awcloud-data-awcloud-cpanel00002.replitbotaw01', 
        #-  'PatiwatNumbut/awcloud-data-awcloud-cpanel00003.replitbotaw01', 
        #-  'PatiwatNumbut/awcloud-data-replitbotaw02', 
        #-  'PatiwatNumbut/awcloud-data-awcloud-cpanel00001.replitbotaw02', 
        #-  'PatiwatNumbut/awcloud-data-awcloud-cpanel00002.replitbotaw02', 
        #-  'PatiwatNumbut/awcloud-data-awcloud-cpanel00003.replitbotaw02', 
        #-  'PatiwatNumbut/awcloud-data-replitbotaw03', 
        #-  'PatiwatNumbut/awcloud-data-awcloud-cpanel00001.replitbotaw03', 
        #-  'PatiwatNumbut/awcloud-data-rovesea',  
        'PatiwatNumbut/awcloud-data-phillipbansilis',  
        'PatiwatNumbut/awcloud-data-00001phillipbansilis', 
        'PatiwatNumbut/awcloud-data-00002phillipbansilis', 
        'PatiwatNumbut/awcloud-data-00003phillipbansilis', 
        'PatiwatNumbut/awcloud-data-PhillipBan00001',  
        'PatiwatNumbut/awcloud-data-00001PhillipBan00001', 
        'PatiwatNumbut/awcloud-data-00002PhillipBan00001', 
        'PatiwatNumbut/awcloud-data-00003PhillipBan00001', 
        'PatiwatNumbut/awcloud-data-PhillipBan00002',  
        'PatiwatNumbut/awcloud-data-00001PhillipBan00002', 
        'PatiwatNumbut/awcloud-data-00002PhillipBan00002', 
        'PatiwatNumbut/awcloud-data-00003PhillipBan00002', 
        #-  'PatiwatNumbut/awcloud-data-itinba',  
        #-  'PatiwatNumbut/awcloud-data-00001itinba', 
        #-  'PatiwatNumbut/awcloud-data-onemanstory',  
        #-  'PatiwatNumbut/awcloud-data-00001onemanstory', 
        #-  'PatiwatNumbut/awcloud-data-00002onemanstory', 
        #-  'PatiwatNumbut/awcloud-data-apolloart16',  
        'PatiwatNumbut/awcloud-data-areeyagamefi',  
        'PatiwatNumbut/awcloud-data-00001areeyagamefi', 
        'PatiwatNumbut/awcloud-data-00002areeyagamefi', 
        'PatiwatNumbut/awcloud-data-00003areeyagamefi', 
        'PatiwatNumbut/awcloud-data-ninjauk13',  
        'PatiwatNumbut/awcloud-data-00001ninjauk13', 
        #-  'PatiwatNumbut/awcloud-data-sodomkk',  
        #-  'PatiwatNumbut/awcloud-data-fireworkiz',  
        #-  'PatiwatNumbut/awcloud-data-warapon1',  
        #-  'PatiwatNumbut/awcloud-data-00001warapon1', 
        #-  'PatiwatNumbut/awcloud-data-ohhwirat',  
        #-  'PatiwatNumbut/awcloud-data-00001ohhwirat', 
        #-  'PatiwatNumbut/awcloud-data-oliengshop757',  
        'PatiwatNumbut/awcloud-data-maxmagod', 
        'PatiwatNumbut/awcloud-data-00001maxmagod', 
        'PatiwatNumbut/awcloud-data-00002maxmagod', 
        #-  'PatiwatNumbut/awcloud-data-maii15',  
        #-  'PatiwatNumbut/awcloud-data-00001maii15',  
        #-  'PatiwatNumbut/awcloud-data-00002maii15',  
        #-  'PatiwatNumbut/awcloud-data-noom1',  
        #-  'PatiwatNumbut/awcloud-data-00001noom1', 
        #-  'PatiwatNumbut/awcloud-data-00002noom1', 
        #-  'PatiwatNumbut/awcloud-data-00003noom1', 
        #-  'PatiwatNumbut/awcloud-data-pixx2020',  
        #-  'PatiwatNumbut/awcloud-data-00001pixx2020', 
        #-  'PatiwatNumbut/awcloud-data-mafiazarr',  
        #-  'PatiwatNumbut/awcloud-data-00001mafiazarr',  
        #-  'PatiwatNumbut/awcloud-data-00002mafiazarr',  
        'PatiwatNumbut/awcloud-data-raicyberteam',  
        'PatiwatNumbut/awcloud-data-00001raicyberteam', 
        'PatiwatNumbut/awcloud-data-00002raicyberteam', 
        'PatiwatNumbut/awcloud-data-00003raicyberteam', 
        'PatiwatNumbut/awcloud-data-oak2323',  
        'PatiwatNumbut/awcloud-data-poomminerz',  
        'PatiwatNumbut/awcloud-data-00001poomminerz', 
        'PatiwatNumbut/awcloud-data-00002poomminerz', 
        #-  'PatiwatNumbut/awcloud-data-Bankenstein',  
        'PatiwatNumbut/awcloud-data-areeyagamefi2',  
        'PatiwatNumbut/awcloud-data-00001areeyagamefi2', 
        'PatiwatNumbut/awcloud-data-00002areeyagamefi2', 
        'PatiwatNumbut/awcloud-data-00003areeyagamefi2', 
        #-  'PatiwatNumbut/awcloud-data-freddy007',  
        #-  'PatiwatNumbut/awcloud-data-alderman08',  
        #-  'PatiwatNumbut/awcloud-data-awdvii3636',  
        #-  'PatiwatNumbut/awcloud-data-00001awdvii3636', 
        #-  'PatiwatNumbut/awcloud-data-00002awdvii3636', 
        #-  'PatiwatNumbut/awcloud-data-00003awdvii3636', 
        #-  'PatiwatNumbut/awcloud-data-poopui1234',  
        #-  'PatiwatNumbut/awcloud-data-00001poopui1234', 
        #-  'PatiwatNumbut/awcloud-data-00002poopui1234', 
        #-  'PatiwatNumbut/awcloud-data-00003poopui1234', 
        #-  'PatiwatNumbut/awcloud-data-awboat5656',  
        #-  'PatiwatNumbut/awcloud-data-00001awboat5656', 
        #-  'PatiwatNumbut/awcloud-data-00002awboat5656', 
        #-  'PatiwatNumbut/awcloud-data-00003awboat5656', 
        #-  'PatiwatNumbut/awcloud-data-awboat6565',  
        #-  'PatiwatNumbut/awcloud-data-00001awboat6565', 
        #-  'PatiwatNumbut/awcloud-data-00002awboat6565', 
        #-  'PatiwatNumbut/awcloud-data-00003awboat6565', 
        #-  'PatiwatNumbut/awcloud-data-awbpn5454',  
        #-  'PatiwatNumbut/awcloud-data-00001awbpn5454', 
        #-  'PatiwatNumbut/awcloud-data-00002awbpn5454', 
        #-  'PatiwatNumbut/awcloud-data-00003awbpn5454', 
        #-  'PatiwatNumbut/awcloud-data-awbpn4545',  
        #-  'PatiwatNumbut/awcloud-data-00001awbpn4545', 
        #-  'PatiwatNumbut/awcloud-data-00002awbpn4545', 
        #-  'PatiwatNumbut/awcloud-data-00003awbpn4545', 
        #-  'PatiwatNumbut/awcloud-data-awall6363',  
        #-  'PatiwatNumbut/awcloud-data-00001awall6363', 
        #-  'PatiwatNumbut/awcloud-data-00002awall6363', 
        #-  'PatiwatNumbut/awcloud-data-00003awall6363', 
        'PatiwatNumbut/awcloud-data-saksitbot',  
        #-  'PatiwatNumbut/awcloud-data-spints34',  
        #-  'PatiwatNumbut/awcloud-data-thekidkudo',  
        'PatiwatNumbut/awcloud-data-sometimex21',  
        'PatiwatNumbut/awcloud-data-00001sometimex21',  
        #-  'PatiwatNumbut/awcloud-data-zekisz1150',  
        #-  'PatiwatNumbut/awcloud-data-janghyuk789563',  
        'PatiwatNumbut/awcloud-data-Alentine',  
        #-  'PatiwatNumbut/awcloud-data-MOGTH001',  
        #-  'PatiwatNumbut/awcloud-data-waritza',  
        'PatiwatNumbut/awcloud-data-nanthakawut191',  
        'PatiwatNumbut/awcloud-data-00001nanthakawut191', 
        #-  'PatiwatNumbut/awcloud-data-werayutphonyut',  
        #-  'PatiwatNumbut/awcloud-data-rachan7428',  
        'PatiwatNumbut/awcloud-data-sophonnjk',  
        #-  'PatiwatNumbut/awcloud-data-Mazajan2011',  
        'PatiwatNumbut/awcloud-data-jakkapongw',  
        #   'PatiwatNumbut/awcloud-data-sinlapa',  
        'PatiwatNumbut/awcloud-data-zenith009',   
        'PatiwatNumbut/awcloud-data-rainbowz7',  
        'PatiwatNumbut/awcloud-data-00001rainbowz7', 
        'PatiwatNumbut/awcloud-data-00002rainbowz7', 
        'PatiwatNumbut/awcloud-data-00003rainbowz7', 
        #-  'PatiwatNumbut/awcloud-data-c1193',  
        #-  'PatiwatNumbut/awcloud-data-sinkidlukyim5',  
        #-  'PatiwatNumbut/awcloud-data-00001sinkidlukyim5', 
        #-  'PatiwatNumbut/awcloud-data-00002sinkidlukyim5', 
        #-  'PatiwatNumbut/awcloud-data-00003sinkidlukyim5', 
        'PatiwatNumbut/awcloud-data-alosimbay',  
        'PatiwatNumbut/awcloud-data-ArmTheeranai',  
        'PatiwatNumbut/awcloud-data-maxim522th',  
        'PatiwatNumbut/awcloud-data-imoyoyo',  
        'PatiwatNumbut/awcloud-data-djnusr001',  
        'PatiwatNumbut/awcloud-data-aum833',  
        'PatiwatNumbut/awcloud-data-00001aum833', 
        'PatiwatNumbut/awcloud-data-codeduck7210',  
        'PatiwatNumbut/awcloud-data-00001codeduck7210', 
        'PatiwatNumbut/awcloud-data-sodamint1z',  
        'PatiwatNumbut/awcloud-data-00001sodamint1z', 
        'PatiwatNumbut/awcloud-data-maxwalker123',  
        #-  'PatiwatNumbut/awcloud-data-00001maxwalker123', 
        #-  'PatiwatNumbut/awcloud-data-00002maxwalker123', 
        #-  'PatiwatNumbut/awcloud-data-00003maxwalker123', 
        #-  'PatiwatNumbut/awcloud-data-maxwalker543',  
        'PatiwatNumbut/awcloud-data-khunote', 
        'PatiwatNumbut/awcloud-data-00001khunote', 
        'PatiwatNumbut/awcloud-data-00002khunote', 
        'PatiwatNumbut/awcloud-data-00003khunote', 
    ]:
        i.append(x)
        if len(i) >= 10:
            #   time.sleep(random.uniform(0.11, 0.64))
            WEBCHECK(i, mode = 'get').thread()
            time.sleep( random.randrange( 1, 2 ) )
            i = []

    if len(i) >= 1:
        WEBCHECK(i, mode = 'get').thread()
        time.sleep( random.randrange( 1, 2 ) )
        i = []
    else:
        i = []

    time.sleep( 10 )

    continue