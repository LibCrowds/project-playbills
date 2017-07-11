#-*- coding: utf8 -*-
"""
A script for generating a project-iiif-mark project.
"""
import argparse
import generate_context
import generate_tasks
import copy_files


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description="Generate a project")
    PARSER.add_argument('category', help="A task category in tasks.json.")
    PARSER.add_argument('manifestid', help="IIIF manifest ID.")
    PARSER.add_argument('--config', help="Project configuration.")
    PARSER.add_argument('--results', help="JSON results file.")
    ARGS = PARSER.parse_args()
    CONTEXT = generate_context.generate(ARGS.category, ARGS.manifestid,
                                        ARGS.config)
    TASKS = generate_tasks.generate(ARGS.category, ARGS.manifestid, ARGS.config,
                                    ARGS.results)
    copy_files.copy(ARGS.config)
    print '\n"{0}" created with {1} tasks'.format(CONTEXT['name'], len(TASKS))
