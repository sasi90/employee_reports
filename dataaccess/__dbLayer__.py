import json
import mysql.connector
# import logging

# logging.basicConfig(filename='logs/traces.log',format='%(levelname)s | %(asctime)s | module: %(module)s | lineno: %(lineno)d | %(message)s')


av3arDB_CNX=None
dbCursor=None

class DataAccess:

    # def __int__(self):
    #     print()

    @staticmethod
    def openConnection():
        try:
            global av3arDB_CNX
            av3arDB_CNX= mysql.connector.connect(host='localhost',
                        database='emp_report',
                        user='root',
                        password='root@123')
            return av3arDB_CNX
        except Exception as e:
            # logging.error("Error while opening the DB connection")
            print('data connection unsuccess')

    @staticmethod
    def closeConnection():
         try:
             av3arDB_CNX.close()
             return ''
         except Exception as e:
             # logging.error("Error while closing the DB connection")
            pass


if __name__ == '__main__':
    DataAccess.openConnection()