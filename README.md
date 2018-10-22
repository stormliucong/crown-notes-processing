# Crown Notes Parser For EHR-Phenolyzer

This project is to parse the crown notes using NLP techniques and extract phenotype, disease, cytoband and gene information.
This is a collabrative project between Cong Liu (Chunhua Weng's team) and Luda (Carrol's team)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- python3.6 is used to parse the notes
- original html files are parsed from crown_472.txt (provided by Alla, stored in AQUA)
- genetic notes are identified by searching provider's name (provided by Jung, see email)


### dictionary-generator

- cytoband was downloaded from http://hgdownload.cse.ucsc.edu/goldenpath/hg38/database/cytoBand.txt.gz 
- hgnc was downloaded from https://biomart.genenames.org/martform/#!/default/HGNC?datasets=hgnc_gene_mart
- hpo was downloaded from http://purl.obolibrary.org/obo/hp.owl
- orphanet was downloaded from https://www.ebi.ac.uk/ols/ontologies/ordo
- omim was downloaded from https://www.omim.org/downloads/


## Authors

* **Cong Liu** - *Initial work* 