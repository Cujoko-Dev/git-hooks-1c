# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import sys

from git_hooks_1c.core import run

sys.path.insert(0, os.path.abspath(os.path.join(__file__, os.pardir, os.pardir)))

if __name__ == '__main__':
    run()
