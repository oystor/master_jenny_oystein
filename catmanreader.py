#!/usr/bin/env python

#   library: catmanreader.py
#
#   Description: Read catman generated binary files
#
#   Author: David Kristiansen, January 2019.
#

import numpy as np
import os.path
import struct
from collections import namedtuple
from datetime import datetime
import sys
import argparse
import h5py


__version__ = "Version 1.1"

ver = sys.version
if int(ver[0]) < 3:
    ver27 = True
    print("Current Python version is not supported. Module requires Python version 3.5+")
    exit(0)


def bytes_from_file(filename, chunksize=8192):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for b in chunk:
                    yield b
            else:
                break

def unpack_short(filecontent, filepos):
    '''
    Unpack short from binary file
    :param filecontent: binary data read from file
    :param filepos: integer position to start read
    :return: read short and new filepos
    '''
    newpos = filepos + 2
    shortval = struct.unpack("h", filecontent[filepos: newpos])
    return shortval, newpos


def unpack_long(filecontent, filepos):
    '''
    Unpack long from binary file
    :param filecontent: binary data read from file
    :param filepos: integer position to start read
    :return: read long and new filepos
    '''
    newpos = filepos + 4
    shortval, = struct.unpack("l", filecontent[filepos: newpos])
    return shortval, newpos


def unpack_float(filecontent, filepos):
    '''
    Unpack long from binary file
    :param filecontent: binary data read from file
    :param filepos: integer position to start read
    :return: read long and new filepos
    '''
    newpos = filepos + 4
    doubleval, = struct.unpack("f", filecontent[filepos: newpos])
    return doubleval, newpos


def unpack_double(filecontent, filepos):
    '''
    Unpack long from binary file
    :param filecontent: binary data read from file
    :param filepos: integer position to start read
    :return: read long and new filepos
    '''
    newpos = filepos + 8
    doubleval, = struct.unpack("d", filecontent[filepos: newpos])
    return doubleval, newpos


def unpack_bytes(filecontent, filepos, numbytes, asbytes=False):
    '''
    Unpack long from binary file
    :param filecontent: binary data read from file
    :param filepos: integer position to start read
    :return: read string and new filepos
    '''
    if numbytes > 0:
        keystr = "{}c".format(numbytes)
        newpos = filepos + numbytes
        bytesarray = struct.unpack(keystr, filecontent[filepos: newpos])
    else:
        bytesarray = ()
        outstr = ''
        newpos = filepos
    if asbytes == True:
        outstr = bytesarray
    else:
        outstr = b''.join(bytesarray).decode('UTF-8', "replace")
        #outstr = b''.join(bytesarray) #.decode

    return outstr, newpos


def unpack_string(filecontent, filepos, numbytes):
    '''
    Unpack string from binary file
    :param filecontent: binary data read from file
    :param filepos: integer position to start read
    :return: read string and new filepos
    '''
    if numbytes > 0:
        keystr = "{}s".format(numbytes)
        newpos = filepos + numbytes
        bytesarray = struct.unpack(keystr, filecontent[filepos: newpos])
        outstr = b''.join(bytesarray).decode('UTF-8')
    else:
        bytesarray = ()
        outstr = ''
        newpos = filepos

    return outstr, newpos


def unpack_byte_as_int(filecontent, filepos):
    '''
    Unpack long from binary file
    :param filecontent: binary data read from file
    :param filepos: integer position to start read
    :return: read string and new filepos
    '''
    newpos = filepos + 1
    byteread, = struct.unpack('c', filecontent[filepos: newpos])
    outval = int(byteread[0])
    return outval, newpos


def unpack_char(filecontent, filepos, unsigned=True):
    '''
    Unpack long from binary file
    :param filecontent: binary data read from file
    :param filepos: integer position to start read
    :return: read string and new filepos
    '''
    newpos = filepos + 1
    if unsigned == True:
        keystr = 'B'
    else:
        keystr = 'b'
    byteread, = struct.unpack('b', filecontent[filepos: newpos])
    outval = int(byteread[0])
    return outval, newpos


def unpack_int(filecontent, filepos, unsigned=True):
    '''
    Unpack int from binary file
    :param filecontent: binary data read from file
    :param filepos: integer position to start read
    :return: read string and new filepos
    '''
    newpos = filepos + 4
    if unsigned == True:
        keystr = 'I'
    else:
        keystr = 'i'
    byteread, = struct.unpack(keystr, filecontent[filepos: newpos])
    outval = int(byteread[0])
    return outval, newpos


