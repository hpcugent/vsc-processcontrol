#
# Copyright 2013-2013 Ghent University
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
Some common classes and functions

@author: Stijn De Weirdt (Ghent University)
"""
import os

try:
    from vsc.utils.fancylogger import getLogger
except:
    from logging import getLogger

def get_subclasses(klass):
    """
    Get all subclasses recursively
    """
    res = []
    for cl in klass.__subclasses__():
        res.extend(get_subclasses(cl))
        res.append(cl)
    return res

def what_classes(klass, allow_not_valid=False):
    """What subclasses of klass are there?
        - allow_not_valid : filter for VALID
    """
    found_klasses = [x for x in get_subclasses(klass) if x.VALID or allow_not_valid]

    return found_klasses


class DummyFunction(object):
    def __getattr__(self, name):
        def dummy(*args, **kwargs):
            pass
        return dummy


class InitLog(object):
    """Base class to set logger
        - set logger in __init__ to log attr
    """
    def __init__(self, *args, **kwargs):
        """
            - disable_log : boolean use dummy logger
        """
        disable_log = kwargs.pop('disable_log', False)
        if disable_log:
            log = DummyFunction()
        else:
            log = getLogger(self.__class__.__name__)
        self.log = log

class ProcessControlBase(InitLog):
    """Base class for all process control classes
        - set pid attribute
    """
    VALID = False  # is this a valid class ?
    def __init__(self, *args, **kwargs):
        """
            - disable_log : boolean use dummy logger
            - pid : int process id
        """
        pid = kwargs.pop('pid', None)
        super(ProcessControlBase, self).__init__(*args, **kwargs)

        if pid is None:
            pid = os.getpid()
        else:
            pid = int(pid)
        self.pid = pid
