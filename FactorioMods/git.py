import logging
import os
from FactorioMods.excepections.FactorioModException import FactorioModException

logger = logging.getLogger(__name__)

import subprocess


def safe_call(*popenargs, **kwargs):
    p = subprocess.Popen(*popenargs,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    if not p:
        raise Exception("call failed (no p): %s" % str(popenargs))

    retVal = p.communicate()
    logger.debug("safe_call(%s) = %s" % (str(popenargs), p.returncode))

    if p.returncode:
        logger.warn("std_err: %s" % retVal[1])
        raise FactorioModException("call failed [%s]: %s" % (p.returncode, str(popenargs)))

    return retVal[0]

class Git(object):
    def __init__(self, base_directory):
        if not os.path.exists(base_directory):
            raise FactorioModException("path does not exit: %s" % base_directory)
        self.base_directory = base_directory

    @property
    def is_initialized(self):
        return os.path.exists(os.path.join(self.base_directory, ".git"))

    @property
    def version(self):
        return safe_call(["git", "--version"])

    def init_repo(self):
        if self.is_initialized:
            raise FactorioModException("already initialized")

        logger.info("git init: %s" % self.base_directory)
        safe_call(["git", "init", self.base_directory])
