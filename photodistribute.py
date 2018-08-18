import os
import time
import exifread
import datetime
import struct
import sys
import shutil

ATOM_HEADER_SIZE = 8
EPOCH_ADJUSTER = 2082844800

def get_photo_createtime(path):
    f = open(path)
    tags = exifread.process_file(f)
    createtime = str(tags["Image DateTime"])
    
    y = int(createtime[0:4])
    m = int(createtime[5:7])
    d = int(createtime[8:10])
    date = datetime.date(y, m, d)
    return date

def get_movie_createtime(path):
    f = open(path, "rb")
    while 1:
        atom_header = f.read(ATOM_HEADER_SIZE)
        if atom_header[4:8] == 'moov':
            break;
        else:
            atom_size = struct.unpack(">I", atom_header[0:4])[0]
            f.seek(atom_size - 8, 1)

    atom_header = f.read(ATOM_HEADER_SIZE)
    if atom_header[4:8] == 'mvhd':
        f.seek(4, 1)
        createtime = struct.unpack(">I", f.read(4))[0]
        return datetime.datetime.utcfromtimestamp(createtime - EPOCH_ADJUSTER)
    else:
        return "unknown create date"

workPath = "/volume1/photo/distribute"
destPath = "/volume1/photo/"

for f in os.listdir(workPath):
    path = os.path.join(workPath, f)
    
    if path.find("jpg") != -1:
        time = get_photo_createtime(path)
    elif path.find("mp4") != -1:
        time = get_movie_createtime(path)
    else:
        continue

    dest = destPath + str(time.year) + "." + str(time.month)
    if os.path.exists(dest) != True:
        os.mkdir(dest)
        os.chmod(dest, 0777)
        print("Make new directory : ", dest)

    fullPath = dest + "/" + f
    if os.path.exists(fullPath) != True:
        src = workPath + "/" + f
        shutil.move(src, fullPath)
        print("move file : ", fullPath)
    else:
        print("exist file", fullPath)


