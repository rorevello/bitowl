import json
import jsonschema
import rdflib
import os
import uuid
from rdflib import Graph, Literal, RDFS, RDF, URIRef
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
        g.parse('.../ontology/bigowl.owl',format='xml')


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
            g.add(
                (
                    rdflib.URIRef(uri_implementation),
                    rdflib.URIRef(uri_bigowl + "hasDependency"),
                    rdflib.URIRef(uri_dependecy),
                )
            )
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
            g.add(
                (
                    rdflib.URIRef(uri_dependecy),
                    rdflib.URIRef(uri_bigowl + "hasLicense"),
                    rdflib.Literal(dependecie["license"]),
                )
            )
            g.add(
                (
                    rdflib.URIRef(uri_dependecy),
                    rdflib.URIRef(uri_bigowl + "hasUrl"),
                    rdflib.Literal(dependecie["url"]),
                )
            )
            g.add(
                (
                    rdflib.URIRef(uri_dependecy),
                    rdflib.URIRef(uri_bigowl + "hasLength"),
                    rdflib.Literal(dependecie["name"]),
                )
            )

        # data implementation
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
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasLicense"),
                rdflib.Literal(annotation["license"]),
            )
        )
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasVersion"),
                rdflib.Literal(annotation["version"]),
            )
        )
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasPublicationDate"),
                rdflib.Literal(annotation["publicationDate"]),
            )
        )  # TODO: annotation ??
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "Author"),
                rdflib.Literal(annotation["author"]),
            )
        )
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasCore"),
                rdflib.Literal(annotation["resources"]["cores"]),
            )
        )
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasMemory"),
                rdflib.Literal(annotation["resources"]["memory"]),
            )
        )
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasGPUMemory"),
                rdflib.Literal(annotation["resources"]["gpuMemory"]),
            )
        )
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasGPUNeed"),
                rdflib.Literal(annotation["resources"]["gpuNeeded"]),
            )
        )
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasEstimatedTimeInMin"),
                rdflib.Literal(annotation["resources"]["estimatedTimeInMin"]),
            )
        )
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasMainScriptPath"),
                rdflib.Literal(annotation["mainScriptPath"]),
            )
        )
        g.add(
            (
                rdflib.URIRef(uri_implementation),
                rdflib.URIRef(uri_bigowl + "hasTestPath"),
                rdflib.Literal(annotation["testPath"]),
            )
        )

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
            print("\n")

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

        # g.add((rdflib.URIRef(uri_component), Namespace.name, rdflib.Literal(str(annotation['name']))))
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
        g.add(
            (
                rdflib.URIRef(uri_component),
                rdflib.URIRef(uri_bigowl + "hasAlgorithm"),
                rdflib.URIRef(uri_algorithm),
            )
        )
        g.add((rdflib.URIRef(uri_component),rdflib.URIRef(uri_bigowl + "hasTag"),rdflib.Literal(annotation["tags"])))

        g.add(
            (
                rdflib.URIRef(uri_component),
                rdflib.URIRef(uri_bigowl + "hasNumberOfInputs"),
                rdflib.Literal(len(annotation["inputs"])),
            )
        )
        g.add(
            (
                rdflib.URIRef(uri_component),
                rdflib.URIRef(uri_bigowl + "hasNumberOfOutputs"),
                rdflib.Literal(len(annotation["outputs"])),
            )
        )

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
            g.add((

                rdflib.URIRef(uri_component),rdflib.URIRef(uri_bigowl + "hasParameter"),rdflib.URIRef(uri_parameter)
            ))
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
                print("\n")
                error_in_modelage += 1

            g.add(
                (
                    rdflib.URIRef(uri_bigowl + str(parameter["type"]).capitalize()),
                    RDF.type,
                    rdflib.URIRef(uri_bigowl + "PrimitiveType"),
                )
            )
            if "defaultValue" in parameter:
                """if ".inputs." in (parameter["defaultValue"]):
                    for input in annotation["inputs"]:
                        if input["name"] == parameter["defaultValue"].split(".")[2]:
                            g.add(
                                (
                                    rdflib.URIRef(uri_parameter),
                                    rdflib.URIRef(uri_bigowl + "hasDefaultValue"),
                                    rdflib.Literal(str(input["path"])),
                                )
                            )
                else:"""
                g.add(
                        (
                            rdflib.URIRef(uri_parameter),
                            rdflib.URIRef(uri_bigowl + "hasDefaultValue"),
                            rdflib.Literal(str(parameter["defaultValue"])),
                        )
                    )

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
            "docx": "Docx",
            "xlsx": "Xlsx",
            "html": "HTML",
            "json": "Json",
            "rdf": "RDF",
            "xml": "XML",
            "tiff": "Tiff",
            "zip": "Zip",
        }
        #TODO:CREAR las clases Docx yXlsx en bigOwl

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
                        rdflib.URIRef(uri_bigowl + "hasPath"),
                        rdflib.Literal(str(input["path"])),
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
                g.add(
                    (
                        rdflib.URIRef(uri_output),
                        rdflib.URIRef(uri_bigowl + "hasPath"),
                        rdflib.Literal(str(output["path"])),
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
        print("\n")

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
    #abrir json schema externo
    with open("schema.json", "r") as f:
        schema = json.load(f)

    main(schema)
