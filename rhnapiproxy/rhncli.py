import sys
import mod_python
from mod_python import apache
sys.path.append("/usr/lib64/python2.6/krb-api/")
from KrbAuth import KAuth
from RHNAPI import RHNApi

#    
#    Copyright (C) 2013 Graeme David Brooks-Crawford < graemedbc at gmail dot com >
#    Copyright (C) 2013 Chris Procter < chris-procter at talk21 dot com >
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

perms={ 'help': ['rhnadmins'],
   'ingrp': ['rhnadmins'],
   'inpkgs': ['rhnadmins'],
   'chksched': ['rhnadmins'],
   'lsyspkgs': ['rhnadmins'],
   'lsyschans': ['rhnadmins'],
   'lsubsyschans': ['rhnadmins'],
   'csyschans': ['rhnadmins'],
   'lsyswpkg': ['rhnadmins'],
   'lsyswopkg': ['rhnadmins'],
   'lsysonchan': ['rhnadmins'],
   'lchans': ['rhnadmins'],
   'latestpkg': ['rhnadmins'],
   'psearch': ['rhnadmins'],
   'lpkgs': ['rhnadmins'],
   'cp2chan': ['rhnadmins'],
   'uppkg': ['rhnadmins'],
   'downpkg': ['rhnadmins'],
   'ldeps': ['rhnadmins'],
   'lclog': ['rhnadmins'],
   'ldesc': ['rhnadmins'],
   'rmpkg': ['rhnadmins'],
}

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
   '''check if user is in group\n rhncli -c ingrp'''
   ## Auth Check ##
   if KAuth().grpcheck(perms['ingrp'],req.user):
   ## Run function ## 
      return "Group is Authorized"
   else:
      return "ACCESS DENIED, user not in group" 



######### SHIT GETS REAL FROM HERE  ##########


### List all functions and how to use them ###

def help(req):
   ''' display help:\n rhncli -c help or rhncli -l'''
   ## Auth Check ##
   if KAuth().grpcheck(perms['help'],req.user):
      grplist=KAuth().getgrplist(req.user)
      l=dict()
      for f in perms.keys():
         if set(perms[f]).intersection(grplist) :
            try:
               (section,text)=globals()[f].__doc__.split('|',1)
            except:
               section = "Misc"
               text = globals()[f].__doc__

            if not l.get(section) :
               l[section] = "\n   *** %s ***\n\n"%section

            l[section] = "%s%s: %s\n\n"%(l[section],f,text)

      return "\n".join(l.values())
   else:
      return noAuth 



### List all channels for current system ###

def lsyschans(req,opt0=""):
   '''SYSTEM MANAGEMENT| List hosts subscribed channels:\n   rhncli -c lsyschans -p <systemname(short)>'''

   if KAuth().grpcheck(perms['lsyschans'],req.user):
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
   '''SYSTEM MANAGEMENT| List hosts subscribable channels:\n   rhncli -c lsubsyschans -p <systemname(short)>'''

   if KAuth().grpcheck(perms['lsubsyschans'],req.user):
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
   '''SYSTEM MANAGEMENT| Change hosts channels:\n   rhncli -c csyschans -p <systemname(short)>,<parent>,<child channel>,<child channel>, ...'''

   if KAuth().grpcheck(perms['csyschans'],req.user):
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
   '''PACKAGE & CHANNEL MANAGEMENT| List all RHN Satellite channels:\n   rhncli -c lchans'''

   if KAuth().grpcheck(perms['lchans'],req.user):
   ## Run function ##
      try:
         return RHNApi().getChans() 
      except Exception as e:
         return "Error: lchans"
   else:
      return noAuth 



### List Systems subscribed to channel ###

