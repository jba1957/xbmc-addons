#if 0 /*
# -----------------------------------------------------------------------
# datainfo.py - info about a normal data disc
# -----------------------------------------------------------------------
# $Id: datainfo.py,v 1.3 2004/02/28 18:45:05 dischi Exp $
#
# -----------------------------------------------------------------------
# Copyright (C) 2003 Thomas Schueppel, Dirk Meyer
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MER-
# CHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
# ----------------------------------------------------------------------- */
#endif


from mmpython import mediainfo
import mmpython
from discinfo import DiscInfo

class DataDiscInfo(DiscInfo):
    def __init__(self,device):
        DiscInfo.__init__(self)
        self.context = 'unknown'
        self.offset = 0
        self.valid = self.isDisc(device)
        self.mime = 'unknown/unknown'
        self.type = 'CD'
        self.subtype = 'data'

    def isDisc(self, device):
        if DiscInfo.isDisc(self, device) != 2:
            return 0

        return 1



mmpython.registertype( 'cd/unknown', mediainfo.EXTENSION_DEVICE, mediainfo.TYPE_NONE, DataDiscInfo )
