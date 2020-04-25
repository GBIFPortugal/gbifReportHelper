#!/usr/bin/python -tt
# coding=utf-8

'''
  Author: Rui Figueira

  Project: gbifReportHelper
  Get the number of downloads and downloaded records for all datasets endorsed by a node (via publisher).

  File: gbifStat_datasetsTable.py

  Specifics:
  - define in the command the nodeKey and year for which statistics are to be retrieved
  - call GBIF API to get a list of datasets for a certain node
  - call GBIF API to get downloads for each dataset, and determnine number of nodes and number of donwloaded records
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


# obtain number of downloads and number of downloaded records for the dataset
def gbifDownload(datasetKey, yearStats):
    endOfRecords = False
    offset = 0
    limit = 20
    address = 'http://api.gbif.org/v1/occurrence/download/dataset/' + datasetKey
    print(address)
    countRec = 0
    countDwl = 0
    year = 9999
    while endOfRecords == False and year >= yearStats:
        try:
            parms = {'offset': offset, 'limit': limit}
            try:
                txt = requests.get(address, params = parms)
            except IOError:
                print('problema no acesso ao GBIF: código:', txt.raise_for_status())
            parsed_json = json.loads(txt.text)
            endOfRecords = parsed_json['endOfRecords']
            results = parsed_json['results']
            i = 0
            for x in results:
                yearStr = results[i]["download"]["created"]
                count = results[i]["numberRecords"]
                year = int(yearStr[0:4])
                print ('yearStats in gbifdownl: ' + str(yearStats))
                print ('yearStr in gbifdownl: ' + yearStr)
                # skip if year is higher that the year for statistics
                if year > yearStats:
                    print('year > yearStats')
                elif year == yearStats:
                    countDwl += 1
                    countRec += count
                    print ('countDwl: ' + str(countDwl))
                    print ('countRec: ' + str(countRec))
                # stop if year is lower than the input year for statistics
                else:
                    break
                i += 1
            offset += 20
        except ValueError:
            print ('ValueError on gbifDownload')
    return (countDwl, countRec)

# obtain the list of datasets for the node
def gbifGetDatasets(nodeKey):
    endOfRecords = False
    offset = 0
    limit = 20
    address = 'http://api.gbif.org/v1/node/' + nodeKey + '/dataset'
    print (address)
    listaDatasets = []
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
                line = [results[i]["key"], results[i]["type"], results[i]["publishingOrganizationKey"], results[i]["title"], results[i]["created"], results[i]["modified"], results[i]["license"]]
                listaDatasets.append(line)
                i += 1
            offset += 20
        except ValueError:
            print ('ValueError on gbifGetDatasets')
    return listaDatasets


def main():
    if len(sys.argv) >= 3:
        nodeKey = sys.argv[1]
        yearRelat = sys.argv[2]
    else:
        print ("Run command: python gbifStat_dataset.py [nodeKey] [year]\nExample: python gbifStat_dataset.py 673f7038-4262-4149-b753-5658a4e912f6 2019")
        nodeKey = '673f7038-4262-4149-b753-5658a4e912f6'
        yearRelat = 2019
    listaDatasets = gbifGetDatasets(nodeKey)
    print ("Existem " + str(len(listaDatasets)) + "datasets.")
    filename = "stats_count_" + nodeKey + ".csv"
    i = 0
    with open(filename, "w") as file:
        file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(['ID','publishingOrganizationKey','datasetKey','license','title','type','modified','n_records','n_downloads','n_downloadeRecords'])
        for lista in listaDatasets:
            i =+ 1
            yearCreated = int(lista[4][0:4])
            print ("yearCreated: " + lista[4][0:4])
            # skip dataset if year of creation is higher than the input year for statistcs
            if yearCreated <= yearRelat:
                # if datasest are of type Occurrence or Sampling Event
                if str(lista[1]) == "OCCURRENCE" or str(lista[1]) == "SAMPLING_EVENT":
                    print (lista[1])
                    counts =  gbifDownload(lista[0], yearRelat)
                    line = (i, lista[2], lista[0], lista[6], lista[3], lista[1],lista[5][0:10],counts[0], counts[1])
                    file_writer.writerow(line)
                else:
                    print (lista[1])
                    line = (i, lista[2], lista[0], lista[6], lista[3], lista[1],lista[5][0:10])
                    file_writer.writerow(line)


if __name__ == '__main__':
    main()
