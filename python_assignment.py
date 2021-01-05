#Script for all the problems given in the attachment

1: Write a Python program to read a file line by line and store it into a list.

Python Code: 

def file_read(fname):
        with open(fname) as f:
                #Content_list is the list that contains the read lines.     
                content_list = f.readlines()
                print(content_list)

file_read(\'test.txt\')

2: Write a Python program to calculate the number of days between two dates.
 Sample dates : (20200702), (20200711)

Python Code: 

from datetime import date
f_date = date(2020, 07, 02)
l_date = date(2020, 07, 11)
delta = l_date - f_date
print(delta.days)


3: Write a Python program to convert the Python dictionary object (sort by key) to
JSON data. Print the object members with indent level 4.

Python Code: 

import json
j_str = {'4': 5, '6': 7, '1': 3, '2': 4}
print("Original String:")
print(j_str)
print("\nJSON data:")
print(json.dumps(j_str, sort_keys=True, indent=4))

4: Write a Python program to sort a list of dictionaries using Lambda.
 Original list of dictionaries :
 [{'make': 'Nokia', 'model': 216, 'color': 'Black'}, {'make': 'Mi Max', 'model': '2',
'color': 'Gold'}, {'make': 'Samsung', 'model': 7, 'color': 'Blue'}]
 Sorting the List of dictionaries :
 [{'make': 'Nokia', 'model': 216, 'color': 'Black'}, {'make': 'Samsung', 'model': 7,
'color': 'Blue'}, {'make': 'Mi Max', 'model': '2', 'color': 'Gold'}]

Python Code : 

models = [{'make':'Nokia', 'model':216, 'color':'Black'}, {'make':'Mi Max', 'model':'2', 'color':'Gold'}, {'make':'Samsung', 'model': 7, 'color':'Blue'}]
print("Original list of dictionaries :")
print(models)
sorted_models = sorted(models, key = lambda x: x['color'])
print("\nSorting the List of dictionaries :")
print(sorted_models)

5: Write a Python program that takes a text file as input and returns the number of
words of a given text file.
Note: Some words can be separated by a comma with no space.

Python Code : 

def count_words(file_path):
   with open(file_path) as f:
       data = f.read()
       data.replace(",", " ")
       return len(data.split(" "))
print(count_words("words.txt"))

6: Write a Python program to convert an array to an array of machine values and
return the bytes representation.
Expected Output:
Original array:
A1: array('i', [1, 2, 3, 4, 5, 6])
Array of bytes: b'010000000200000003000000040000000500000006000000'

Python Code: 

import array
import binascii
a = array.array('i', [1,2,3,4,5,6])
print("Original array:")
print('A1:', a)
bytes_array = a.tobytes()
print('Array of bytes:', binascii.hexlify(bytes_array))

7: Write a script which can read the files line by line with .log ext and print it into a
file , while printing the data from the suffix with present date and time of the system.

Python Code: 

import arcpy
import sys
import os
import datetime
import traceback

# Database Connection
editDB = "Database Connections\\Frogmouth_Natural_Resources.sde" #Connect to the Natural Resources databse using TC_USer admin access"
# Current Day
Day = time.strftime("%m-%d-%Y", time.localtime())
# Current Time
Time = time.strftime("%I:%M:%S %p", time.localtime())


# Set workspace
workspace = editDB

# Set the workspace environment
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

try:
    # Start Time
    print 'Process Started at ' + str(Day) + " " + str(Time)

 # block new connections to the working and Frogmouth database.
  #  print "Blocking Connections..."
  #  arcpy.AcceptConnections(editDB, False)

# disconnect all users from the working and Frogmouth database.
    #print "Disconnecting Users..."
    #arcpy.DisconnectUser(editDB, "ALL")

# Get a list of all child versions besides QAQC and DEFAULT to pass into the ReconcileVersions tool.
    ver1List = [ver1.name for ver1 in arcpy.da.ListVersions(editDB) if ver1.name != 'TC_USER.QA/QC' and ver1.name != 'sde.DEFAULT']

# Execute the ReconcileVersions tool with QAQC Target Version and do not delete child versions
    print "Reconcile/post versions to QAQC...."
    arcpy.ReconcileVersions_management(editDB, "ALL_VERSIONS", "TC_USER.QA/QC", ver1List, "LOCK_ACQUIRED", "ABORT_CONFLICTS", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "KEEP_VERSION")

# Extract QAQC version from the list of versions to pass to ReconcileVersions tool.
    ver2List = [ver2.name for ver2 in arcpy.da.ListVersions(editDB) if ver2.name == 'TC_USER.QA/QC']

# Execute the ReconcileVersions tool with DEFAULT Target Version and do not delete QAQC version
    print "Reconcile/post QAQC to DEFAULT..."
    arcpy.ReconcileVersions_management(editDB, "ALL_VERSIONS", "sde.DEFAULT", ver2List, "LOCK_ACQUIRED", "ABORT_CONFLICTS", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "KEEP_VERSION")

# Run the compress tool.
    print "Compressing database..."
    arcpy.Compress_management(editDB)

# /////////////////////////////////// ANALYZE DATASETS AND CALC STATISTICS /////////////////////////////////////

    # NOTE: Rebuild indexes can accept a Python list of datasets.

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters.
    dataList = arcpy.ListTables() + arcpy.ListFeatureClasses() + arcpy.ListRasters()

# Next, for feature datasets get all of the datasets and featureclasses
    # from the list and add them to the master list.
    for dataset in arcpy.ListDatasets("*", "Feature"):
        arcpy.env.workspace = os.path.join(workspace, dataset)
        dataList += arcpy.ListFeatureClasses() + arcpy.ListDatasets()

        # reset the workspace
    arcpy.env.workspace = workspace

    # Concatenate all datasets into a list
    datasetList = [ds for ds in dataList]

    print "rebuilding indexes"
    # Execute rebuild indexes
    # Note: to use the "SYSTEM" option the workspace user must be an administrator.
    arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", datasetList, "ALL")
    print('Rebuild Complete')

    print "analyzing datasets"
    arcpy.AnalyzeDatasets_management(workspace, "NO_SYSTEM", datasetList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
    print "analysis complete"

    #Allow the database to begin accepting connections again
    print "Set databases to allow connections..."
    arcpy.AcceptConnections(editDB, True)

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ script initiation, Rec/Post process error handling \\\\\\\\\\\\\\\\\\\\\\\\\\\\\

except:
    print 'An error occured'
    failMsg = '\nSCRIPT FAILURE IN SCRIPT INITIATION OR RECONCILE-POST PROCESS, \n'
    failMsg += 'Most recent GP messages below.\n'
    failMsg += arcpy.GetMessages() +'\n'
    failMsg += '\nTraceback messages below.\n'
    failMsg += traceback.format_exc().splitlines()[-1]
    print failMsg
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ write error log info\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# move to working directory 
    os.chdir (u'Y:\\TOOLS\\Logs\\')
## define function with variable filename and the format of the timestamp
    def timeStamped(filename, fmt='%m-%d-%y-%H.%M.%S-{filename}'):
       return datetime.datetime.now().strftime(fmt).format(filename=filename)
## assign local variable filename and use whatever file name and extension you need
    filename = timeStamped('Infrastructure_RecPost_toQC_Log.txt')
## Create the logfile and assign write permission
    file = open(filename, "w")
    for line in file:
        print line

## and do it again for the second file
    filename = timeStamped('Infrastructure_RecPost_toDefault_Log.txt')
## Create the logfile and assign wright permission
    open(filename, "w")


8: Program to Generate random logs and write in a file , once the file size reaches 2Mb
open new file and continue writing

Python Code: 

import time
import re
import os
import stat
import logging
import logging.handlers as handlers


class SizedTimedRotatingFileHandler(handlers.TimedRotatingFileHandler):
    """
    Handler for logging to a set of files, which switches from one file
    to the next when the current file reaches a certain size, or at certain
    timed intervals
    """

    def __init__(self, filename, maxBytes=0, backupCount=0, encoding=None,
                 delay=0, when='h', interval=1, utc=False):
        handlers.TimedRotatingFileHandler.__init__(
            self, filename, when, interval, backupCount, encoding, delay, utc)
        self.maxBytes = maxBytes

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        Basically, see if the supplied record would cause the file to exceed
        the size limit we have.
        """
        if self.stream is None:                 # delay was set...
            self.stream = self._open()
        if self.maxBytes > 0:                   # are we rolling over?
            msg = "%s\n" % self.format(record)
            # due to non-posix-compliant Windows feature
            self.stream.seek(0, 2)
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        t = int(time.time())
        if t >= self.rolloverAt:
            return 1
        return 0


def demo_SizedTimedRotatingFileHandler():
    log_filename = '/tmp/log_rotate'
    logger = logging.getLogger('MyLogger')
    logger.setLevel(logging.DEBUG)
    handler = SizedTimedRotatingFileHandler(
        log_filename, maxBytes=2000, backupCount=5,
        when='s', interval=10,
        # encoding='bz2',  # uncomment for bz2 compression
    )
    logger.addHandler(handler)
    for i in range(10000):
        time.sleep(0.1)
        logger.debug('i=%d' % i)

demo_SizedTimedRotatingFileHandler()


9: Script to ping and check whether any given IPs are active, also whether given set of
software are installed in the existing system ( like java, kubectl, aws etc)

Python Code : 

import platform    # For getting the operating system name
import subprocess  # For executing a shell command

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0