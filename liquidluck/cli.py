#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import argparse
from liquidluck.config import Config
from liquidluck import logger

def apply_writer(writer_name):
    logger.info('Apply writer: ' + writer_name)
    writers = writer_name.split('.')
    if len(writers) == 1:
        return __import__(writer_name)

    package = __import__('.'.join(writers[:-1]))
    for module in writers[1:]:
        package = getattr(package, module)
    return package

def build(config):
    begin = time.time()

    cwd = os.getcwd()
    config = Config(os.path.join(cwd, config))
    writers = [apply_writer(writer) for writer in config.writers.itervalues()]
    for writer in writers:
        writer(config, cwd).register()

    for writer in writers:
        writer(config, cwd).run()
    end = time.time()

    print end - begin

def main():
    parser = argparse.ArgumentParser(
        prog='felicis',
        description='Felix Felicis, aka liquidluck, is a static weblog generator',
    )
    parser.add_argument('--config', dest='config', default='.conf', metavar='.conf')
    parser.add_argument('--command', dest='command', default='build', metavar='build')
    args = parser.parse_args()

    if 'build' == args.command:
        build(args.config)

if '__main__' == __name__:
    main()
