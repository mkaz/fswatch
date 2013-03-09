#!/usr/bin/env python

"""
fswatch.py
Marcus Kazmierczak, marcus@mkaz.com
http://github.com/mkaz/fswatch/

This script will watch a local directory using Mac OS X FSEvents
and on change will sync to a remote directory. The script can be
easily modified to do whatever you want on a change event.

requires: pip install fsevents

Note: if you are running against a large directory, it will 
take awhile at the beginning, my hunch is it needs to traverse
all sub-directories and attach the listeners everywhere

TODO:
  * switch to daemon-mode
  * add catch-up mode, in case weren't running it
  * fix hanging sometimes on quit
    
"""

import argparse, os, signal, time   # python packages
import fsevents                     # https://pypi.python.org/pypi/MacFSEvents

# CONFIG PARAMS, set envirovnment variables or hardcode
# include trailing slashes for rsync, being more explicit is better
local_path  = os.getenv('FSWATCH_LOCAL_PATH',  '/hard/coded/path/')
remote_host = os.getenv('FSWATCH_REMOTE_HOST', 'user@remote.server.com')
remote_path = os.getenv('FSWATCH_REMOTE_PATH', '/remote/hard/coded/')

# list of files to ignore, simple substring match
ignore_list = ['.svn', '.DS_Store']

def main():
    global observer, stream
    observer = fsevents.Observer()
    observer.start()
    stream = fsevents.Stream(file_event_sync, local_path, file_events=True)
    observer.schedule(stream)

    if not args.quiet:
        print "Watching: %s -- [ ctrl-c to quit ] " % local_path
    signal.signal(signal.SIGINT, clean_exit)
    signal.pause()  # run until ctrl-c


def file_event_sync(event):
    """ callback on event action, this does the sync passing in filename """
    filename = event.name
    remote_file = filename.replace(local_path, '')  # switch local path to remote
    for ig in ignore_list:                          # check ignore list
        if ig in filename:
            return
    
    # basic rsync to remote server
    cmd = " rsync -cazq %s %s:%s%s " % (filename, remote_host, remote_path, remote_file)
    if not args.quiet:
         print "Syncing ", filename
    os.system(cmd)


def clean_exit(signal, frame):
    """ Mom always says, clean up after yourself """
    global observer, stream
    observer.unschedule(stream)
    observer.stop()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='watches directory for changes and syncs to remote')
    parser.add_argument('--verbose', action='store_true', help='verbose output')
    parser.add_argument('--quiet',   action='store_true', help='quiet output')
    args = parser.parse_args()
    main()
