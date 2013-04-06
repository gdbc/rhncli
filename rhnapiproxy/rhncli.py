import sys
import mod_python
from mod_python import apache
sys.path.append("/usr/lib64/python2.6/krb-api/")
from KrbAuth import KAuth
from RHNAPI import RHNApi

#    
#    Copyright (C) 2013 Graeme David Brooks-Crawford 
#    < graemedbc at gmail dot com >
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


### Global vars ###

noAuth="\nError: Not in Authorized Group!\n"
noVars="\nError: Not enough variables!\n"


### Connectivity test code ### 

def index(req):
   return req.user

def testVars(req):
   V={}
   form = mod_python.util.FieldStorage(req)
   for i in form.keys():
      V[i] = form[i].value
   return V


### Check if user is in group ###

def ingrp(req):
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ## 
      return "Group is Authorized"
   else:
      return "ACCESS DENIED, user not in group" 



######### SHIT GETS REAL FROM HERE  ##########


### List all functions and how to use them ###

###%%%% NEED TO LIST WHAT FUNCTIONS A USER HAS ACCESS TO DYNAMICALLY %%%%### 

def help(req):
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:

   ## Run function ##

      l = ["\n   *** SYSTEM MANAGEMENT ***\n\n",
         "Schedule package installs on host to start on first check in from a proposed time or use \"now\":\n   rhncli -c inpkgs -p <systemname(short)>,<YYYYMMDDTHH:MM | now><comma separated list of EXPLICIT or GENERIC(defaults to latest) pkg names>\n    ie: rhncli -c inpkgs -p xldn1979nap,20130410T17:00,httpd-2.2.15-15.el6_2.1.x86_64.rpm,gcc,gdbc-241279-1.el6.x86_64.rpm,tomcat\n",
         "Check scheduled package installs on given host using scheduled time as the key:\n   rhncli -c chksched -p <systemname(short)>,<YYYYMMDDTHH:MM>\n",
         "List all packages on a given host:\n   rhncli -c lsyspkgs -p <systemname(short)>\n",
         "List hosts subscribed channels:\n   rhncli -c lsyschans -p <systemname(short)>\n",
         "List hosts subscribable channels:\n   rhncli -c lsubsyschans -p <systemname(short)>\n",
         "Change hosts channels:\n   rhncli -c csyschans -p <systemname(short)>,<parent>,<child channel>,<child channel>, ...\n",       
         "List all hosts WITH package installed:\n   rhncli -c lsyswpkg -p <EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>\n",
         "List all hosts WITHOUT package installed:\n   rhncli -c lsyswopkg -p <EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>\n",
         "List all hosts subscribed to specific channel:\n   rhncli -c lsysonchan -p <channel label>\n",
     	 "\n   *** PACKAGE & CHANNEL MANAGEMENT ***\n\n",
     	 "List all RHN Satellite channels:\n   rhncli -c lchans\n",
         "Search for NEWEST available package using GENERIC name AND release OR channel:\n   rhncli -c latestpkg -p <generic package name>,5|6|<channel name>\n",
         "Search for PACKAGES displaying ALL versions and hosting channels:\n   rhncli -c psearch -p <generic package name>\n",
         "List all packages in a given channel:\n   rhncli -c lpkgs -p <channel label>\n",
         "Copy package to channel:\n   rhncli -c cp2chan -p <channel label>,<EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>\n",
         "Upload package to channel:\n   rhncli -c uppkg -p <channel label>,<EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>\n",
         "Download package:\n   rhncli -c downpkg -p <EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>\n",
         "List package description:\n   rhncli -c ldesc -p <EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>\n",
         "List package changelog:\n   rhncli -c lclog -p <EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>\n",
         "List package dependencies:\n   rhncli -c ldeps -p <EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>\n",
         "Remove package from channel:\n   rhncli -c rmpkg -p <channel label>,<EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>\n",
        ]
      return "\n".join(l)
   else:
      return noAuth 



### List all channels for current system ###

def lsyschans(req,opt0=""):
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      if str(opt0) != "None":
         try:
            return RHNApi().getSysChans(opt0) 
         except Exception as e:
            return "Error: listsyschans, use the the right hostname?"
      else:
         return noVars 
   else:
      return noAuth 



### List subscribable channels for current system ###

def lsubsyschans(req,opt0=""):
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      if str(opt0) != "None":
         try:
            return RHNApi().getSubSysChans(opt0) 
         except Exception as e:
            return "Error: listsubsyschans"
      else:
         return noVars 
   else:
      return noAuth 



### Change system channels ###

def csyschans(req):
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      V={}
      form = mod_python.util.FieldStorage(req)
      for i in form.keys():
         V[i] = form[i].value
      try:
         return RHNApi().changeSysChans(V)
      except Exception as e:
         return "Error: changesyschans, check you can subscribe to those channels(lsubsyschans) and try not using spaces before and after commas!"
   else:
      return noAuth 



### List Channels ###

def lchans(req):
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      try:
         return RHNApi().getChans() 
      except Exception as e:
         return "Error: lchans"
   else:
      return noAuth 



