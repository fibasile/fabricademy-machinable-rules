# Tests for machine-friendly assessment rules

This is a small test, to try ways to represent assessment rules in a git-friendly format that can be converted easily
in UI for the evaluation.

In the test the rules are represented using [YAML](http://yaml.org/)


## Rule file format

The structure follows this general model:

    unit: <Unit name>
      tasks:
       - name: Task name
         description: markdown description
         outcomes: list of outcomes
         checklist: student checklist
       -..
      faq: Markdown faq

Take a look to the provided .yaml for a full example

## Build.py

This script takes all the yaml files in src/ and can:

**Test them for correctness**

   python build.py test

This will simply check syntax and exit without errors if it's correct

**Convert them to Markdown**

   python build.py gitbook

This will generate a `gitbook` folder containing the Markdown formatted files.

**Convert them to JSON**

   python build.py json

This will generate a `json` folder containing the JSON formatted files.

## Try it yourself

To be able to run build.py you need to intsall the packages in requirements.txt

   pip install -r requirements.txt

## Using Docker

```
docker build -t fabricademy-machinable-rules .

docker run --rm -it -v ${PWD}:/src fabricademy-machinable-rules json
docker run --rm -it -v ${PWD}:/src fabricademy-machinable-rules gitbook
```

## Next steps

This format should allows us to build the gitbook and nueval version from the YAML files,
so we might convert the remaining pagese using the format.


