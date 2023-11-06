import json
import jsonschema
import rdflib
import os
import uuid
from rdflib import Graph, Literal, RDFS, RDF, URIRef,OWL
from jsonschema import validate


def graph_rdf(path: str, graph, schema) -> Graph:
    """
    Read to json file (path) and return a graph object with the information of the json file

    Args:
        path (str): The path to the JSON file.
        graph: The graph object to add information to.
        schema: The JSON schema to validate the file against.

    Returns:
        Graph: The graph object with information from the file added.
    """
    try:
        error_in_modelage = 0
        # open json file
        with open(path, "r") as f:
            annotation = json.load(f)

        try:
            validate(annotation, schema)
            result = path + " follows the schema."
        except jsonschema.exceptions.ValidationError as e:
            result = path + f" --> ERROR does not follow the schema : {e}"
            error_in_modelage += 1

        with open("log_annotation.txt", "a") as file:
            file.write(result + "\n")

        uri_enbic2lab = "http://www.ontologies.khaos.uma.es/enbic2lab/"
        uri_bigowl = "http://www.ontologies.khaos.uma.es/bigowl/"

        name = str(annotation["name"])

        g = graph

        #############################
        #                           #
        #      Implementation       #
        #                           #
        #############################

        uri_implementation = uri_enbic2lab + "Implementation" + name.capitalize().replace(" ", "_")
        type_implementation = uri_bigowl + "Implementation"

        # dependecy
        for dependecie in annotation["dependencies"]:
            uri_dependecy = (
                uri_enbic2lab
                + str(dependecie["name"])
                + "_"
                + str(dependecie["version"])
                + "_"
                + str(dependecie["license"])
            )
            g.add((rdflib.URIRef(uri_dependecy), RDF.type,  rdflib.URIRef(uri_bigowl + "Dependency")))
            g.add(
                (
                    rdflib.URIRef(uri_dependecy),
                    RDFS.label,
                    rdflib.Literal(
                        str(dependecie["name"])
                        + "_"
                        + str(dependecie["version"])
                        + "_"
                        + str(dependecie["license"])
                    ),
                )
            )
            g.add(
                (
                    rdflib.URIRef(uri_dependecy),
                    rdflib.URIRef(uri_bigowl + "hasVersion"),
                    rdflib.Literal(dependecie["version"]),
                )
            )
            g.add((rdflib.URIRef(uri_bigowl + "hasVersion"), RDF.type, OWL.DatatypeProperty))
            g.add(
                (
                    rdflib.URIRef(uri_dependecy),
                    rdflib.URIRef(uri_bigowl + "hasLicense"),
                    rdflib.Literal(dependecie["license"]),
                )
            )
            g.add((rdflib.URIRef(uri_bigowl + "hasLicense"), RDF.type, OWL.DatatypeProperty))
            g.add(
                (
                    rdflib.URIRef(uri_dependecy),
                    rdflib.URIRef(uri_bigowl + "hasUrl"),
                    rdflib.Literal(dependecie["url"]),
                )
            )
            g.add((rdflib.URIRef(uri_bigowl + "hasUrl"), RDF.type, OWL.DatatypeProperty))
            g.add(
                (
                    rdflib.URIRef(uri_dependecy),
                    rdflib.URIRef(uri_bigowl + "hasLength"),
                    rdflib.Literal(dependecie["name"]),
                )
            )
            g.add((rdflib.URIRef(uri_bigowl + "hasLength"), RDF.type, OWL.DatatypeProperty))
            g.add(
                (
                    rdflib.URIRef(uri_implementation),
                    rdflib.URIRef(uri_bigowl + "hasDependency"),
                    rdflib.URIRef(uri_dependecy),
                )
            )
            g.add((rdflib.URIRef(uri_bigowl + "hasDependency"), RDF.type, OWL.ObjectProperty))
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                RDFS.label,
                rdflib.Literal(annotation["label"]),
            )
        )
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasName"),
                rdflib.Literal(str(annotation["name"])),
            )
        )
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                RDF.type,
                rdflib.URIRef(type_implementation),
            )
        )
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasDockerImage"),
                rdflib.Literal(annotation["dockerImage"]),
            )
        )
        g.add((rdflib.URIRef(uri_bigowl + "hasDockerImage"), RDF.type, OWL.DatatypeProperty))
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasLicense"),
                rdflib.Literal(annotation["license"]),
            )
        )
        g.add((rdflib.URIRef(uri_bigowl + "hasLicense"), RDF.type, OWL.DatatypeProperty))
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasVersion"),
                rdflib.Literal(annotation["version"]),
            )
        )
        g.add((rdflib.URIRef(uri_bigowl + "hasVersion"), RDF.type, OWL.DatatypeProperty))
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasPublicationDate"),
                rdflib.Literal(annotation["publicationDate"]),
            )
        ) 
        g.add((rdflib.URIRef(uri_bigowl + "hasPublicationDate"), RDF.type, OWL.DatatypeProperty))
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "Author"),
                rdflib.Literal(annotation["author"]),
            )
        )
        g.add((rdflib.URIRef(uri_bigowl + "Author"), RDF.type, OWL.DatatypeProperty))
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasCore"),
                rdflib.Literal(annotation["resources"]["cores"]),
            )
        )
        g.add((rdflib.URIRef(uri_bigowl + "hasCore"), RDF.type, OWL.DatatypeProperty))
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasMemory"),
                rdflib.Literal(annotation["resources"]["memory"]),
            )
        )
        g.add((rdflib.URIRef(uri_bigowl + "hasMemory"), RDF.type, OWL.DatatypeProperty))
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasGPUMemory"),
                rdflib.Literal(annotation["resources"]["gpuMemory"]),
            )
        )
        g.add((rdflib.URIRef(uri_bigowl + "hasGPUMemory"), RDF.type, OWL.DatatypeProperty))
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasGPUNeed"),
                rdflib.Literal(annotation["resources"]["gpuNeeded"]),
            )
        )
        g.add((rdflib.URIRef(uri_bigowl + "hasGPUNeed"), RDF.type, OWL.DatatypeProperty))
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasEstimatedTimeInMin"),
                rdflib.Literal(annotation["resources"]["estimatedTimeInMin"]),
            )
        )
        g.add((rdflib.URIRef(uri_bigowl + "hasEstimatedTimeInMin"), RDF.type, OWL.DatatypeProperty))
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasMainScriptPath"),
                rdflib.Literal(annotation["mainScriptPath"]),
            )
        )
        g.add((rdflib.URIRef(uri_bigowl + "hasMainScriptPath"), RDF.type, OWL.DatatypeProperty))
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasTestPath"),
                rdflib.Literal(annotation["testPath"]),
            )
        )
        g.add((rdflib.URIRef(uri_bigowl + "hasTestPath"), RDF.type, OWL.DatatypeProperty))

        #############################
        #                           #
        #        Algorithm          #
        #                           #
        #############################

        # convert type component to type algorithm
        dict_type_algorithm = {
            "DataAnalysing": "DataAnalysingAlgorithm",
            "MachineLearning": "DataAnalysingAlgorithm",
            "DataMinig": "DataAnalysingAlgorithm",
            "DataCollection": "DataCollectionAlgorithm",
            "DataIngestion": "DataAnalysingAlgorithm",
            "DataFlow": "DataFlowAlgorithm",
            "DataProcessing": "DataProcessingAlgorithm",
            "DataTransform": "DataProcessingAlgorithm",
            "RemoveOutlier": "DataProcessingAlgorithm",
            "Split": "DataProcessingAlgorithm",
            "SplitShuffle": "DataProcessingAlgorithm",
            "WebSever": "DataProcessingAlgorithm",
            "DataSink": "DataSinkAlgorithm",
        }

        uri_algorithm = uri_enbic2lab + "Algorithm" + name.capitalize().replace(" ", "_")

        try:
            type_algorithm = uri_bigowl + dict_type_algorithm[str(annotation["type"])]

        except:
            print(
                '--> ERROR: type algorithm not found in dict_type_algorithm: "DataAnalysing", "MachineLearning", "DataMinig", "DataCollection", "DataIngestion", "DataFlow", "DataProcessing", "DataTransform", "RemoveOutlier", "Split", "SplitShuffle", "WebSever", "DataSink"'
            )
            print("Path: " + path)
            print(
                "--> Algorithm: "
                + str(annotation["name"])
                + " type: "
                + str(annotation["type"])
            )
            print(
                "NOTE: if ontology was changed, please change dict_type_algorithm in main.py"
            )
            print(
                "Please check "
                + os.getcwd()
                + "/log_annotation.txt "
                + "for more errors"
            )
            

            error_in_modelage += 1

        g.add(
            (
                rdflib.URIRef(uri_algorithm),
                RDFS.label,
                rdflib.Literal(annotation["label"]),
            )
        )
        g.add(
            (
                rdflib.URIRef(uri_algorithm),
                rdflib.URIRef(uri_bigowl + "hasName"),
                rdflib.Literal(str(annotation["name"])),
            )
        )

        g.add((rdflib.URIRef(uri_algorithm), RDF.type, rdflib.URIRef(type_algorithm)))
        g.add(
            (
                rdflib.URIRef(uri_algorithm),
                RDFS.comment,
                rdflib.Literal(str(annotation["description"])),
            )
        )

        #############################
        #                           #
        #        Component          #
        #                           #
        #############################

        uri_component = uri_enbic2lab + "Component" + (name.capitalize()).replace(" ", "_")

        type_component = uri_bigowl + str(annotation["type"])

        g.add(
            (
                rdflib.URIRef(uri_component),
                RDFS.label,
                rdflib.Literal(annotation["label"]),
            )
        )
        g.add(
            (
                rdflib.URIRef(uri_component),
                rdflib.URIRef(uri_bigowl + "hasName"),
                rdflib.Literal(str(annotation["name"])),
            )
        )
        g.add((rdflib.URIRef(uri_component), RDF.type, rdflib.URIRef(type_component)))
        g.add(
            (
                rdflib.URIRef(uri_component),
                RDFS.comment,
                rdflib.Literal(str(annotation["description"])),
            )
        )

        g.add(
            (
                rdflib.URIRef(uri_component),
                rdflib.URIRef(uri_bigowl + "hasImplementation"),
                rdflib.URIRef(uri_implementation),
            )
        )
        g.add((rdflib.URIRef(uri_bigowl + "hasImplementation"), RDF.type, OWL.ObjectProperty))
        g.add(
            (
                rdflib.URIRef(uri_component),
                rdflib.URIRef(uri_bigowl + "hasAlgorithm"),
                rdflib.URIRef(uri_algorithm),
            )
        )
        g.add((rdflib.URIRef(uri_bigowl + "hasAlgorithm"), RDF.type, OWL.ObjectProperty))
        g.add(
            (
                rdflib.URIRef(uri_component),
                rdflib.URIRef(uri_bigowl + "hasNumberOfInputs"),
                rdflib.Literal(len(annotation["inputs"])),
            )
        )
        g.add((rdflib.URIRef(uri_bigowl + "hasNumberOfInputs"), RDF.type, OWL.DatatypeProperty))
        g.add(
            (
                rdflib.URIRef(uri_component),
                rdflib.URIRef(uri_bigowl + "hasNumberOfOutputs"),
                rdflib.Literal(len(annotation["outputs"])),
            )
        )
        g.add((rdflib.URIRef(uri_bigowl + "hasNumberOfOutputs"), RDF.type, OWL.DatatypeProperty))

        for parameter in annotation["parameters"]:
            parameter_uuid = uuid.uuid1()
            uri_parameter = (
                uri_enbic2lab
                + "Parameter"
                + (str(parameter["label"])).replace(" ", "_")
                + "_"
                + str(parameter_uuid)
            )

            g.add(
                (
                    rdflib.URIRef(uri_parameter),
                    RDFS.label,
                    rdflib.Literal(str(parameter["label"])),
                )
            )
            g.add(
                (
                    rdflib.URIRef(uri_parameter),
                    rdflib.URIRef(uri_bigowl + "hasName"),
                    rdflib.Literal(str(parameter["name"])),
                )
            )
            g.add(
                (
                    rdflib.URIRef(uri_parameter),
                    RDF.type,
                    rdflib.URIRef(uri_bigowl + "Parameter"),
                )
            )
            g.add(
                (
                    rdflib.URIRef(uri_parameter),
                    RDFS.comment,
                    rdflib.Literal(str(parameter["description"])),
                )
            )
            list_parametre_type = ["string", "number", "integer", "float", "boolean"]
            if str(parameter["type"]).lower() in list_parametre_type:
                g.add(
                    (
                        rdflib.URIRef(uri_parameter),
                        rdflib.URIRef(uri_bigowl + "hasDataType"),
                        rdflib.URIRef(uri_bigowl + str(parameter["type"]).capitalize()),
                    )
                )
                g.add((rdflib.URIRef(uri_bigowl + "hasDataType"), RDF.type, OWL.ObjectProperty))
            else:
                print(
                    '--> ERROR: type parameter not found in list_parametre_type: "string", "number", "integer", "float", "boolean" '
                )
                print("Path: " + path)
                print(
                    "--> Parameter: "
                    + str(parameter["name"])
                    + " type: "
                    + str(parameter["type"])
                )
                print(
                    "NOTE: if ontology was changed, please change list_parametre_type in main.py"
                )
                print(
                    "Please check "
                    + os.getcwd()
                    + "/log_annotation.txt "
                    + "for more errors"
                )
                
                error_in_modelage += 1

            g.add(
                (
                    rdflib.URIRef(uri_bigowl + str(parameter["type"]).capitalize()),
                    RDF.type,
                    rdflib.URIRef(uri_bigowl + "PrimitiveType"),
                )
            )
            if "defaultValue" in parameter:
                if ".inputs." in (parameter["defaultValue"]):
                    for input in annotation["inputs"]:
                        if input["name"] == parameter["defaultValue"].split(".")[2]:
                            g.add(
                                (
                                    rdflib.URIRef(uri_parameter),
                                    rdflib.URIRef(uri_bigowl + "hasDefaultValue"),
                                    rdflib.Literal(str(input["path"])),
                                )
                            )
                else:
                    g.add(
                        (
                            rdflib.URIRef(uri_parameter),
                            rdflib.URIRef(uri_bigowl + "hasDefaultValue"),
                            rdflib.Literal(str(parameter["defaultValue"])),
                        )
                    )
            g.add((rdflib.URIRef(uri_bigowl + "hasDefaultValue"), RDF.type, OWL.DatatypeProperty))

        list_data_type = {
            "bin": "Bin",
            "fastq": "Fastq",
            "image": "Image",
            "map": "Map",
            "pdf": "Pdf",
            "rar": "Rar",
            "sav": "Sav",
            "shp": "Shp",
            "tempfile": "Tempfile",
            "text": "Text",
            "datasetclass": "Datasetclass",
            "tabulardataset": "Tabulardataset",
            "doc": "Doc",
            "html": "HTML",
            "json": "Json",
            "rdf": "RDF",
            "xml": "XML",
            "tiff": "Tiff",
            "zip": "Zip",
        }

        for input in annotation["inputs"]:
            input_uuid = uuid.uuid1()
            uri_input = (
                uri_enbic2lab
                + (str(input["label"])).replace(" ", "_")
                + "_"
                + str(input_uuid)
            )
            if input["type"] in list_data_type:
                g.add(
                    (
                        rdflib.URIRef(uri_input),
                        RDFS.label,
                        rdflib.Literal(str(input["label"])),
                    )
                )
                g.add(
                    (
                        rdflib.URIRef(uri_input),
                        rdflib.URIRef(uri_bigowl + "hasName"),
                        rdflib.Literal(str(input["name"])),
                    )
                )
                g.add(
                    (
                        rdflib.URIRef(uri_input),
                        RDF.type,
                        rdflib.URIRef(
                            uri_enbic2lab + (list_data_type[input["type"].lower()])
                        ),
                    )
                )
                g.add(
                    (
                        rdflib.URIRef(uri_component),
                        rdflib.URIRef(uri_bigowl + "specifiesInputClass"),
                        rdflib.URIRef(uri_input),
                    )
                )

        for output in annotation["outputs"]:
            output_uuid = uuid.uuid1()
            uri_output = (
                uri_enbic2lab
                + (str(output["label"])).replace(" ", "_")
                + "_"
                + str(output_uuid)
            )
            if output["type"] in list_data_type:
                g.add(
                    (
                        rdflib.URIRef(uri_output),
                        RDFS.label,
                        rdflib.Literal(str(output["label"])),
                    )
                )
                g.add(
                    (
                        rdflib.URIRef(uri_output),
                        rdflib.URIRef(uri_bigowl + "hasName"),
                        rdflib.Literal(str(output["name"])),
                    )
                )
                g.add(
                    (
                        rdflib.URIRef(uri_output),
                        RDF.type,
                        rdflib.URIRef(
                            uri_enbic2lab + (list_data_type[output["type"].lower()])
                        ),
                    )
                )
                g.add(
                    (
                        rdflib.URIRef(uri_component),
                        rdflib.URIRef(uri_bigowl + "specifiesOutputClass"),
                        rdflib.URIRef(uri_output),
                    )
                )

        if error_in_modelage != 1:
            g = graph

    except Exception as e:
        print("ERROR: " + str(e))
        print(
            "NOTE: if ontology was changed, please change list_parametre_type in main.py"
        )
        print(
            "Please check " + os.getcwd() + "/log_annotation.txt " + "for more errors"
        )
        

        g = graph

    return g


