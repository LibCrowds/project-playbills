# Configuration

This folder contains the following configuration files.

### tasks.json

Defines the configurations used to generate the project context and tasks.

All key value pairs under `task` are fed directly into the task info field in
addition to the manifest URI and the image info URI extracted from the
manifest. This info field is in turn used to generate the task options that
are fed into an instance of
[libcrowds-viewer](https://github.com/LibCrowds/libcrowds-viewer)
(see the libcrowds-viewer docs for more details of the available task options).

The keys under `project` are used to create project-specific details, such as
the title and description.

### metadata.csv

This file contains a mapping between IIIF manifest URIs and name suffixes that
are appended to the name prefixes defined in tasks.json.

## help

The help folder contains a set of markdown files that can be loaded as the 
tutorial for a project by linking them via the `tutorial` key in `tasks.json`.
