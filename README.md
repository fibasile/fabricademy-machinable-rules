# NuEval machine-friendly assessment rules

These are the assessment rules in a git-friendly format that can be converted easily
in UI for the NuEval evaluation and into the "Criteria Assessment" doc.

The Yaml structure allows us to build both the gitbook and nueval formats.

> This project will automatically build and publish the Gitbook docs using GitLab CI & Pages.

## Locations

* Yaml rules: `/src` (the criteria/rules in yaml format)

## Assessment rules file format

The rules are represented using [YAML](http://yaml.org/). The structure follows this general model:

```yaml
    unit: <Unit name>
      tasks:
       - name: Task name
         description: markdown description
         outcomes: list of outcomes
         checklist: student checklist
       -..
      faq: Markdown faq
```

Take a look at the provided .yaml rules in `src` folder for a full example

> **Remember** Indentation is very important in a YAML file


## Outputs

* `public/json` files for importing into Nueval (inc a `rules.json` list of all files).
* `public/gitbook/criteria.md` markdown file containing all criteria to add to handbook.


## Run locally

There is a python script that takes all the Yaml files and converts them into JSON and Markdown files.

To be able to run the build script you, need to install the packages from [requirements.txt](requirements.txt).

`pip install -r requirements.txt`

### Step 1. Validate Yaml files
This will check syntax and exit without errors if it's correct. If there are errors, review and fix the corresponding yaml files.

`python build.py test`

### Step 2. Convert Yaml to JSON
Use this to generate the Nueval json files. This will generate a `json` folder containing the JSON formatted files.

`python build.py json`

### Step 3. Convert Yaml to Markdown
Use this to generate the markdown for Gitbook docs. This will add files to the `gitbook` folder formatted as Markdown.

`python build.py gitbook`


## Example: Using Docker
Can be usefull to test/run locally, without installing Python/gitbook etc. 
The Dockefiles (or CI) can also be used to see what is needed to run these scripts

### First time: 

`docker build -t fabri-rules-build -f Dockerfile-build .`
`docker build -t fabri-rules-gitbook -f Dockerfile-gitbook .`

And probably this one:
`docker run --rm -it -v ${PWD}/gitbook:/opt/gitbook fabri-rules-gitbook gitbook install`

### To generate JSON
`docker run --rm -it -v ${PWD}:/src fabri-rules-build json`

### To generate Gitbook/docs
`docker run --rm -it -v ${PWD}:/src fabri-rules-build gitbook`
`docker run --rm -it -v ${PWD}/gitbook:/opt/gitbook -v ${PWD}/public:/opt/public fabri-rules-gitbook`
