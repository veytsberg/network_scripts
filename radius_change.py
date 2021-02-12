from netmiko import ConnectHandler
from getpass import getpass
import time
from netmiko import ConnectHandler

def test_connection(main_connection, logfile):
    with ConnectHandler(**device) as test_conn:
        test_conn.enable()
        test_out = test_conn.send_command('sh radius server-group all')
        logfile.write(f'{test_out}\n')
        main_connection.disconnect()
        return test_out

def radius_change(ip_file, new_cfg_file, rollback_file):
    with open(ip_file) as f:
        for item in f:
            ip = item.strip()
            print(ip)
            device = {
                "device_type": "cisco_ios",
                "host": ip,
                "username": name,
                "password": passwd,
                "secret": secret,
            }
            net_connect = ConnectHandler(**device)
            net_connect.enable()
            output = net_connect.send_config_from_file(config_file=new_cfg_file)
            print(output)
            with open('output_log.log', 'a') as log:
                log.write(f'{output}\n')
                try:
                    print(test_connection(net_connect, log))
                except:
                    rollback = net_connect.send_config_from_file(config_file=rollback_file)
                    print(rollback)
                    log.write(f'{rollback}\n')
                    print(test_connection(net_connect, log))
