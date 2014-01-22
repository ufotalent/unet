import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, Response

import threading
import time
import pickle

# create our little application :)
app = Flask(__name__)

app.config.from_object("config");
nodes = {}

def get():
    rootdir = app.config['PATH']
    for s,d,files in os.walk(rootdir):
        return files
    
@app.route('/')
def root():
    data=[]
    for n in get():
        i=None
        p1=p2=None
        if n in nodes:
            i=nodes[n]

        if i!=None and os.path.exists("pings/"+i):
            with open("pings/"+i) as f:
                p1=f.readline()
                p2=f.readline()

        data.append(dict(name=n, ip=i, p1=p1, p2=p2))

    return render_template('index.html', data=data)
        
@app.route('/listuser/<string:name>')
def list_item(name):
    f = open(app.config['PATH']+"/"+name)
    return Response(f.read(), content_type="text/plain;charset=UTF-8");

@app.route('/sync_script')
def sync_script():
    return Response(render_template('sync.sh', names=get(), host=request.host), content_type="text/plain;charset=UTF-8")

@app.route('/add_node', methods=['POST'])
def add_node():
    f = open(app.config['PATH']+"/"+request.form["name"], "w")
    f.write(request.form["content"]+"\n");
    return redirect(url_for('root'))

@app.route('/set_node_ip', methods=['POST'])
def set_node_ip():
    name = request.form['name']
    ip = request.form['ip']
    nodes[name] = ip
    f = open("ip-name", "w");
    for key in nodes:
        f.write(key+" "+nodes[key]+"\n");
    return redirect(url_for('root'))

def get_nodes():
    f = open("ip-name");
    for line in f:
        [name, ip] = line.split()
        nodes[name] = ip


if __name__ == '__main__':
    get_nodes()
    app.run(port=app.config['PORT'], host = app.config['HOST'], debug = app.config['DEBUG'])
