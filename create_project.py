"""
A script for generating the a project for project-playbills-mark.
"""
import os
import argparse
import pbs


if __name__ == '__main__':
    description = '''Generate a project for project-playbills-mark.'''
    here = os.path.dirname(__file__)
    default_tasks = os.path.join(here, 'tasks.csv')
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--tasks', default=default_tasks, help="The CSV tasks file.")
    args = parser.parse_args()
    pass