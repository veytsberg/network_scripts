import argparse
import psycopg2
from getpass import getpass
import yaml


def get_db_parameters():
    parser = argparse.ArgumentParser(description='Collecting inventory from database')
    parser.add_argument('-n', '--name', dest='dbname', help='database name', required=True)
    parser.add_argument('-hs', '--host', dest='dbhost', help='database host', required=True)
    parser.add_argument('-u', '--user', dest='dbuser', help='username', required=True)
    args = parser.parse_args()
    return args


def get_inventory(sql_request, object_cursor_sql, filename_for_writing, groups):
    object_cursor_sql.execute(sql_request)
    f = open(filename_for_writing, 'w')
    for row in object_cursor_sql:
        yaml.dump({row[0]: {'hostname': row[1], 'groups': [groups], 'data': {'type': row[2]}}}, f)
        print(row)
    f.close()


parameters = get_db_parameters()
password = getpass('Database password: ')
conn = psycopg2.connect(dbname=parameters.dbname, user=parameters.dbuser,
                        password=password, host=parameters.dbhost)

cursor = conn.cursor()

#create all sql requests
sql_req_all_routers = "SELECT device,inet_ntoa(devip),type FROM public.devices WHERE snmpversion>0 AND lastdis>extract(epoch from (now() - INTERVAL '2 DAYS')) AND vendor='Cisco' AND services=78 AND type NOT LIKE 'WS-%'"
sql_req_all_switches = "SELECT device,inet_ntoa(devip),type FROM public.devices WHERE snmpversion>0 AND lastdis>extract(epoch from (now() - INTERVAL '2 DAYS')) AND vendor='Cisco' AND type LIKE 'WS-%'"
sql_req_all_nexus = "SELECT device,inet_ntoa(devip),type FROM public.devices WHERE snmpversion>0 AND lastdis>extract(epoch from (now() - INTERVAL '2 DAYS')) AND vendor='Cisco' AND (type LIKE 'N5K%' OR type LIKE 'N6K%')"


get_inventory(sql_req_all_routers, cursor, 'inventory_routers.yaml', 'routers')
get_inventory(sql_req_all_switches, cursor, 'inventory_switches.yaml', 'switches')
get_inventory(sql_req_all_nexus, cursor, 'inventory_nexus.yaml', 'nexus')

cursor.close()
conn.close()