def unpack_vb_db_chanheader(filecontent, filepos, numbytes=148):

    startbyte = filepos
    T0, filepos = unpack_double(filecontent, filepos)
    dt, filepos = unpack_double(filecontent, filepos)
    sensortype, filepos = unpack_short(filecontent, filepos)
    supplyvoltage, filepos = unpack_short(filecontent, filepos)
    filtchar, filepos = unpack_short(filecontent, filepos)
    filtfreq, filepos = unpack_short(filecontent, filepos)
    tareval, filepos = unpack_float(filecontent, filepos)
    zeroval, filepos = unpack_float(filecontent, filepos)
    measrange, filepos = unpack_float(filecontent, filepos)
    #inchar, filepos = unpack_float(filecontent, filepos)
    incharvec = []
    for item in range(4):
         inchar, filepos = unpack_float(filecontent, filepos)
         incharvec.append(inchar)
    #inputcharacteristics = {0: "x1", 1: "y1", 2: "x2", 3: "y2"}
    serialno, filepos = unpack_bytes(filecontent, filepos, 32)
    physunit, filepos = unpack_bytes(filecontent, filepos, 8)
    nativeunit, filepos = unpack_bytes(filecontent, filepos, 8)
    slot, filepos = unpack_short(filecontent, filepos)
    subslot, filepos = unpack_short(filecontent, filepos)
    amptype, filepos = unpack_short(filecontent, filepos)
    aptype, filepos = unpack_short(filecontent, filepos)
    kfactor, filepos = unpack_float(filecontent, filepos)
    bfactor, filepos = unpack_float(filecontent, filepos)
    meassig, filepos = unpack_short(filecontent, filepos)
    ampinput, filepos = unpack_short(filecontent, filepos)
    hpfilt, filepos = unpack_short(filecontent, filepos)
    olimportinfo, filepos = unpack_byte_as_int(filecontent, filepos)
    scaletype, filepos = unpack_byte_as_int(filecontent, filepos)
    softwaretareval, filepos = unpack_float(filecontent, filepos)
    writeprotected, filepos = unpack_byte_as_int(filecontent, filepos)
    nominalrange, filepos = unpack_float(filecontent, filepos)
    clcfactor, filepos = unpack_float(filecontent, filepos)
    exportformat, filepos = unpack_byte_as_int(filecontent, filepos)
    reserve, filepos = unpack_bytes(filecontent, filepos, 10)
    endbyte = filepos

    bytesread = endbyte-startbyte

    vb_db_chanheader_struct = VB_DB_ChanHeader(T0=T0,
                           dt=dt,
                           SensorType=sensortype,
                           SupplyVoltage=supplyvoltage,
                           FiltChar=filtchar,
                           FiltFreq=filtfreq,
                           TareVal=tareval,
                           ZeroVal=zeroval,
                           MeasRange=measrange,
                           InChar=incharvec,
                           SerNo=serialno,
                           PhysUnit=physunit,
                           NativeUnit=nativeunit,
                           Slot=slot,
                           SubSlot=subslot,
                           AmpType=amptype,
                           APType=aptype,
                           kFactor=kfactor,
                           bFactor=bfactor,
                           MeasSig=meassig,
                           AmpInput=ampinput,
                           HPFilt=hpfilt,
                           OLImportInfo=olimportinfo,
                           ScaleType=scaletype,
                           SoftwareTareVal=softwaretareval,
                           WriteProtected=writeprotected,
                           NominalRange=nominalrange,
                           CLCFactor=clcfactor,
                           ExportFormat=exportformat,
                           Reserve=reserve)

    return vb_db_chanheader_struct, filepos

def unpack_db_sensorinfo(filecontent, filepos, numbytes=68):

    # Unpack parameters from binary
    inuse, filepos = unpack_short(filecontent, filepos)
    description, filepos = unpack_bytes(filecontent, filepos, 50)
    TID, filepos = unpack_bytes(filecontent, filepos, 16)

    # Fill named tuple
    db_sensorinfo = DBSensorInfo(inuse, description, TID)

    return db_sensorinfo, filepos

