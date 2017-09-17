#-*- coding: utf8 -*-
"""
A script for generating a project-playbills project.
"""
import argparse
import generate_context
import generate_tasks
import generate_help


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description="Generate a project")
    PARSER.add_argument('category', help="A task category in tasks.json.")
    PARSER.add_argument('manifestid', help="IIIF manifest ID.")
    PARSER.add_argument('--config', help="Project configuration.")
    PARSER.add_argument('--results', help="JSON results file.")
    PARSER.add_argument('--skip', help="Skip the first n tasks.")
    ARGS = PARSER.parse_args()
    CONTEXT = generate_context.generate(ARGS.category, ARGS.manifestid,
                                        ARGS.config)
    TASKS = generate_tasks.generate(ARGS.category, ARGS.manifestid, ARGS.config,
                                    ARGS.results)
    generate_help.generate(ARGS.category, ARGS.config)
    print '\n"{0}" created with {1} tasks'.format(CONTEXT['name'], len(TASKS))
