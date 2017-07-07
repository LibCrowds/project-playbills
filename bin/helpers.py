#-*- coding: utf8 -*-
"""
Helper functions for project-playbills-mark scripts.
"""
import os
import csv
import json
import os
import errno

__all__ = ['SRC_DIR', 'DIST_DIR', 'get_taskset', 'get_csv_field', 'mkdist']

SRC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src')
DIST_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dist')


def get_taskset(name):
    """Return the chosen taskset."""
    tasks_file = open(os.path.join(SRC_DIR, 'data', 'tasks.json'), 'rb')
    tasks_json = json.load(tasks_file)
    return tasks_json[name]


def get_csv_field(sysno, field):
    """Return the CSV metadata value adjacent to a system number."""
    f = open(os.path.join(SRC_DIR, 'data', 'metadata.csv'), 'rb')
    reader = csv.reader(f)
    rows = [r for r in list(reader) if r[0] == str(sysno)]
    if not rows:
        raise ValueError('{0} not found'.format(sysno))
    if field == 'ark':
      return rows[0][1]
    elif field == 'name':
      return rows[0][2]
    raise ValueError('Invalid field requested from CSV file')


def mkdist():
    """Create an empty dist folder if one doesn't already exist."""
    try:
      os.makedirs(DIST_DIR)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
