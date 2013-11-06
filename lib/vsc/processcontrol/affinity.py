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
@author: Stijn De Weirdt (Ghent University)

A module to abstract cpu affinity interfaces
"""
from vsc.processcontrol.processcontrol import ProcessControlBase, what_classes
from vsc.processcontrol.cpusett import CpuSetT

def what_affinity(mode=None, algo=None):
    """What affinity classes are there?"""
    found_affinities = what_classes(Affinity)

    # case insensitive match?
    if mode is not None:
        found_affinities = [x for x in found_affinities if x.is_affinity_mode(mode)]
    if algo is not None:
        found_affinities = [x for x in found_affinities if x.is_algorithm(algo)]


    return found_affinities


class Affinity(ProcessControlBase):
    """An abstract class for controlling cpu affinity of a process"""
    AFFINITY_MODE = None
    AFFINITY_ALGORITHM = None
    CPUSETT_CLASS = CpuSetT

    def __init__(self, *args, **kwargs):
        super(Affinity, self).__init__(*args, **kwargs)

        self.cpusett = self.CPUSETT_CLASS()

    @classmethod
    def is_affinity_mode(cls, mode):
        if cls.AFFINITY_MODE is not None:
            return mode.lower() == cls.AFFINITY_MODE.lower()
        else:
            return None

    @classmethod
    def is_algorithm(cls, name):
        if cls.AFFINITY_ALGORITHM is not None:
            return name.lower() == cls.AFFINITY_ALGORITHM.lower()
        else:
            return None

    def _get_affinity(self):
        """Actually get the affinity of self.pid and save in self.cpusett
        """
        self.log.error("_get_affinity not implemented")

    def _set_affinity(self):
        """Actually set the affinity for self.pid from self.cpusett
            TO BE IMPLEMENTED
        """
        self.log.error("_set_affinity not implemented")

    def _sanitize_cpuset(self, cpuset=None):
        """Check if cpuset is proper type"""
        if cpuset is None:
            cpuset = self.cpusett

        if not isinstance(cpuset, self.CPUSETT_CLASS):
            self.log.error("_sanitize_cpuset: cpuset type %s, expected %s" % (type(cpuset), self.CPUSETT_CLASS.__name__))

        # TODO actual sanity check

        self.cpusett = cpuset

    def get_affinity(self):
        """Get the affinity of self.pid
            @return : CpuSetT instance
        """
        self._get_affinity()
        return self.cpusett

    def set_affinity(self, cpuset):
        """Set the affinity for self.pid
            - cpuset : instance of CpuSetT
        """
        self._sanitize_cpuset(cpuset)
        self._set_affinity()

    def _algorithm(self, *args, **kwargs):
        """Given set of arguments, set cpusett with new process placement
            TO BE IMPLEMENTED
        """
        self.log.error("_algorithm not implemented")

    def algorithm(self, *args, **kwargs):
        """Given set of arguments, set cpusett with new process placement
            TO BE IMPLEMENTED
        """
        self._algorithm(*args, **kwargs)
        self.set_affinity(self.cpusett)