def main(schema):

    g = Graph()

    with open("log_annotation.txt", "w") as file:
        file.write("Annotation.json Schema Compliance \n\n")

    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if "annotation.json" in file:
                (graph_rdf(os.path.join(root, file), g, schema))

    hash = uuid.uuid1()
    owl_file = open(
        "ontology_enbic2lab.owl",
        "w",
    )
    owl_file.write(g.serialize(format="nt"))
    owl_file.close()


if __name__ == "__main__":

    __version__ = "0.1.0"
    __group__ = "Khaos Research <khaos.uma.es>"

    HEADER = "\n".join(
        [
            r"    _     _ _      ___  __    __  __     ",
            r"   | |__ (_) |_   /___\/ / /\ \ \/ /     ",
            r"   | '_ \| | __| //  //\ \/  \/ / /      ",
            r"   | |_) | | |_ / \_//  \  /\  / /___    ",
            r"   |_.__/|_|\__|\___/    \/  \/\____/    ",
            "                                          ",
            f" Ver. {__version__}  Group. {__group__}  ",
            "                                          ",
        ]
    )
    print(HEADER)

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "description": "Specifies the category of the component within the data workflow.",
                "enum": [
                    "DataProcessing",
                    "DataAnalysing",
                    "DataSink",
                    "DataCollection",
                    "DataFlow",
                ],
            },
            "name": {"type": "string", "description": "Name of the component."},
            "label": {
                "type": "string",
                "description": "A concise, descriptive name for the component that will be displayed in user interfaces.",
            },
            "description": {
                "type": "string",
                "description": "A detailed description of the component's purpose and functionality.",
            },
            "license": {
                "type": "string",
                "description": "Software license governing the component's use and distribution.",
            },
            "version": {
                "type": "string",
                "description": "The release version of the component, following semantic versioning when applicable.",
                "default": "0.0.1",
            },
            "dockerImage": {
                "type": "string",
                "description": "The full identifier for the Docker image used to execute the component, including the repository and tag.",
                "default": "docker.io/docker/hello-world:latest",
            },
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "description": "An array of keywords to facilitate search and categorization of the component.",
                "uniqueItems": True,
            },
            "parameters": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The technical name used internally by the component to identify the parameter.",
                        },
                        "label": {
                            "type": "string",
                            "description": "A readable name for the parameter used in user interfaces.",
                        },
                        "description": {
                            "type": "string",
                            "description": "Explains what the parameter does and how it affects the component's behavior.",
                        },
                        "type": {
                            "type": "string",
                            "description": "Specifies the expected data type for the parameter value.",
                            "enum": ["string", "number", "integer", "float", "boolean"],
                        },
                        "required": {
                            "type": "boolean",
                            "description": "Whether the parameter must be provided for the component to function.",
                        },
                        "defaultValue": {
                            "type": "string",
                            "description": "Provides a default value for the parameter, to be used when no value is explicitly provided.",
                            "properties": {},
                        },
                    },
                    "required": ["name", "label", "description", "type", "required"],
                    "description": "Parameters that can be configured for the component.",
                },
                "uniqueItems": True,
            },
            "inputs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name identifying each input required by the component.",
                        },
                        "label": {
                            "type": "string",
                            "description": "A label providing a human-readable name for the input.",
                        },
                        "path": {
                            "type": "string",
                            "description": "The location or source path where the input data can be found.",
                        },
                        "type": {
                            "type": "string",
                            "description": "The data type of the input.",
                            "enum": [
                                "bin",
                                "fastq",
                                "image",
                                "map",
                                "pdf",
                                "rar",
                                "sav",
                                "shp",
                                "tempfile",
                                "text",
                                "datasetclass",
                                "tabulardataset",
                                "doc",
                                "html",
                                "json",
                                "rdf",
                                "xml",
                                "tiff",
                                "zip",
                            ],
                        },
                    },
                    "required": ["name", "label", "path", "type"],
                    "description": "Input data sources for the component.",
                },
            },
            "outputs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name identifying each output generated by the component.",
                        },
                        "label": {
                            "type": "string",
                            "description": "A label providing a human-readable name for the output.",
                        },
                        "path": {
                            "type": "string",
                            "description": "The destination path where output data will be written.",
                        },
                        "type": {
                            "type": "string",
                            "description": "The data type of the output.",
                            "enum": [
                                "bin",
                                "fastq",
                                "image",
                                "map",
                                "pdf",
                                "rar",
                                "sav",
                                "shp",
                                "tempfile",
                                "text",
                                "datasetclass",
                                "tabulardataset",
                                "doc",
                                "html",
                                "json",
                                "rdf",
                                "xml",
                                "tiff",
                                "zip",
                            ],
                        },
                    },
                    "required": ["name", "label", "path", "type"],
                    "description": "Output data destinations for the component.",
                },
            },
            "mainScriptPath": {
                "type": "string",
                "description": "The filesystem path to the executable script.",
            },
            "testPath": {
                "type": "string",
                "description": "The filesystem path to the component's test script or suite.",
            },
            "dependencies": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of an external library or service that this component relies on-",
                        },
                        "version": {
                            "type": "string",
                            "description": "The specified version of the dependency that is known to be compatible with this component.",
                        },
                        "license": {
                            "type": "string",
                            "description": "The license governing the dependency, which may impact the overall licensing of the component.",
                        },
                        "url": {
                            "type": "string",
                            "description": "A URL or other locator where the dependency can be accessed or reviewed.",
                        },
                    },
                    "required": ["name", "version", "license"],
                    "description": "Dependencies required to run the component.",
                },
            },
            "resources": {
                "type": "object",
                "properties": {
                    "cores": {
                        "type": "integer",
                        "description": "The number of CPU cores requested for processing.",
                    },
                    "memory": {
                        "type": "integer",
                        "description": "The quantity of RAM required for the component, specified in Megabytes (MB).",
                    },
                    "gpuNeeded": {
                        "type": "boolean",
                        "description": "Flag to indicate whether the component requires GPU support.",
                        "default": False,
                    },
                    "gpuMemory": {
                        "type": ["integer", "null"],
                        "description": "The amount of GPU memory required, specified in Megabytes (MB), applicable if `gpuNeeded` is true.",
                    },
                    "estimatedTimeInMin": {
                        "type": "integer",
                        "description": "An approximate time in minutes that the component will take to execute.",
                    },
                },
                "required": [
                    "cores",
                    "memory",
                    "gpuNeeded",
                    "gpuMemory",
                    "estimatedTimeInMin",
                ],
                "description": "Resource requirements for running the component.",
            },
            "publicationDate": {
                "type": "string",
                "format": "date-time",
                "description": "The date and time when the component was officially made available.",
            },
            "author": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "Author email."},
                    "affiliation": {
                        "type": "string",
                        "description": "The institution or organization with which the author is associated.",
                    },
                },
                "required": ["email", "affiliation"],
                "description": "Identifies the individual or organization responsible for creating the component.",
            },
            "contributor": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "type": "string",
                            "format": "email",
                            "default": "Contact email.",
                            "description": "Contributor email.",
                        },
                        "affiliation": {
                            "type": "string",
                            "description": "The institution or organization with which the contributor is associated.",
                        },
                    },
                    "required": ["email"],
                },
                "description": "Contact information for the component's author or maintainers.",
            },
        },
        "required": [
            "type",
            "name",
            "label",
            "description",
            "license",
            "version",
            "dockerImage",
            "outputs",
            "mainScriptPath",
            "dependencies",
            "resources",
            "publicationDate",
            "author",
            "contributor",
        ],
    }

    main(schema)
