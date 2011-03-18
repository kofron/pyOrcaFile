# We need this to be able to read the binary data
# format in the ORCA files
from struct import unpack

# for file seeking offsets
from os import SEEK_END, SEEK_CUR

# We need this for header stuff
from plistlib import readPlistFromString as rpl

# Takes a file handle and returns a 
# tuple (HeaderLength, RecordLength)
def get_hd_rc_lengths(file_handle):
    file_handle.seek(0)
    (rc,hd) = unpack('>LL',file_handle.read(8))
    return (hd,rc)   

# Takes a file handle and returns
# the header for the ORCA file in plist form.
def get_header(file_handle, length):
    file_handle.seek(8)
    return rpl(file_handle.read(length))

# Takes a header and returns the dataId for the
# run
def get_dataId(header):
    return header['dataDescription']['ORRunModel']['Run']['dataId']

# Takes a header and returns the start time of the run
def get_t0(header):
    return header['ObjectInfo']['DataChain'][0]['Run Control']['startTime']

# Takes a file handle and an offset where the
# first data record is located and returns the
# dataID and timestamp of the run record.
def get_firstRunRec(file_handle,offset):
    (dId,noOp,noOp,ts) = unpack('>LLLL',file_handle.read(16))
    return (dId,ts)

# Takes a file handle and gets the last record.
def get_lastRunRec(file_handle):
    file_handle.seek(0,SEEK_END)
    file_handle.seek(-16,SEEK_CUR)
    (dId,noOp,noOp,ts) = unpack('>LLLL',file_handle.read(16))
    return (dId,ts)

# Gets the livetime in seconds for an ORCA run file.
def get_livetime(file_handle):
    (hd,noOp) = get_hd_rc_lengths(file_handle)
    t0 = get_t0(get_header(file_handle,hd))
    (dId,tf) = get_lastRunRec(file_handle)
    return tf-t0