def now_time_to_sec(nowtime):
    seconds = (nowtime - 25569) * 86400.0
    return seconds

def as_string(bytesarray):
    return b''.join(bytesarray).decode('UTF-8')


#======================================================================================
# Define catman types
#======================================================================================
DBSensorInfo = namedtuple("DBSensorInfo", "InUse Description TID")

VB_DB_ChanHeader = namedtuple("VB_DB_ChanHeader",
                              "T0 dt SensorType SupplyVoltage FiltChar FiltFreq TareVal ZeroVal MeasRange " \
                              "InChar SerNo PhysUnit NativeUnit Slot SubSlot AmpType APType kFactor bFactor " \
                              "MeasSig AmpInput HPFilt OLImportInfo ScaleType SoftwareTareVal WriteProtected " \
                              "NominalRange CLCFactor ExportFormat Reserve")




#======================================================================================
# Catman binary file reader
#======================================================================================

class import_catman_binary:

    def __init__(self, filename):

        self.filename = filename

        assert os.path.splitext(filename)[1] == '.bin'

        with open(filename, "rb") as file:
            filetop = file.read(6)

        #==================================================
        # Global section:
        #==================================================

        globalparams = {}
        filepos = 0
        self.fileid, filepos = unpack_short(filetop, filepos)
    
        tupInt = ''.join(map(str, self.fileid ))
        self.fileid = tupInt

        self.version = int(self.fileid)
        if self.version >= 5009:
            self.dataoffset, filepos = unpack_long(filetop, filepos)

        with open(filename, "rb") as file:
            filecontent = file.read(self.dataoffset)

        globalparams['fileID'] = self.fileid
        globalparams['dataoffset'] = self.dataoffset

        filepos = 6
        L, filepos = unpack_short(filecontent, filepos)
        tupL = ''.join(map(str, L))
        L = int(tupL)
        if L > 0:
            comment, filepos = unpack_bytes(filecontent, filepos, L)
            globalparams['comment'] = ''.join(comment)
        else:
            globalparams['comment'] = ''

        if self.version >= 5011:
            #    print("Reserved...")
            for rs in range(32):
                L, filepos = unpack_short(filecontent, filepos)
                tupL = ''.join(map(str, L))
                L = int(tupL)
                if L > 0:
                    string, filepos = unpack_bytes(filecontent, filepos, L)
                    globalparams['reservedstring_{}'.format(rs)] = string
        self.numchans, filepos = unpack_short(filecontent, filepos)
        tupL = ''.join(map(str, self.numchans))
        self.numchans = int(tupL)
        globalparams['numchannels'] = self.numchans

        if self.version >= 5010:
            maxchanlen, filepos = unpack_long(filecontent, filepos)
            globalparams['maxchanlength'] = maxchanlen
            self.channeloffset = []
            for rs in range(self.numchans):
                chanoffset, filepos = unpack_long(filecontent, filepos)
                globalparams['channeloffset_{}'.format(rs)] = chanoffset
                self.channeloffset.append(chanoffset)
            reductionfactor, filepos = unpack_long(filecontent, filepos)
            globalparams['reductionfactor'] = reductionfactor

        self.__global__ = globalparams

        #==================================================
        # Channel header section:
        #==================================================

        # Loop over channels
        self.chanheaders = []
        self.chandataentry = np.zeros((self.numchans), dtype='int64')
        self.NVals = np.zeros((self.numchans), dtype='int64')

        for chan in range(self.numchans):
            channel = {}
            chanloc, filepos = unpack_short(filecontent, filepos)
            chanlen, filepos = unpack_long(filecontent, filepos)
            channel['dblocation'] = chanloc
            channel['numsamples'] = chanlen
            self.NVals[chan] = chanlen

            L, filepos = unpack_short(filecontent, filepos)
            L = int(''.join(map(str, L)))
            channel['name'] = ''
            if L > 0:
                channelname, filepos = unpack_bytes(filecontent, filepos, L)
                channel['name'] = channelname
            L, filepos = unpack_short(filecontent, filepos)
            L = int(''.join(map(str, L)))
            channel['unit'] = ''
            if L > 0:
                unitname, filepos = unpack_bytes(filecontent, filepos, L)
                channel['unit'] = unitname

            if self.version <= 5009:
                L, filepos = unpack_short(filecontent, filepos)
                L = int(''.join(map(str, L)))
                channel['datestamp'] = ''
                if L > 0:
                    dateofmeasurement, filepos = unpack_bytes(filecontent, filepos, L)
                    channel['datestamp'] = dateofmeasurement
                L, filepos = unpack_short(filecontent, filepos)
                L = int(''.join(map(str, L)))
                channel['timestamp'] = ''
                if L > 0:
                    timeofmeasurement, filepos = unpack_bytes(filecontent, filepos, L)
                    channel['timestamp'] = timeofmeasurement

            L, filepos = unpack_short(filecontent, filepos)
            L = int(''.join(map(str, L)))
            channel['comment'] = ''
            if L > 0:
                comment, filepos = unpack_bytes(filecontent, filepos, L)
                channel['comment'] = comment
            if self.version >= 5007:
                chanformat, filepos = unpack_short(filecontent, filepos)
                datawidth, filepos = unpack_short(filecontent, filepos)
                channel['format'] = chanformat
                channel['datawidth'] = datawidth
            if self.version >= 5010:
                timeofmeasurement, filepos = unpack_double(filecontent, filepos)
                seconds = now_time_to_sec(timeofmeasurement)
                timestamp = datetime.fromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%S')
                channel['timestamp'] = timestamp
            if self.version >= 5008:
                extchanheadersize, filepos = unpack_long(filecontent, filepos)
                extchanheader, filepos = unpack_vb_db_chanheader(filecontent, filepos, numbytes=extchanheadersize)
                channel['extchannelheader'] = extchanheader

            if self.version >= 5009:
                mode, filepos = unpack_byte_as_int(filecontent, filepos)
                channel['linearization_mode'] = mode
                usrscaletype, filepos = unpack_byte_as_int(filecontent, filepos)
                nScalData, filepos = unpack_byte_as_int(filecontent, filepos)
                channel['user_scale_type'] = usrscaletype
                nScalDataVals = np.zeros((nScalData))
                for pt in range(nScalData):
                    nScalDataVals[pt], filepos = unpack_double(filecontent, filepos)
                channel['numscaledata'] = nScalData
                channel['scaledata'] = nScalDataVals

                thermotype, filepos = unpack_short(filecontent, filepos)
                channel['thermo-type'] = thermotype
                L, filepos = unpack_short(filecontent, filepos)
                L = int(''.join(map(str, L)))
                channel['formula'] = ''
                if L > 0:
                    formula, filepos = unpack_bytes(filecontent, filepos, L)
                    channel['formula'] = formula

            if self.version >= 5012:
                L, filepos = unpack_long(filecontent, filepos)
                dbsensorinfo, filepos = unpack_db_sensorinfo(filecontent, filepos, L)
                channel['sensorinfo'] = dbsensorinfo

            expformat = {0: ('d', 8), 1: ('f', 4), 2: ('h', 2)}

            if chan == 0:
                self.chandataentry[chan] = self.dataoffset
            else:
                prevchan = self.chanheaders[chan-1]
                self.chandataentry[chan] = self.chandataentry[chan-1] + int(channel['numsamples']) * expformat[channel['extchannelheader'].ExportFormat][1]
                #self.chandataentry[chan] = self.chandataentry[chan-1] + int(prevchan['numsamples']) * int(prevchan['datawidth'])

            self.chanheaders.append(channel)


        #==================================================
        # Post data area:
        #==================================================
        self.postdata = {}
        if self.version >= 5011:
            id, filepos = unpack_short(filecontent, filepos)
            self.postdata.update({"id": id})

            for ichan, chan in enumerate(self.chanheaders):
                L, filepos = unpack_short(filecontent, filepos)
                L = int(''.join(map(str, L)))
                if L > 0:
                    formatstring, filepos = unpack_bytes(filecontent, filepos, L)
                    self.postdata.update({"formatstring, channel {}".format(ichan): formatstring})


    def print_globals(self):

        print("File ID: {}".format(self.fileid))
        print("Data offset: {}".format(self.dataoffset))
        print("Comment: {}".format(self.__global__['comment']))
        print("Number of channels: {}".format(self.numchans))

        if self.version > 5010:
            print("Max channel length (normally=0, used for special append mode): {}" \
                  .format(self.__global__['maxchanlength']))
            for rs in range(self.numchans):
                print("Offset, channel {}: {}".format(rs, self.__global__['channeloffset_{}'.format(rs)]))
            print("Reduction factor: {}".format(self.__global__['reductionfactor']))


    def print_channel_headers(self):

        for i, chan in enumerate(self.chanheaders):

            print("\n\nChannel {}".format(i+1))
            print("-----------------------------------------")
            print("Location in catman database: {}".format(chan['dblocation']))
            print("Length (number of samples): {}".format(chan['numsamples']))
            print("Name: {}".format(chan['name']))
            print("Unit: {}".format(chan['unit']))
            if self.version <= 5009:
                print("Date of measurement: {}".format(chan['datestamp']))
                print("Time of measurement: {}".format(chan['timestamp']))
            print("Comment: {}".format(chan['comment']))
            if self.version >= 5007:
                print("Channel format: {}".format(chan['format']))
                print("Data width in Bytes: {}".format(chan['datawidth']))
            if self.version >= 5010:
                print("Date and time of measurement: {}".format(chan['timestamp']))
            if self.version >= 5008:
                print("Extended channel header:\n {}".format(chan['extchannelheader']))
            if self.version >= 5009:
                linmodes = {0: 'None', 1: 'Extern Hardware', 2: 'User scale', 3: 'Thermo J'}
                print("Linearization mode: \t{} = {} ".format(chan['linearization_mode'], linmodes[chan['linearization_mode']]))
                scaletypes = {0: 'Linearization table', 1: 'Polynom', 2: 'f(x)', 3: 'DMS Skalierung'}
                print("User scale type: \t\t{} = {}".format(chan['user_scale_type'], scaletypes[chan['user_scale_type']]))
                print("Number of points for user scale linearization table: {}".format(chan['numscaledata']))
                print("Points: {}".format(chan['scaledata']))
                print("Thermo-type: {}".format(chan['thermo-type']))
                print("Formula: {}".format(chan['formula']))
            if self.version >= 5012:
                print("DB-SensorInfo: {}".format(chan['sensorinfo']))


    def print_channel_list(self):

        print("\nData-file: {}".format(self.filename))
        print("Channel list:")
        print("--------------------------------------------------------------------------")
        for i, chan in enumerate(self.chanheaders):
            print("Channel {}:\t Name = {},\t Unit = {}".format(i, chan['name'], chan['unit']))

    def get_channel_headers(self):
        return self.chanheaders

    def get_data(self, channels=[], numsamples=0):

        if channels == []:
            channels = range(self.numchans)

        data = {}
        keylist = []

        readsamples = ''
        if numsamples == 0:
            "Read all samples"
            readsamples = 'all'

        for ch in channels:
            if ch in range(self.numchans):
                chan = self.chanheaders[ch]
            else:
                print("Invalid channel index: {}. Skipping...".format(ch))
                continue
            name = chan['name']
            unit = chan['unit']
            #print("Loading data from channel {}: {}".format(ch, name))
            exportformat = chan['extchannelheader'].ExportFormat

            if exportformat == 0:
                #samplesize = 8
                typekey = 'd'
            elif exportformat == 1:
                #samplesize = 4
                typekey = 'f'
            elif exportformat == 2:
                #samplesize = 2
                typekey = 'h'
            else:
                print("Cannot import data due to unknown data format.")
                return 0

            samplesize = struct.calcsize(typekey)

            if readsamples == 'all':
                # Read all samples
                numsamples = chan['numsamples']
                datawidth = chan['datawidth'][0]

                #print(f'Numsamples {numsamples}, type: type:{type(numsamples)} Datawidth: {datawidth}, type: type{type(datawidth)}')

                with open(self.filename, "rb") as file:
                    file.seek(self.chandataentry[ch], 0)
                    datastr = file.read(numsamples*datawidth)
                    chandata = struct.unpack(typekey*numsamples, datastr)

                # Append channel data to data matrix
                if ch == 0:
                    data = {ch: np.array(chandata)}
                    keylist = [chan['name']]
                    #data = np.array(chandata)
                else:
                    keylist.append(chan['name'])
                    data.update({ch: np.array(chandata)})
                    #data = np.c_[data, np.array(chandata)]

        return data, keylist #zip(keylist, data)


    def print_postdataarea(self):
        print(self.postdata)


