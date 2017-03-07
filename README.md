# project-playbills-mark

Playbills marking project for LibCrowds.


## Creating a new project

Generate the tasks:

```
python bin/generate_tasks_.py <Aleph system number>
```

Create the project:
```
python bin/create_project_.py <endpoint> <api_key>
```

The first script generates the tasks for a given Aleph system number. The second creates a new project using a name 
derived from the title of the catalogue record, adds the tasks and sets the task redundancy. The project can now be
published from the project settings page.