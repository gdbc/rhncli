rhncli
======

Copyright (C) 2013 Graeme David Brooks-Crawford 
< graemedbc at gmail dot com >
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


Summary:

An client/server cli to RHN Satellite's or Spacewalks api using SSO(kerberos) for user authentication and group lookups for authorisation.

General: 

The goals of this project was to collate all the individual scripts scattered around networks and the internet into a single location so that everyone can use, contribute and benefit from the work others have done and have the benefit of leveraging existing company auth mechanisms(SSO(kerberos)/netgroups/groups) for user management instead of RHN Satellite. 

It also provides a cmd line interface into the management of RHN Satellite allowing for the benefits that come with that in being able to script repeatable tasks, sorting data using common tools and not using the web interface or spacecmd which can be intimidating and dangerous to an initiated user or being required to provide authentication details by leveraging SSO.

Secondly RHN Satellite is kind of like a separate authentication island from the rest of a companies usual implemented auth mechanisms and I want this to integrate with a companies current authentication and authorisation policies. 

I wanted initial access to be kerberized and then be checked against a group/netgroup to simply verify if that user is allowed to run that command. This reduces the complexity of user configuration/administration greatly on RHN Satellite and better integrates with a companies existing auth infra. Using apache log facility keeps a nice audit trail of who is running what in apaches access log files.

Thirdly api scripts are generally associated with RHN Satellite user/password credentials, kerberizing the client elleviates this requirement. 

Present command offering:

[user1@client ~]$ rhncli -l

   *** SYSTEM MANAGEMENT ***


Schedule package installs on host to start on first check in from a proposed
time or use "now":
   rhncli -c inpkgs -p <systemname(short)>,<YYYYMMDDTHH:MM | now><comma
separated list of EXPLICIT or GENERIC(defaults to latest) pkg names>
    ie: rhncli -c inpkgs -p
xldn1979nap,20130410T17:00,httpd-2.2.15-15.el6_2.1.x86_64.rpm,gcc,gdbc-241279-1.el6.x86_64.rpm,tomcat

Check scheduled package installs on given host using scheduled time as the
key:
   rhncli -c chksched -p <systemname(short)>,<YYYYMMDDTHH:MM>

List all packages on a given host:
   rhncli -c lsyspkgs -p <systemname(short)>

List hosts subscribed channels:
   rhncli -c lsyschans -p <systemname(short)>

List hosts subscribable channels:
   rhncli -c lsubsyschans -p <systemname(short)>

Change hosts channels:
   rhncli -c csyschans -p <systemname(short)>,<parent>,<child channel>,<child
channel>, ...

List all hosts WITH package installed:
   rhncli -c lsyswpkg -p <EXPLICIT package name ie:
gdbc-241279-1.el6.x86_64.rpm>

List all hosts WITHOUT package installed:
   rhncli -c lsyswopkg -p <EXPLICIT package name ie:
gdbc-241279-1.el6.x86_64.rpm>

List all hosts subscribed to specific channel:
   rhncli -c lsysonchan -p <channel label>


   *** PACKAGE & CHANNEL MANAGEMENT ***


List all RHN Satellite channels:
   rhncli -c lchans

Search for NEWEST available package using GENERIC name AND release OR channel:
   rhncli -c latestpkg -p <generic package name>,5|6|<channel name>

Search for PACKAGES displaying ALL versions and hosting channels:
   rhncli -c psearch -p <generic package name>

List all packages in a given channel:
   rhncli -c lpkgs -p <channel label>

Copy package to channel:
   rhncli -c cp2chan -p <channel label>,<EXPLICIT package name ie:
gdbc-241279-1.el6.x86_64.rpm>

Upload package to channel:
   rhncli -c uppkg -p <channel label>,<EXPLICIT package name ie:
gdbc-241279-1.el6.x86_64.rpm>

Download package:
   rhncli -c downpkg -p <EXPLICIT package name ie:
gdbc-241279-1.el6.x86_64.rpm>

List package description:
   rhncli -c ldesc -p <EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>

List package changelog:
   rhncli -c lclog -p <EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>

List package dependencies:
   rhncli -c ldeps -p <EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>