#fileinfo = {'globals': globalparams, 'channelinfo': chanheaders, 'data': data, 'post-data': postdata}
#    return fileinfo

def export_to_hdf5(outfile, data, keys):
    ta, keys = binary.get_data(outfile)
    hf = h5py.File(os.path.splitext(outfile)[0]+'.h5', 'w')
    for key, (ch, item) in zip(keys, data.items()):
        hf.create_dataset(key, data=item, compression='gzip')
    hf.close()

def argumentparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', help="Input file name.")
    parser.add_argument('--searchpath', action='store', default=False, dest='search_path', help='Search path for input files')
    parser.add_argument('--chanlist', action='store_true', default=False, dest='print_chanlist', help="Print list of data channel names")
    parser.add_argument('--chanheaders', action='store_true', default=False, dest='print_headers', help="Print extended headers")
    parser.add_argument('--globals', action='store_true', default=False, dest='print_globals', help="Print global parameters")
    parser.add_argument('--postdata', action='store_true', default=False, dest='print_postdata', help="Print post-data area")
    parser.add_argument('--channels', action='store', default='[]', type=str, dest='channels', help="Specify channels to export")
    parser.add_argument('--export', action='store_true', default=False, dest='export_data', help="Export data to python binary")
    parser.add_argument('--hdf5', action='store_true', default=False, dest='hdf5', help="HDF5 export format")
    parser.add_argument('--outname', action='store', default=None, dest='outfile', help="Specify filename base for output")
    parser.add_argument('--outdir', action='store', dest='outdir', help='Output directory for exported data')
    return parser

