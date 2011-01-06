#!/usr/bin/env python

import time
import sys

from bravo.chunk import Chunk
from bravo.ibravo import ITerrainGenerator
from bravo.plugin import retrieve_plugins

def timed(f):
    def wrapped(*args, **kwargs):
        before = time.time()
        f(*args, **kwargs)
        return time.time() - before
    return wrapped

@timed
def empty_chunk(i):
    Chunk(i, i)

@timed
def sequential_seeded(i, p):
    chunk = Chunk(i, i)
    p.populate(chunk, i)

@timed
def repeated_seeds(i, p):
    chunk = Chunk(i, i)
    p.populate(chunk, 0)

plugins = retrieve_plugins(ITerrainGenerator)

def empty_bench():
    l = [empty_chunk(i) for i in xrange(25)]
    return "chunk_baseline", l

benchmarks = [empty_bench]
for plugin in plugins:
    name = plugin.name
    def seq():
        l = [sequential_seeded(i, plugin) for i in xrange(25)]
        return ("chunk_%s_sequential" % name), l
    def rep():
        l = [repeated_seeds(i, plugin) for i in xrange(25)]
        return ("chunk_%s_repeated" % name), l
    benchmarks.append(seq)
    benchmarks.append(rep)
