# gbifReportHelper
This project contains helper scripts to prepare the GBIF.pt yearly report

### gbifStat_datasetsTable.py
This script creates a table with information about the datasets published by a GBIF country's publishers. Using the GBIF API Registry, it gets the number of downloads and downloaded records for a certain year. It runs with python 3.

The created table includes the following columns
- ID
- publishingOrganizationKey - key of the publisher organisation
- datasetKey - key of the dataset
- license - license of the dataset
- title - title of the dataset
- type - dataset type: occurrences, sample based, checklist
- created - creation date of the dataset
- modified - last modification date
- n_records - number of records in the dataset
- n_recordsGeo - number of georeferenced records
- n_downloads - number of GBIF downloads that included records from the dataset
- n_downloadeRecords - number of downloaded records

Run command:

usage: `gbifStat_datasetsTable.py [-h] [-n NODEKEY] [-o ORGANIZATIONKEY]
                                 [-y YEAR]`

Help on how to use this script

optional arguments:
```  -h, --help            show this help message and exit
  -n NODEKEY, --nodeKey NODEKEY
                        GUID of the node. Example:
                        673f7038-4262-4149-b753-5658a4e912f6
  -o ORGANIZATIONKEY, --organizationKey ORGANIZATIONKEY
                        GUID of the organization. Example:
                        dfad10f6-d84b-4fa2-b6d0-df2a3eb38b65
  -y YEAR, --year YEAR  Year of report. Example: 2019```
