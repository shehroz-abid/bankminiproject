
#Just a testing File

import MySQLdb

try:
    con = MySQLdb.connect("localhost", "root", "123456", "shehroz")
    print("Connection done")
except Exception.why:
    print(why)