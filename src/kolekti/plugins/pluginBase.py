# -*- coding: utf-8 -*-
#     kOLEKTi : a structural documentation generator
#     Copyright (C) 2007-2011 Stéphane Bonhomme (stephane@exselt.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys
import shutil
from lxml import etree as ET
from kolekti.common import kolektiBase
from kolekti.publish import PublishExtensions

class plugin(kolektiBase):
    _plugin="dummy"
    LOCAL_ENCODING=sys.getfilesystemencoding()
    
    def __init__(self, *args, **kwargs):
        super(plugin, self).__init__(*args, **kwargs)
        self._plugin = self.__module__.split('.')[-1]
        self._plugindir = os.path.join(self.appdir,'plugins',"_%s"%self._plugin)
        self.__ext = None

    def get_xsl(self,xslfile, **kwargs):
        return super(plugin,self).get_xsl(xslfile, extclass = self.__ext, xsldir = self._plugindir, **kwargs)

    def __call__(self, scriptdef, profile, pubdir, pivot, lang ):
        self.scriptdef = scriptdef
        self.profile = profile
        self.pubdir = pubdir
        self.pivot = pivot
        self.lang = lang
        self.__ext = PublishExtensions
        scriptlabel = scriptdef.get('name')
        profilelabel = profile.xpath('string(label)')
        self.pubscriptdir = pubdir + "/" + profilelabel + "/" +scriptlabel
        self.pubprofiledir_c = pubdir + "/" + profilelabel + "_c"
        try:
            self.makedirs(self.pubscriptdir)
        except:
            pass
        
        print "Script ", scriptlabel

        for m in self.postpub():
            yield m
            
        return

    def copymedias(self):
        for d in ['medias']:
            source = self.pubprofiledir_c + '/' + d
            target = self.pubscriptdir + '/' + d
            self.copyDirs(source,target)
            
        
    def postpub(self):
        """
        postpub is the iterator used in plugin
        """
        yield "Dummy plugin"
        return

    def get_script_parameter(self, param):
        try:
            return self.scriptdef.xpath('string(script/parameters[@name="%s"]/@value)')
        except:
            return None
