# CiscoShowToXLS
This python script connects to hosts specified in the "devices" file using Paramiko and performs a "show flash | i bytes".
It then captures available and total bytes and adds data to the "xlwt example.xls" file (it creates it if it doesn't exist).

