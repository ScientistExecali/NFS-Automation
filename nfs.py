#!/usr/bin/python36

import subprocess as sp
import os
import cgi

print("content-type:text/html")
print("\n")

form=cgi.FieldStorage()
node=form.getvalue('node')
sip=form.getvalue('sip')
cip=form.getvalue('cip')
spw=form.getvalue('spw')
cpw=form.getvalue('cpw')

#NFS Server

if node=="Server":
	sp.getoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} mkdir /nfsdata".format(spw,sip))
	sp.getoutput("sshpass -p {} scp -o StrictHostKeyChecking=no /var/www/cgi-bin/exports.py root@{}:/root/ ".format(spw,sip))
	sp.getoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} python /root/exports.py".format(spw,sip))
	sp.getoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} systemctl restart nfs".format(spw,sip))
	sp.getoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} systemctl enable nfs".format(spw,sip))
	x=sp.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} exportfs -v".format(spw,sip))
	if x[0]==0:
		print("Server has been setup")
	else:
		print("Server setup failed")

#NFS Client

elif node=="Client":
	sp.getoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} mkdir /nfsdata".format(cpw,cip))
	x=sp.getstatusoutput("sshpass -p {} ssh -o StrictHostKeyChecking=no -l root {} mount {}:/nfsdata /nfsdata".format(cpw,cip,sip))
	if x[0]==0:
		print("Client has been setup")
	else:
		print("Client setup failed")

else:
	print("Incorrect node type")