Remove package from channel:
   rhncli -c rmpkg -p <channel label>,<EXPLICIT package name ie:
gdbc-241279-1.el6.x86_64.rpm>


The Future:

Query multiple RHN Satellite servers transparently allowing an rhncli user to manage systems/packages/channels 
on multiple instances of RHN Satellite without specifying servers individually. 


Installation/Configuration:

Assumptions:

Kerberised environment configured with app principle on rhn api proxy server as /etc/http/http.keytab and 
permissions on it correctly set
An Installed/Configured Satellite Server.
Apache installed on rhn api proxy server.

Client Configuration:
servername:client.example.com
build:rhel6
install python-kerberos and Kenneth Reitz's python-requests and install python-kerberos
Copy rhncli to /usr/local/bin/ on any kerberised client machine.

Open and edit rhncli
Change the server variable to that of the rhnapiproxy server
server="rhnproxy.example.com"

[user1@client ~]$ klist
klist: No credentials cache found (ticket cache FILE:/tmp/krb5cc_500)
[user1@client ~]$ rhncli -l
No credentials cache, please run kinit!
[user1@client ~]$ kinit
Password for user1@EXAMPLE.COM: 
[user1@client ~]$ rhncli -c ingrp
Group is Authorized

Server Configuration:
servername: rhnproxy.example.com
build: rhel6
installmod_auth_kerb, mod_python, rhnpush packages

Copy file_upload.cgi and rhncli.py to /var/www/html/rhnapiproxy/
Edit rhncli.py and add the groups you want to allow access to each function.
This can be done by editing and adding a comma separated list of groups to the variable "authlist"

Create directiories /var/pkgs and  /usr/lib64/python2.6/
Copy krb-api including KrbAuth.py and RHNAPI.py to /usr/lib64/python2.6/
edit /usr/lib64/python2.6/krb-api/RHNAPI.py and change the following to suite your environment:

   #Satellite Server
   SAT1 = "rhnsata.example.com"
   SATELLITE_URL1 = "http://" + SAT1 + "/rpc/api"
   # Satellite user
   SATELLITE_LOGIN1 = "rhnadminuser"
   # Satellite password
   SATELLITE_PASSWORD1 = "password"

Additionally you will need to ed the getLatest function and add the channels that are connected
to RHN Hosted depending on which release you are syncing down you will change or edit this function 
accordingly.
example snippet:
...
      if channel == "5":
         chan1 = "rhel-x86_64-server-5"
         chan2 = "rhn-tools-rhel-x86_64-server-5"
         chan3 = "rhel-x86_64-server-cluster-storage-5"
         chan4 = "rhel-x86_64-server-cluster-5"
...
      elif channel == "6":
         chan1 = "rhel-x86_64-server-6"
         chan2 = "rhel-x86_64-server-supplementary-6"
         chan3 = "rhel-x86_64-server-optional-6"
         chan4 = "rhn-tools-rhel-x86_64-server-6"
         chan5 = "rhel-x86_64-server-6-debuginfo"
...


Add the following to http configuration file:

<Directory /var/www/html/rhnapiproxy/>
 DAV On
 AuthType Kerberos
 AuthName "Restricted Access"
 KrbMethodNegotiate On
 KrbMethodK5Passwd Off
 KrbLocalUserMapping On
 Krb5Keytab /etc/httpd/http.keytab
 KrbAuthRealms EXAMPLE.COM
 KrbServiceName HTTP/rhnproxy.example.com
  <Limit PUT POST>
        Require valid-user
  </Limit>
 Require group api
 require valid-user
 Options Indexes FollowSymLinks MultiViews
 AllowOverride None
 Order allow,deny
 allow from all
 AddHandler cgi-script .cgi
 Options +ExecCGI
 AddHandler mod_python .py
 PythonHandler mod_python.publisher
 PythonDebug On
</Directory>

Change  KrbAuthRealms to include your kerberos realm
and KrbServiceName to your http application principle
Change Krb5Keytab to point to your http keytab file.

restart apache

Apologies:

The code in its current form is quite raw, when I have time I'll clean it up and so can you :D. 
It was initially a function over form driven project done on some leave I had and put together rather quickly. 
