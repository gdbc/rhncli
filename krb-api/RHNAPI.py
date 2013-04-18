import os
import time
import xmlrpclib
from datetime import datetime

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



def getKey():
   SAT1 = "<satellite server>"
   SATELLITE_URL1 = "http://" + SAT1 + "/rpc/api"
   SATELLITE_LOGIN1 = "<sat username>"
   SATELLITE_PASSWORD1 = "<password>"
   client1 = xmlrpclib.Server(SATELLITE_URL1, verbose=0)
   key = client1.auth.login(SATELLITE_LOGIN1, SATELLITE_PASSWORD1)
   return key,client1


def getDate(dateAndTime):
   currentime = xmlrpclib.DateTime(time.strftime("%Y%m%dT%H:%M:%S",time.localtime(time.time())))
   if str(dateAndTime).strip() == "now":
      dateAndTime = xmlrpclib.DateTime(time.strftime("%Y%m%dT%H:%M:%S",time.localtime(time.time()+60)))
   else:
      schedTime = str(dateAndTime) + ":00"
   try:
      if currentime.__lt__(schedTime):
         return xmlrpclib.DateTime(schedTime)
      else: 
         return "timefsck"
   except Exception as e:
      return "timefsck"
   

   
class RHNApi:


   def getSysChans(self, systemname):
      key1, client1 = getKey()
      getId = client1.system.getId(key1,systemname)[0]['id']
      baseChan = client1.system.getSubscribedBaseChannel(key1,getId)['label']
      childChans = client1.system.listSubscribedChildChannels(key1,getId)
      chans = "p: " + baseChan + "\n"
      for i in childChans:
	chans = chans + "  c: " + i['label'] + "\n"
      return chans.strip()


   def getSubSysChans(self, systemname):
      key1, client1 = getKey()
      chans=""
      getId = client1.system.getId(key1,systemname)[0]['id']
      childChans = client1.system.listSubscribableChildChannels(key1,getId)
      for i in childChans:
	chans = chans + "c: " + i['label'] + "\n"
      return chans.strip()


   def getPkgChans(self, pkgname):
      key1, client1 = getKey()
      pkglist = ""
      pkg_sub = pkgname
      package = client1.packages.search.name(key1,pkg_sub)	
      for i in package:
         x = i['name'] + "-" + i['version'] + "-" + i['release'] + "." + i['arch'] + ".rpm"
         if pkgname in x:
            pkglist = pkglist + "%s\nchannels: \n" %(x)
            chans = client1.packages.listProvidingChannels(key1,int(i['id']))
            for chan in chans:
               pkglist = pkglist + chan['label'] + "\n"
            pkglist = pkglist + "\n"
            pkglist = pkglist[:-1] + "\n"
      return pkglist[:-1]


   def getPkgs(self, channame):
      key1, client1 = getKey()
      pkglist = ""
      packages = client1.channel.software.listAllPackages(key1,channame)	
      if packages:
         for i in packages:
            x = i['name'] + "-" + i['version'] + "-" + i['release'] + "." + i['arch_label'] + ".rpm"
            pkglist = pkglist + "%s\n" %(x)
         return pkglist[:-1]
      else:
         return "Fail"


   def getSystems(self, channame):
      key1, client1 = getKey()
      syslist = ""
      systems = client1.channel.software.listSubscribedSystems(key1,channame)
      if systems:
         for i in systems:
            x = i['name']
            syslist = syslist + "%s\n" %(x)
         return syslist[:-1]
      else:
         return "Failed: incorrect channel name, maybe, mmm?"


   def diffSysPkgs(self,systemname1,systemname2):
      key1, client1 = self.__getKey__()
      systemname1=str(sys['opt0']).strip()
      systemname2=str(sys['opt1']).strip()
      p1 = [] 
      p2 = [] 
      getId1 = client1.system.getId(key1,systemname1)[0]['id']
      packages1 = client1.system.listPackages(key1,getId1)	
      getId2 = client1.system.getId(key1,systemname2)[0]['id']
      packages2 = client1.system.listPackages(key1,getId2)	

      for i in packages1:
         p1.append("%s-%s-%s.%s.rpm"%(i['name'], i['version'],i['release'], i['arch'])

      for i in packages2:
         p2.append("%s-%s-%s.%s.rpm" %(i['name'], i['version'],i['release'], i['arch']))

      pkglist=[a for a in p1 if a not in p2]

      if pkglist:
         return "\n".join(pkglist[:-1])
      else:
         return "Fail"


   def getHPkgs(self, systemname):
      key1, client1 = getKey()
      pkglist = ""
      getId = client1.system.getId(key1,systemname)[0]['id']
      packages = client1.system.listPackages(key1,getId)	
      for i in packages:
         x = i['name'] + "-" + i['version'] + "-" + i['release'] + "." + i['arch'] + ".rpm"
         pkglist = pkglist + "%s\n" %(x)
      if pkglist:
         return pkglist[:-1]
      else:
         return "Fail"


   def getLatest(self,PkgAndChans):
      key1, client1 = getKey()
      chans=[]
      name=str(PkgAndChans['opt0']).strip()
      channel=str(PkgAndChans['opt1']).strip()
      if channel == "5":
         chan1 = "rhel-x86_64-server-5" 
         chan2 = "rhn-tools-rhel-x86_64-server-5" 
         chan3 = "rhel-x86_64-server-cluster-storage-5" 
         chan4 = "rhel-x86_64-server-cluster-5" 
         latest_packages1 = client1.channel.software.listLatestPackages(key1,chan1)
         latest_packages2 = client1.channel.software.listLatestPackages(key1,chan2)
         latest_packages3 = client1.channel.software.listLatestPackages(key1,chan3)
         latest_packages4 = client1.channel.software.listLatestPackages(key1,chan4)
         for lists in latest_packages1, latest_packages2, latest_packages3, latest_packages4:
            for i in lists:
               x = i['name'] + "-" + i['version'] + "-" + i['release'] + "." + i['arch_label'] + ".rpm"
               if name == str(i['name']).strip():  
                  return x
      elif channel == "6":
         chan1 = "rhel-x86_64-server-6" 
         chan2 = "rhel-x86_64-server-supplementary-6"
         chan3 = "rhel-x86_64-server-optional-6"
         chan4 = "rhn-tools-rhel-x86_64-server-6"
         chan5 = "rhel-x86_64-server-6-debuginfo"
         latest_packages1 = client1.channel.software.listLatestPackages(key1,chan1)
         latest_packages2 = client1.channel.software.listLatestPackages(key1,chan2)
         latest_packages3 = client1.channel.software.listLatestPackages(key1,chan3)
         latest_packages4 = client1.channel.software.listLatestPackages(key1,chan4)
         latest_packages5 = client1.channel.software.listLatestPackages(key1,chan5)
         for lists in latest_packages1, latest_packages2, latest_packages3, latest_packages4, latest_packages5:
            for i in lists:
               x = i['name'] + "-" + i['version'] + "-" + i['release'] + "." + i['arch_label'] + ".rpm"
               if name == str(i['name']).strip():  
                  return x
      elif len(channel) > 1:
         latest_packages = client1.channel.software.listLatestPackages(key1,channel)
      for i in latest_packages:
         x = i['name'] + "-" + i['version'] + "-" + i['release'] + "." + i['arch_label'] + ".rpm"
         if name == str(i['name']).strip():  
            return x
      return "No package by that name found in channels, maybe channel not added to search list!"
      

   def changeSysChans(self,SysAndChans):
      key1, client1 = getKey()
      chans=[]
      getId = client1.system.getId(key1,SysAndChans['opt0'])[0]['id']
      del SysAndChans['opt0']
      client1.system.setBaseChannel(key1,getId,SysAndChans['opt1'])
      del SysAndChans['opt1']
      for i in SysAndChans:
         chans.append(SysAndChans[i]) 
      client1.system.setChildChannels(key1,getId,chans)
      return "Done"


   def getChans(self):
      key1, client1 = getKey()
      getChans = client1.channel.listAllChannels(key1)
      parents = {}
      cList = []
      outpkgs = ""
      for i in getChans:
         children = client1.channel.software.listChildren(key1,i['label'])
         if children:
            for child in children:
               cList.append(child['label'])
            parents[i['label']] = cList
            cList = []

      for parent in parents:
         outpkgs = outpkgs + "p: %s" %(parent)
         for c in parents[parent]:
            outpkgs = outpkgs + "\n  c: %s" %c
         outpkgs = outpkgs + "\n"
      return outpkgs[:-1]


   def uploadRPM(self,chanPKG):
      key1, client1 = getKey()
      passfail=""
      path = "/var/pkgs/"
      channel = chanPKG['opt0']
      pkg = chanPKG['opt1'].split('/')[-1]
      if os.system("/usr/bin/rhnpush --nosig --no-cache -c %s -u %s -p %s --server=%s %s%s" %(str(channel), str(SATELLITE_LOGIN1), str(SATELLITE_PASSWORD1), SAT1, str(path).strip(), str(pkg).strip())) != 0:
         passfail = "Package upload failed, check if there isn't an existing package already!"
      else:
         passfail = "Package uploaded, repo cache regeneration will take a few minutes!"
         os.system("rm -rf %s%s" %(str(path).strip(),str(pkg).strip()))
      return passfail 
       

   def cpPkg(self, pkgChan):
      key1, client1 = getKey()
      pkgname = pkgChan['opt1']
      channame = pkgChan['opt0']
      pkgurl = "Fail"
      pkg_name = "-".join(pkgname.split('-')[:-2])
      pkg_ver  = pkgname.split('-')[-2:][0]
      pkg_rel  = ".".join(pkgname.split('-')[-1].split('.')[:-2])
      srch = "name:%s AND version:%s AND release:%s" %(pkg_name,pkg_ver,pkg_rel)
      package = client1.packages.search.advanced(key1,srch)	
      for i in package:
         x = i['name'] + "-" + i['version'] + "-" + i['release'] + "." + i['arch'] + ".rpm"
         if str(pkgname).strip() == str(x).strip():
            if client1.channel.software.addPackages(key1,channame,i['id']):
	       client1.channel.software.regenerateNeededCache(key1,channame)
               return "Package copied!"
            else:
	       return "Package copy failed!"

   def rmPkg(self, pkgChan):
      key1, client1 = getKey()
      channame = pkgChan['opt0']
      pkgname = pkgChan['opt1']
      pkgurl = "Fail"
      pkg_name = "-".join(pkgname.split('-')[:-2])
      pkg_ver  = pkgname.split('-')[-2:][0]
      pkg_rel  = ".".join(pkgname.split('-')[-1].split('.')[:-2])
      srch = "name:%s AND version:%s AND release:%s" %(pkg_name,pkg_ver,pkg_rel)
      package = client1.packages.search.advanced(key1,srch)	
      for i in package:
         x = i['name'] + "-" + i['version'] + "-" + i['release'] + "." + i['arch'] + ".rpm"
         if str(pkgname).strip() == str(x).strip():
            if client1.channel.software.removePackages(key1,channame,i['id']):
               return "Package removed!"
            else:
	       return "Package remove failed!"


   def getDeps(self, pkgname):
      key1, client1 = getKey()
      output = ""
      pkgurl = "Failed"
      pkg_name = "-".join(pkgname.split('-')[:-2])
      pkg_ver  = pkgname.split('-')[-2:][0]
      pkg_rel  = ".".join(pkgname.split('-')[-1].split('.')[:-2])
      srch = "name:%s AND version:%s AND release:%s" %(pkg_name,pkg_ver,pkg_rel)
      package = client1.packages.search.advanced(key1,srch)	
      for i in package:
         x = i['name'] + "-" + i['version'] + "-" + i['release'] + "." + i['arch'] + ".rpm"
         if str(pkgname).strip() == str(x).strip():
            pkgurl = client1.packages.listDependencies(key1,i['id'])
	    for x in pkgurl:
               if x['dependency_type'] == "requires":
                  output = output + x['dependency'] + " " + x['dependency_modifier'] + "\n"
            return output[:-1]
      return pkgurl 

   def getChangeLog(self, pkgname):
      key1, client1 = getKey()
      clog=""
      pkgurl = "Failed"
      pkg_name = "-".join(pkgname.split('-')[:-2])
      pkg_ver  = pkgname.split('-')[-2:][0]
      pkg_rel  = ".".join(pkgname.split('-')[-1].split('.')[:-2])
      srch = "name:%s AND version:%s AND release:%s" %(pkg_name,pkg_ver,pkg_rel)
      package = client1.packages.search.advanced(key1,srch)	
      for i in package:
         x = i['name'] + "-" + i['version'] + "-" + i['release'] + "." + i['arch'] + ".rpm"
         if str(pkgname).strip() == str(x).strip():
            pkgurl = client1.packages.listChangelog(key1,i['id'])
      for z in pkgurl:
         clog = clog + "\n" + z['date'] + " " + z['author'] + "\n\n" + z['text'] + "\n"
      return clog 

   def getDesc(self, pkgname):
      key1, client1 = getKey()
      pkgurl = "Failed"
      pkg_name = "-".join(pkgname.split('-')[:-2])
      pkg_ver  = pkgname.split('-')[-2:][0]
      pkg_rel  = ".".join(pkgname.split('-')[-1].split('.')[:-2])
      srch = "name:%s AND version:%s AND release:%s" %(pkg_name,pkg_ver,pkg_rel)
      package = client1.packages.search.advanced(key1,srch)	
      for i in package:
         x = i['name'] + "-" + i['version'] + "-" + i['release'] + "." + i['arch'] + ".rpm"
         if str(pkgname).strip() == str(x).strip():
            pkgurl = client1.packages.getDetails(key1,i['id'])
            return pkgurl['description'][:-2]
      return pkgurl 

   def getPkgUrl(self, pkgname):
      key1, client1 = getKey()
      pkgurl = "Failed"
      pkg_name = "-".join(pkgname.split('-')[:-2])
      pkg_ver  = pkgname.split('-')[-2:][0]
      pkg_rel  = ".".join(pkgname.split('-')[-1].split('.')[:-2])
      srch = "name:%s AND version:%s AND release:%s" %(pkg_name,pkg_ver,pkg_rel)
      package = client1.packages.search.advanced(key1,srch)	
      for i in package:
         x = i['name'] + "-" + i['version'] + "-" + i['release'] + "." + i['arch'] + ".rpm"
         if str(pkgname).strip() == str(x).strip():
            pkgurl = client1.packages.getPackageUrl(key1,i['id'])
            return pkgurl
      return pkgurl 

   def getSysWPkg(self, pkgname):
      key1, client1 = getKey()
      output = ""
      pkg_name = "-".join(pkgname.split('-')[:-2])
      pkg_ver  = pkgname.split('-')[-2:][0]
      pkg_rel  = ".".join(pkgname.split('-')[-1].split('.')[:-2])
      srch = "name:%s AND version:%s AND release:%s" %(pkg_name,pkg_ver,pkg_rel)
      package = client1.packages.search.advanced(key1,srch)	
      for i in package:
         x = i['name'] + "-" + i['version'] + "-" + i['release'] + "." + i['arch'] + ".rpm"
         if str(pkgname).strip() == str(x).strip():
            syswithpkg = client1.system.listSystemsWithPackage(key1,i['id'])
            for systems in syswithpkg:
               output = output + systems['name'] + "\n"
      return output[:-1]

   def getSysWOPkg(self, pkgname):
      key1, client1 = getKey()
      output = ""
      sysw = []
      syswo = []
      syswithpkg = []
      pkg_name = "-".join(pkgname.split('-')[:-2])
      pkg_ver  = pkgname.split('-')[-2:][0]
      pkg_rel  = ".".join(pkgname.split('-')[-1].split('.')[:-2])
      srch = "name:%s AND version:%s AND release:%s" %(pkg_name,pkg_ver,pkg_rel)
      package = client1.packages.search.advanced(key1,srch)	
      for i in package:
         x = i['name'] + "-" + i['version'] + "-" + i['release'] + "." + i['arch'] + ".rpm"
         if str(pkgname).strip() == str(x).strip():
            syswithpkg = client1.system.listSystemsWithPackage(key1,i['id'])
      allsystems = client1.system.listSystems(key1)
      for systems in allsystems:
         syswo.append(systems['name'])
      for systemsw in syswithpkg:
         sysw.append(systemsw['name'])
      syswithopkg = set(syswo) - set(sysw)            
      for x in syswithopkg:
         output = output + x + "\n"
      return output[:-1]

   def inPkg(self,SysAndPkgs):
      key1, client1 = getKey()
      count = 0
      pkgids = [] 
      chans=[]
      latest_packages = {}
      getId = client1.system.getId(key1,SysAndPkgs['opt0'])[0]['id']

# Get system channels #

      baseChan = client1.system.getSubscribedBaseChannel(key1,getId)['label']
      childChans = client1.system.listSubscribedChildChannels(key1,getId)
      chans.append(baseChan)
      for i in childChans:
         chans.append(i['label'])
      for x in chans:
         latest_packages[chans.index(x)] = client1.channel.software.listLatestPackages(key1,x)
      td = getDate(SysAndPkgs['opt1'])
      if td == "timefsck":
         return "Failed, date is in the past or in an incorrect format, probably!"
      del SysAndPkgs['opt0']
      del SysAndPkgs['opt1']
      for pkg in SysAndPkgs.values():
	 if pkg[-3:] != "rpm":
            for lists in latest_packages:
               for i in latest_packages[lists]:
                  x = i['name'] + "-" + i['version'] + "-" + i['release'] + "." + i['arch_label'] + ".rpm"
                  if str(pkg).strip() == str(i['name']).strip():
                        pkgids.append(i['id'])
                        count = 1
            if count == 0: 
               return "cannot find package named: %s" %(pkg)
            else: 
               count = 0
	 else:
            pkg_name = "-".join(pkg.split('-')[:-2])
            pkg_ver  = pkg.split('-')[-2:][0]
            pkg_rel  = ".".join(pkg.split('-')[-1].split('.')[:-2])
            srch = "name:%s AND version:%s AND release:%s" %(pkg_name,pkg_ver,pkg_rel)
            package = client1.packages.search.advanced(key1,srch)
            for i in package:
               x = i['name'] + "-" + i['version'] + "-" + i['release'] + "." + i['arch'] + ".rpm"
               if str(pkg).strip() == str(x).strip():
                  pkgids.append(i['id'])
		  count = 1
            if count == 0: 
               return "cannot find package named: %s" %(pkg)
            else: 
               count = 0
      client1.system.schedulePackageInstall(key1,getId,pkgids,td)
      client1.system.schedulePackageRefresh(key1,getId,td)
      return "RPM/s scheduled to run at first checkin after %s, if now was called, run rhn_check on host to execute!" %(td)


   def chkSched(self,SysAndTime):
      DKEY=""
      passfail="Didn't catch passed or failed jobs for this schedule, sure this schedule applies to this host?"
      key1, client1 = getKey()
      sysname=str(SysAndTime['opt0']).strip()
      dTime=str(SysAndTime['opt1']).strip()
      yr,tm=dTime.split("T")
      id = client1.system.getId(key1,sysname)
      events = client1.system.listSystemEvents(key1,int(id[0]['id']))
      DKEY = yr[:4] + "-" + yr[4:-2] + "-" + yr[-2:] + " " + tm + ":00.0"
      for i in events:
         if str(i['earliest_action']).strip() == DKEY and str(i['action_type']).strip() == "Package Install":
            if str(i['failed_count']).strip() == "0" and str(i['successful_count']).strip() == "0":
               return str(i['action_type']) + ":" + str(i['additional_info'][0]['detail']) + " - " + "Pending"
            elif str(i['failed_count']).strip() == "1":
               return "Failed: - %s : %s - Reason: %s" %(i['action_type'],i['additional_info'][0]['detail'],i['result_msg'])
            elif str(i['successful_count']).strip() == "1":
               return "Passed: - %s : %s - Reason: %s" %( i['action_type'],i['additional_info'][0]['detail'],i['result_msg'])
