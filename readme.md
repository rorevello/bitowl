# README.md

## Description
This Python script is used to read the annotations.json files, validate them against a JSON schema, and then convert the information to an RDF graph using the rdflib library.
The RDF graph is then saved to a file ``ontology_enbic2lab.owl``.
Schema validations as well as errors are stored in a file called ``log_annotation.txt``.

## Usage
To use this script, place the ``main.py`` file and the ``ontology`` folder with ``bigowl`` in the repository's root folder. Run to ``main.py`` from your terminal; the script will search the different subfolders, and using ``bigowl`` will generate the final ontology.

## Execution
To run this script, you will need to have Python installed on your machine. Then, you can execute the script with the following command:

```bash
python main.py
```

This script depends on the following Python libraries:

- json
- jsonschema
- rdflib
- os
- uuid

Make sure to have these libraries installed before running the script. You can install them using pip:

```bash
pip install jsonschema rdflib uuid 
```

