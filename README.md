# project-playbills-mark

Playbills marking projects for LibCrowds, designed for use with the 
[libcrowds-bs4-pybossa-theme](https://github.com/LibCrowds/libcrowds-bs4-pybossa-theme).


## Creating a new project

Choose a set of tasks from [tasks.json](tasks/tasks.json) (e.g. `"events"`) 
and either an Aleph system number from the file 
[ark_and_aleph_system_numbers.csv](tasks/ark_and_aleph_system_numbers.csv) or a 
JSON file where the info field contains the keys *aleph_sys_no*, *image_ark* 
and *regions*.

When generating tasks from an Aleph system number a new task will be created
for each permutation of image and test in the chosen set. When generating
tasks from a JSON file (which will probably be the result of a previous marking
task) a new task will be created for all permutations of an image, each region 
now associated  with that image and each task in the chosen task set. The idea 
being that we can chain tasks to highlight increasingly more specific regions 
in the text.

To generate a new project and push it to the server 
install and configure [pbs](https://github.com/Scifabric/pbs), then:

```
python generate_project.py <task set> [--sysno=<sysno> or --json=<path>]
cd gen
pbs create_project
pbs add_tasks --tasks-file=tasks.csv
pbs update-task-redundancy --redundancy 3
pbs update_project
```

Now visit the project settings page and update the category, webhook and 
thumbnail. The project is now ready to be published.


## Bad Ark Identifiers

Some of the ark identifiers in 
[ark_and_aleph_system_numbers.csv](tasks/ark_and_aleph_system_numbers.csv) do 
not point to images that can be retreived via the BL IIIF API. For now, these
rows are being moved to [bad_arks.csv](tasks/bad_arks.csv). If you receive an 
error message stating that a bad ark has been find while generating the project
just copy that row over to [bad_arks.csv](tasks/bad_arks.csv) and run the script
again. We'll deal with these later!