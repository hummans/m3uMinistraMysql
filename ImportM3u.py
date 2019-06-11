#!/usr/bin/python
'''
Created on May 27, 2019

@author: zack
'''

import sys
import M3uParser
import MinistraSQL
import os
import argparse

def useGenreMapFile(self,GenreMapFile):
    self.genreMap = {}
    with open(GenreMapFile) as f:
        for line in f:
            if ":" in line:
                (key, val) = line.split(":")
                self.genreMap[key.rstrip()] = val.rstrip()

def main(argv=None): 
    parser = argparse.ArgumentParser(description='Process import args.')
    parser.add_argument('-t', '--tag', help='xmltv-id prefix: any tag/id of your choice. channels will be added to a tariff with this name',default="")
    parser.add_argument('-g', '--genre', help='genre mapping text file name in format: XMLTV-Group name:your genre  entries that end in ^ will cause that groups channels to be skipped')
    parser.add_argument('-n', '--channel', help='A prefix for your channel names', default="")
    parser.add_argument('-r', '--remove', help='clear out existing channels first',action='store_true')
    requiredNamed = parser.add_argument_group('required arguments')
    requiredNamed.add_argument('-m', '--m3u', help='Input m3u name', required=True)
    args=parser.parse_args()
    
    sql = MinistraSQL.MinistraSQL("root","st@lk3r","localhost",args.tag)
    
    if args.remove:
        sql.cleanChannels()
        
    myM3u = M3uParser.M3uParser();
    myM3u.readM3u(args.m3u)
    
    genreMap = {} 
    if os.path.isfile(args.genre):
        useGenreMapFile(args.genre)
     
    for i in myM3u.getList():
        genre = i["tvg-group"]
        if i["tvg-group"] in genreMap.keys():
            genre = genreMap[i["tvg-group"]]     
        
        if genre.endswith("^"):
            continue
        
        if "/series/" in i["link"]:
            pass
        elif "/movie/" in i["link"]:
            pass
        elif "24/7" in genre:
            sql.insertMovie(i["tvg-ID"] + args.channel,i["tvg-name"], genre, i["link"], i["tvg-logo"])
        else:
            sql.insertChannel(i["tvg-ID"] + args.channel,i["tvg-name"], genre, i["link"], i["tvg-logo"])


if __name__ == '__main__':
    sys.exit(main())