def lsysonchan(req,opt0=""):
   '''SYSTEM MANAGEMENT| List all hosts subscribed to specific channel:\n   rhncli -c lsysonchan -p <channel label>'''

   if KAuth().grpcheck(perms['lsysonchan'],req.user):
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
   '''PACKAGE & CHANNEL MANAGEMENT| Search for PACKAGES displaying ALL versions and hosting channels:\n   rhncli -c psearch -p <generic package name>'''
   
   if KAuth().grpcheck(perms['psearch'],req.user):
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
   '''SYSTEM MANAGEMENT| List all hosts WITH package installed:\n   rhncli -c lsyswpkg -p <EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>'''

   if KAuth().grpcheck(perms['lsyswpkg'],req.user):
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
   '''SYSTEM MANAGEMENT| List all hosts WITHOUT package installed:\n   rhncli -c lsyswopkg -p <EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>'''

   if KAuth().grpcheck(perms['lsyswopkg'],req.user):
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
   '''PACKAGE & CHANNEL MANAGEMENT| List all packages in a given channel:\n   rhncli -c lpkgs -p <channel label>'''

   if KAuth().grpcheck(perms['lpkgs'],req.user):
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
   '''SYSTEM MANAGEMENT| List all packages on a given host:\n   rhncli -c lsyspkgs -p <systemname(short)>'''

   if KAuth().grpcheck(perms['lsyspkgs'],req.user):
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
   '''PACKAGE & CHANNEL MANAGEMENT| List package changelog:\n   rhncli -c lclog -p <EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>'''

   if KAuth().grpcheck(perms['lclog'],req.user):
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
   '''PACKAGE & CHANNEL MANAGEMENT| List package dependencies:\n   rhncli -c ldeps -p <EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>'''

   if KAuth().grpcheck(perms['ldeps'],req.user):
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
   '''PACKAGE & CHANNEL MANAGEMENT| List package description:\n   rhncli -c ldesc -p <EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>'''

   if KAuth().grpcheck(perms['ldesc'],req.user):
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
   '''PACKAGE & CHANNEL MANAGEMENT| Search for NEWEST available package using GENERIC name AND release OR channel:\n   rhncli -c latestpkg -p <generic package name>,5|6|<channel name>'''

   if KAuth().grpcheck(perms['latestpkg'],req.user):
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
   '''PACKAGE & CHANNEL MANAGEMENT| Copy package to channel:\n   rhncli -c cp2chan -p <channel label>,<EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>'''

   if KAuth().grpcheck(perms['cp2chan'],req.user):
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
   '''PACKAGE & CHANNEL MANAGEMENT| Remove package from channel:\n   rhncli -c rmpkg -p <channel label>,<EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>'''

   if KAuth().grpcheck(perms['rmpkg'],req.user):
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
   '''PACKAGE & CHANNEL MANAGEMENT| Upload package to channel:\n   rhncli -c uppkg -p <channel label>,<EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>'''

   if KAuth().grpcheck(perms['uppkg'],req.user):
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
   '''PACKAGE & CHANNEL MANAGEMENT| Download package:\n   rhncli -c downpkg -p <EXPLICIT package name ie: gdbc-241279-1.el6.x86_64.rpm>'''

   if KAuth().grpcheck(perms['downpkg'],req.user):
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
   '''SYSTEM MANAGEMENT| Schedule package installs on host to start on first check in from a proposed time or use \"now\":\n   rhncli -c inpkgs -p <systemname(short)>,<YYYYMMDDTHH:MM | now><comma separated list of EXPLICIT or GENERIC(defaults to latest) pkg names>\n    ie: rhncli -c inpkgs -p xldn1979nap,20130410T17:00,httpd-2.2.15-15.el6_2.1.x86_64.rpm,gcc,gdbc-241279-1.el6.x86_64.rpm,tomcat'''

   if KAuth().grpcheck(perms['inpkgs'],req.user):
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
   '''SYSTEM MANAGEMENT| Check scheduled package installs on given host using scheduled time as the key:\n   rhncli -c chksched -p <systemname(short)>,<YYYYMMDDTHH:MM>'''
   if KAuth().grpcheck(perms['chksched'],req.user):
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
