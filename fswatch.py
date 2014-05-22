"""
fswatch.py
Marcus Kazmierczak, marcus@mkaz.com
http://github.com/mkaz/fswatch/

This script will watch a local directory using and on change will 
sync to a remote directory. The script can be easily modified to 
do whatever you want on a change event.

requires: pip install watchdog
    
"""

import os, os.path, datetime, time
import ConfigParser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# config parameters
local_path = ""
remote_host = ""
remote_path = ""

# list of files to ignore, simple substring match
ignore_list = ['.svn', '.DS_Store', '.git']


def load_config():
    global local_path, remote_host, remote_path
    configParser = ConfigParser.RawConfigParser()   
    configFilePath = "./fswatch.conf"
    if not os.path.isfile(configFilePath):
        print("Config file fswatch.conf not found")
        os.exit(1)

    configParser.read(configFilePath)
    local_path  = configParser.get('local', 'path')
    remote_host = configParser.get('remote', 'server')    
    remote_path = configParser.get('remote', 'path')

        
def display(str):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print( "[{0}] {1} \n".format(now, str) )


# handles sync event actions, only modified 
class MySyncHandler(FileSystemEventHandler):

    def on_modified(self, event):
        global local_path, remote_host, remote_path
        filename = event.src_path
        remote_file = filename.replace(local_path, '')  # switch local path to remote
        for ig in ignore_list:                          # check ignore list
            if ig in filename:
                return

        # basic rsync to remote server
        cmd = " rsync -cazq --del %s %s:%s%s " % (filename, remote_host, remote_path, remote_file)
        display("Syncing %s " % filename)
        os.system(cmd)


## main loop
def main():
    global local_path, remote_host, remote_path
    load_config();

    observer = Observer()
    observer.schedule(MySyncHandler(), ".", recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