def print_usage():
    print("Catman reader - read binary data files created by Catman.")
    print("Author: David Kristiansen, NTNU, 2019.")
    print("#")
    print("# Use as module:")
    print("#-----------------")
    print("import catmanreader as cr")
    print("#")
    print("inputfile = \"testinput.bin\"")
    print("binary = cr.import_catman_binary(inputfile)")
    print("# Implemente methods:")
    print("binary.print_channel_list()    # Print list of data channels")
    print("binary.print_globals()         # Print global parameters of data file.")
    print("binary.print_channel_headers() # Print extended headers of each data channel.")
    print("binary.print_postdataarea()    # Print post-data area of data file (usually empty).")
    print("data, keys = binary.get_data() # Load all data channels into variable \"data\", with data columns corresponding to keys list")
    print("selecteddata, selectedkeys = binary.get_data(channellist) # Load given data channels into variable \"selecteddata\", with data columns corresponding to keys list")


if __name__ == '__main__':

    parser = argumentparser()
    args = parser.parse_args()

    if args.search_path:
        # Search given path for input bin-files:
        infilelist = [os.path.join(root, name) for root, dirs, files in os.walk(args.search_path)
                     for name in files if name.endswith((".bin", ".BIN"))]
    else:
        # Binary input files given
        infilelist = [args.infile]

    for infile in infilelist:
        # Loop over given/found input files
        try:
            #print("Loading file "+infile)
            binary = import_catman_binary(infile)
            if args.print_chanlist:
                binary.print_channel_list()
            if args.print_headers:
                binary.print_channel_headers()
            if args.print_globals:
                binary.print_globals()
            if args.print_postdata:
                binary.print_postdataarea()

            # Input:
            chanliststr = args.channels.strip('][').split(',')
            chanlist = []
            if len(chanliststr) > 2: # Length of empty list of string is 2, ['']
                chanlist = [int(ch) for ch in chanliststr]
                print("Selected store channels: ", chanlist)

            # Output:
            outfilename = os.path.basename(infile).strip('StoreChannels')
            outdir = os.path.curdir
            if args.outfile is not None:
                outfilename = args.outfile + outfilename
            if args.outdir is not None:
                outdir = args.outdir


            if args.export_data:
                outfilename = os.path.splitext(outfilename)[0]
                outfile = os.path.join(outdir, outfilename)
                data, keys = binary.get_data(chanlist)
                if args.hdf5:
                    print("Exporting data to hdf5 file", outfile+'.h5')
                    export_to_hdf5(outfile, data, keys)
                else:
                    print("Exporting data numpy binary file", outfile+'.npz')
                    np.savez(outfile+'.npz', data=data, keys=keys)

        except FileNotFoundError:
            print("Could not locate input file at: {}".format(infile))
            exit(0)
