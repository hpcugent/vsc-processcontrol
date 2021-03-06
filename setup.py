#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# Copyright 2009-2013 Ghent University
#
# This file is part of vsc-processcontrol,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/vsc-processcontrol
#
# vsc-processcontrol is free software: you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License as
# published by the Free Software Foundation, either version 2 of
# the License, or (at your option) any later version.
#
# vsc-processcontrol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with vsc-processcontrol. If not, see <http://www.gnu.org/licenses/>.
#
"""
@author: Stijn De Weirdt (Ghent University)

Setup for the VSC-tools ldap utilities
"""

from shared_setup import  sdw
from shared_setup import action_target

PACKAGE = {
    'name': 'vsc-processcontrol',
    'install_requires': ['vsc-base >= 0.99'],
    'version': '1.0',
    'author': [sdw],
    'maintainer': [sdw],
    'packages': ['vsc.processcontrol', 'vsc'],
    'scripts': [],
}

if __name__ == '__main__':
    action_target(PACKAGE)
