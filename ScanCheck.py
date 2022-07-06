# Read config file - for database connection
import pandas as pds
from sqlalchemy import create_engine
from configparser import ConfigParser
import psycopg2


def config(filename='database.ini', section='sql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db

# Connect to database
def get_scan(parcelnumbers,scantype="05"):
    #params = config()
    alchemyEngine = create_engine("postgresql+psycopg2://user:pass@10.2.20.33/dpdregister");
    dbConnection = alchemyEngine.connect()



    sql = f"""SELECT depot, sdate, stime, parcelno, geoid, location, country, tpcode, 
                             service, generated FROM scans.scandata"""+scantype+""" 
                                WHERE parcelno in %s""" % str(parcelnumbers)

    query = pds.read_sql_query(sql, dbConnection)
    #print(sql)

    return query.set_index('parcelno')


# generator to flatten values of irregular nested sequences,
# modified from answers http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
def flatten(l):
    for el in l:
        try:
            yield from flatten(el)
        except TypeError:
            yield el



