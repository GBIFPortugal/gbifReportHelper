#!/usr/bin/python -tt
# coding=utf-8

'''
  Author: Rui Figueira

  Project: gbifReportHelper
  Get the number of downloads and downloaded records for all datasets endorsed by a node (via publisher).

  File: gbifStat_organisationsTable.py

  Specifics:
  - define in the command the nodeKey and year for which statistics are to be retrieved
  - call GBIF API to get a list of organisations for a certain node
  - Details of the GBIF API at https://www.gbif.org/developer/registry

  ToDo:
  - obtain statistics for CHECKLISTS

  Assumptions:
  - the nodeKey of the node for which dataset statistics will be retrieved is known. This can be obtained from https://api.gbif.org/v1/node

'''

import os
import sys
import json
import requests
import csv
import argparse


# obtain the list of datasets for the node
def gbifGetNodeOrg(nodeKey):
    endOfRecords = False
    offset = 0
    limit = 20
    address = 'https://api.gbif.org/v1/organization?country=PT'
    print (address)
    listaOrgs = []
    while endOfRecords == False:
        try:
            parms = {'offset': offset, 'limit': limit}
            try:
                txt = requests.get(address, params = parms)
            except IOError:
                print ('problema no acesso ao GBIF: código:', txt.raise_for_status())
            parsed_json = json.loads(txt.text)
            endOfRecords = parsed_json['endOfRecords']
            results = parsed_json['results']
            i = 0
            for x in results:
                line = [results[i]["key"], results[i]["title"]]
                listaOrgs.append(line)
                i += 1
            offset += 20
        except ValueError:
            print ('ValueError on gbifGetNodeDatasets')
    return listaOrgs


def main():

    parser = argparse.ArgumentParser(description = "Help on how to use this script ")
    parser.add_argument("-n", "--nodeKey", help = "GUID of the node. Example: 673f7038-4262-4149-b753-5658a4e912f6", required = False, default = "673f7038-4262-4149-b753-5658a4e912f6")
    parser.add_argument("-o", "--organizationKey", help = "GUID of the organization. Example: dfad10f6-d84b-4fa2-b6d0-df2a3eb38b65", required = False, default = "dfad10f6-d84b-4fa2-b6d0-df2a3eb38b65")
    parser.add_argument("-y", "--year", type=int, help = "Year of report. Example: 2019", required = False, default = "2019")

    argument = parser.parse_args()
    status = False
    print(argument.year)
    print(argument.nodeKey)

    yearRelat = argument.year
    listaDatasets = gbifGetNodeOrg(argument.nodeKey)
    filename = "stats_org_" + str(argument.year) + "_" + argument.nodeKey + ".csv"
    i = 1
    with open(filename, "w") as file:
        file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(['ID','publishingOrganizationKey','title'])
        for lista in listaDatasets:
            line = (i, lista[0], lista[1])
            file_writer.writerow(line)
            print(line)
            i =+ 1


if __name__ == '__main__':
    main()
