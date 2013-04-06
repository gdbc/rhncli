import os

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



# Overall group check class 

class KAuth:

# This function checks the group the user is in to see if they can run the specified cmd

   def getgrplist(self,username):
     uname = username
     d = os.popen('groups %s' % uname).read().split(':')[1]
     ulist = d.split()
     return ulist

   def grpcheck(self,grplist, username):
     userlist = self.getgrplist(username)
     for u in userlist: 
      if u in grplist:
       grpexists = True
       break 
      grpexists = False
     return grpexists
