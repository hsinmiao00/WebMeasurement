import sqlite3
import logging
import os
import argparse


def analyze(DBFILE,TYPE):
    #print(DBFILE)
    db = sqlite3.connect(DBFILE)
    cursor = db.cursor()
    
    if(TYPE == "cookies"):
        print("========cookies=======")
        cursor.execute('''SELECT domain, top_url FROM cookies''')
    elif(TYPE == "http_requests"):
        print("========http_requests=======")
        cursor.execute('''SELECT url, top_url FROM http_requests''')
    else:
        print("Please input TYPE")
        return
    count = 0;
    hit = 0;
    topURL = "";
    
    for user1 in cursor:
        #user1 = cursor.fetchone() #retrieve the first row
    
        domainName = str(user1[1]).split("//")[1].split(".")[0]
        #print(domainName)
        
        if( topURL != domainName ):
            if(TYPE == "cookies"):
                print("domain:"+topURL+", cookie count:"+str(count)+", third-party cookie count:"+str(hit))
            else:
                print("domain:"+topURL+", request count:"+str(count)+", third-party request count:"+str(hit))
                
            topURL = domainName
            count = 0
            hit = 0

        if(str(user1[0]).find(domainName)==-1):
            hit += 1
            #print(user1[0])
            #print(domainName)
            #break
        #else:
            #print("found")
        count += 1
    
    db.close()

if __name__ == '__main__':
    p = argparse.ArgumentParser(description="Analyze the cookies in a database file.")
    p.add_argument('file', metavar='DBFILE', help='DB file')
    args = p.parse_args()
    analyze(args.file,"cookies")
    analyze(args.file,"http_requests")
