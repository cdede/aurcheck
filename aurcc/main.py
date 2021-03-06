#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import AUR.RPC as AUR
from time import localtime, strftime 
from pycman import config
import pyalpm

class Aurget(AUR.AUR):
    def __init__(self,pkgnames ):
        super(Aurget, self).__init__(ttl=1, log_func=lambda x,y: None)
        self.pkgnames=pkgnames
      
    def get_aur_pkgs(self):
        """Search the AUR."""
        try:
            return AUR.insert_full_urls(self.info(self.pkgnames))
        except AUR.AURError as e:
            sys.stderr.write(str(e))
            sys.exit(1)

class Upgrad(object):
    def __init__(self ):
        self.aurs = []
        self.dict1 = {}
        self.get_upgradable()
    
    def get_upgradable(self):
        """Search for upgradable packages."""
      
        h = config.init_with_config("/etc/pacman.conf")
        installed = set(h.get_localdb().pkgcache)
      
        for db in h.get_syncdbs():
            for pkg in list(installed):
                pkgname = pkg.name
                syncpkg = db.get_pkg(pkgname)
                if syncpkg:
                    installed.remove(pkg)
          
        foreign = dict([(p.name,p) for p in installed])
      
        ag1 = Aurget((p.name for p in installed))
      
        for aur_pkg in ag1.get_aur_pkgs():
            installed_pkg = foreign[aur_pkg['Name']]
            if pyalpm.vercmp(aur_pkg['Version'], installed_pkg.version) != 0:
                key = aur_pkg['Name']
                self.aurs.append(key)
                self.dict1[key]= installed_pkg.version
      

def main():
    up1 = Upgrad()
    pkgnames = set(up1.aurs)

    if not pkgnames:
        print("nothing to do")
        return

    else:
        print("searching AUR interface")
        ag1 = Aurget(pkgnames)
        for aurpkg in ag1.get_aur_pkgs():
            tmp1 = aurpkg['Name']
            print("  found", tmp1)
            pkgnames.remove(tmp1)
            display_fields = ('LocalVersion','Version', 'LastModified')
            aurpkg['LastModified'] = strftime(
                '%Y-%m-%d %H:%M:%S', localtime(aurpkg['LastModified'])
            )
            aurpkg['LocalVersion'] = up1.dict1[tmp1]
            l = max(len(x) for x in display_fields) + 1
            fmt = '    %-' + str(l) + 's %s'
            for df in display_fields:
                print(fmt % (df + ':', aurpkg[df]))
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