### List Systems subscribed to channel ###

def lsysonchan(req,opt0=""):
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      if str(opt0) != "None":
         try:
            return RHNApi().getSystems(opt0)
         except Exception as e:
            return "Error: lsyswpkg"
      else:
         return noVars
   else:
      return noAuth



#### PKGS ####


### Search for pkg and show related channels ###

def psearch(req,opt0=""):
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      if str(opt0) != "None":
         try: 
            return RHNApi().getPkgChans(opt0) 
         except Exception as e:
            return "Error: psearch"
      else:
         return noVars 
   else:
      return noAuth 



### List systems with package ###

def lsyswpkg(req,opt0=""):
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      if str(opt0) != "None":
         try:
            return RHNApi().getSysWPkg(opt0) 
         except Exception as e:
            return "Error: lsyswpkg"
      else:
         return noVars 
   else:
      return noAuth 



### List systems without package ###

def lsyswopkg(req,opt0=""):
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      if str(opt0) != "None":
         try:
            return RHNApi().getSysWOPkg(opt0) 
         except Exception as e:
           return "Error: lsyswopkg"
      else:
         return noVars 
   else:
      return noAuth 



### List all packages in a channel ###

def lpkgs(req,opt0=""):
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      if str(opt0) != "None":
         try:
            return RHNApi().getPkgs(opt0) 
         except Exception as e:
            return "Error: lpkgs"
      else:
         return noVars 
   else:
      return noAuth 



### List all packages on a client ###

def lsyspkgs(req,opt0=""):
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      if str(opt0) != "None":
         try:
            return RHNApi().getHPkgs(opt0) 
         except Exception as e:
            return "Error: lsyspkgs"
      else:
         return noVars 
   else:
      return noAuth 



### List package changelog ###

def lclog(req,opt0=""):
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      if str(opt0) != "None":
         try:  
            return RHNApi().getChangeLog(opt0) 
         except Exception as e:
            return "Error: lclog"
      else:
         return noVars 
   else:
      return noAuth 



### List package deps ###

def ldeps(req,opt0=""):
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      if str(opt0) != "None":
         try: 
            return RHNApi().getDeps(opt0) 
         except Exception as e:
            return "Error: ldeps"
      else:
         return noVars 
   else:
      return noAuth 



### List package description ###

def ldesc(req,opt0=""):
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      if str(opt0) != "None":
         try:
            return RHNApi().getDesc(opt0) 
         except Exception as e:
            return "Error: ldesc"
      else:
         return noVars 
   else:
      return noAuth 



### Search for latest pkg for given release ###

def latestpkg(req):
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      V={}
      form = mod_python.util.FieldStorage(req)
      for i in form.keys():
         V[i] = form[i].value
      #try:
      return RHNApi().getLatest(V)
     # except Exception as e:
     #    return "Error: latestpkg"
   else:
     return noAuth 



### Copy package to a channel ###

def cp2chan(req,opt0=""):
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      V={}
      form = mod_python.util.FieldStorage(req)
      for i in form.keys():
         V[i] = form[i].value
      try:
         return RHNApi().cpPkg(V)
      except Exception as e:
         return "Error: cppkg2chan"
   else:
      return noAuth



### Remove a package to a channel ###

def rmpkg(req,opt0=""):
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      V={}
      form = mod_python.util.FieldStorage(req)
      for i in form.keys():
         V[i] = form[i].value
      try:
         return RHNApi().rmPkg(V)
      except Exception as e:
         return "Error: rmpkg"
   else:
      return noAuth



### Upload RPMs ###

def uppkg(req): 
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      V={}
      form = mod_python.util.FieldStorage(req)
      for i in form.keys():
         V[i] = form[i].value
      try:
         return RHNApi().uploadRPM(V)
      except Exception as e:
         return "Error: uploadrpm ... also avoid spaces after comma's"
   else:
      return noAuth 



### Download RPMs ###

def downpkg(req,opt0=""):
   ## Auth Check ##
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      if str(opt0) != "None":
         try:
            return RHNApi().getPkgUrl(opt0) 
         except Exception as e:
            return "Error: downloadrpm"
      else:
         return noVars 
   else:
      return noAuth 



### Schedule rpm install ###

def inpkgs(req):
   ## Auth Check ##
   #authlist=['rhnadmins']
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      V={}
      form = mod_python.util.FieldStorage(req)
      for i in form.keys():
         V[i] = form[i].value
      try:
         return RHNApi().inPkg(V)
      except Exception as e:
         return "Error: inspkg"
   else:
      return noAuth 



### Schedule rpm install ###

def chksched(req):
   ## Auth Check ##
   #authlist=['rhnadmins']
   authlist=['rhnadmins']
   gcheck = KAuth().grpcheck(authlist,req.user)
   if gcheck:
   ## Run function ##
      V={}
      form = mod_python.util.FieldStorage(req)
      for i in form.keys():
         V[i] = form[i].value
      #try:
      return RHNApi().chkSched(V)
      #except Exception as e:
      #   return "Error: chksched"
   else:
      return noAuth 
