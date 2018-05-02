import getpass
import paramiko
import time
from xlwt import Workbook



USER = raw_input("Enter your username: ")
PASSWD = getpass.getpass()



def disable_paging(remote_conn):
    '''Disable paging on a Cisco router'''

    remote_conn.send("terminal length 0\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output

wb = Workbook()
sheet1 = wb.add_sheet('Flash Space')

#if __name__ == '__main__':
def main():

    # VARIABLES THAT NEED CHANGED
    ip = IPADDR
    username = USER
    password = PASSWD

    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())

    # initiate SSH connection
    remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
    print "SSH connection established to %s" % ip

    # Use invoke_shell to establish an 'interactive session'
    remote_conn = remote_conn_pre.invoke_shell()
    print "Interactive SSH session established"

    # Strip the initial router prompt
    output = remote_conn.recv(1000)

    # See what we have
    print output

    # Turn off paging
    disable_paging(remote_conn)

    # Now let's try to send the router a command
    remote_conn.send("\n")
    remote_conn.send("show flash | i bytes\n")

    # Wait for the command to complete
    time.sleep(2)
    
    output = remote_conn.recv(5000)
    print output

    for each_line in output.splitlines():
        if "bytes total" in each_line:    	       	
            AS = each_line.split()[-3]
            TS = each_line.split()[0]
            print AS[1:] + " available space from a total of: " + TS
            sheet1.write(n,0,IPADDR)
            sheet1.write(n,1,AS[1:])
            sheet1.write(n,2,TS)

sheet1.write(0,0,"IP Address")
sheet1.write(0,1,"Available")
sheet1.write(0,2,"Total")

n = 1

with open('devices') as f:
	for each_line in f.read().splitlines():
		IPADDR = str(each_line)
		n = n + 1
		main()

wb.save('xlwt example.xls')
