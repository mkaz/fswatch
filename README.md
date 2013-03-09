fswatch
=======

This script will watch a local directory using Mac OS X FSEvents
and on change will sync to a remote directory. The script can be
easily modified to do whatever you want on a change event.

**Install** 
`pip install fsevents`


**Note:** if you are running against a large directory, it will 
take awhile at the beginning, my hunch is it needs to traverse
all sub-directories and attach the listeners everywhere


### TODO

  * setup as a daemon
  * add catch-up mode, in case weren't running it and made changes
  
 
 