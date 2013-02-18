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

Implement Priority and Affinity classes using vsc.utils.affinity
"""

from vsc.processcontrol.priority import Priority
from vsc.processcontrol.affinity import Affinity
from vsc.processcontrol.algorithm import BasicCore
try:
    from vsc.utils.affinity import sched_getaffinity, sched_setaffinity, cpu_set_t, getpriority, setpriority
    valid = True
except:
    vaild = False

MODE_NAME = 'vsc'

class VSCPriority(Priority):
    PRIORITY_MODE = MODE_NAME
    VALID = valid
    def _get_priority(self):
        self.priority = getpriority(who=self.pid)

    def _set_priority(self):
        setpriority(self.priority, who=self.pid)

class VSCAffinity(Affinity):
    AFFINITY_MODE = MODE_NAME
    VALID = False  # abstract, don't use
    def _get_affinity(self):
        ctypes_cpuset_t = sched_getaffinity(pid=self.pid)
        self.cpusett.set_bits(cpus=ctypes_cpuset_t.cpus)

    def _set_affinity(self):
        cs = cpu_set_t()
        cs.set_bits(cpus=self.cpusett.cpus)
        sched_setaffinity(cs, pid=self.pid)

class VSCAffinityBasic(VSCAffinity):
    AFFINITY_ALGORITHM = 'basiccore'
    VALID = valid

    def _algorithm(self, total_proc, proc_nr):
        proc_nr = int(proc_nr)
        total_proc = int(total_proc)

        self.get_affinity()
        allowed_cpus = self.cpusett.get_cpus_idx()  # takes into account cgroups/cpusets
        total_cpus = len(allowed_cpus)

        alg = BasicCore()
        alg.create(total_cpus, total_proc)
        rel_cpus = alg.get_cpus(proc_nr)

        # rel_cpus is a list relative to the usable cpus of cpusett.cpus
        for rel_idx, abs_idx in enumerate(allowed_cpus):
            self.cpusett.cpus[abs_idx] = int(rel_idx in rel_cpus)

if __name__ == '__main__':
    """Simple test code. Difficult to write unit tests because of direct dependency on hardware"""
    import time
    vp = VSCPriority()
    print vp.get_priority()

    vp.set_priority(5)
    print vp.get_priority()

    vab = VSCAffinityBasic()
    print vab.get_affinity()
    # process nr 1 out of 2 processes
    vab.algorithm(1, 2)
    print vab.get_affinity()


    time.sleep(5)
