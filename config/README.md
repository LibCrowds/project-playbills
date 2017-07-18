# Configuration

This folder contains the following configuration files.

### api.json

The PyBossa API endpoints for development and production.

### help.json

The file used to create the interactive tutorial shown to users on the
first visit.

### long_description.md

The long description for all projects.

### metadata.csv

This file contains a mapping between IIIF manifest URIs and name suffixes that
are appended to the name prefixes defined in tasks.json.

While it would be possible to use the labels from the manifest as the suffix
there are instances where this wouldn't meet the required standards (such as
the label being too long).

The manifest URI should always be listed in the first column with the name
suffix in the second. Additional columns can be added for reference and will
be ignored.

### tasks.json

Defines the configuration used to generate the project context and tasks.

All key value pairs under `task` are fed directly into the task info field in
additional to the manifest URI and the image info URI extracted from the
manifest. This info field is in turn used to generate the task options that
are fed into an instance of
[libcrowds-viewer](https://github.com/LibCrowds/libcrowds-viewer)
(see the libcrowds-viewer docs for more details of the available task options).
These task options are updated at runtime with properties such as `id`,
`creator` and `generator`.

The keys under `project` are used to create the project title and description.
