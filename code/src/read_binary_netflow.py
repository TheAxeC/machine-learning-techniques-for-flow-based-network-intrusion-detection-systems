

def main(filepath):
    print filepath
    d=search_file(filepath)
    #d.set_where(start="2009-03-23 11:00")
    #records=d.search('', statistics='port', statistics_order='bytes')
    for r in d:
        print "line"
        print r['last'], r['dstip'], r['dstport'], r['bytes']

import sys
if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(str(sys.argv[1]))
    else:
        main()
