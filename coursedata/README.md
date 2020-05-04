Course Data Structure
=====================

```
course/{coursename}/{language}.yaml         <-- course definition
course/{coursename}/docs-{language}/*.md    <-- docs pages
level-defaults/{language}.yaml              <-- defaults for every level
```

## Course Definitions

```
trajectories:
  {trajectory_name}:                        <-- list of assignments
    - level: {level}
      intro_text: {text above examples}
      commands:                             <-- list of examples
        - name: {unused?}
          explanation: {...}
          example: {...}
          demo_code: {...}
      prompt: {text below examples}
      start_code: {initial code}
```

Field `level` is required.

Fields `into_text`, `commands`, `start_code` are taken from the indicated
level if not supplied.

## Level Defaults

```
{level}:
  intro_text: {text above examples}
  start_code: {initial code}
  commands: {as under course definitions}
```

## MarkDown docs pages

MarkDown docs must end in `.md` extension and have a "front matter" section
(which is a YAML object ending in `---` before the start of the real document).

The front matter must have the following fields:

```
title: {page title here}
level: {level it applies to}
[trajectory: {...} should probably be added in the future but isn't yet]
---
# Real document starts here

...
```
