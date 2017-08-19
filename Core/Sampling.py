import os
from Core.Dataset import Dataset
from Core.DataFiles import DataFiles

def sampling(datasets, file_metadata, file_data):
    resultFiles = DataFiles(file_metadata, file_data)
    for dataset in datasets:
        ds = Dataset(dataset, resultFiles)
        ds.sampling()

    resultFiles.save()
