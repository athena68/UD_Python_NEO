"""Extract data from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file. Each row in the CSV
file represents a near-Earth object.

The `load_approaches` function extracts close approach data from a JSON file.
Each dictionary in the JSON list represents a close approach to Earth by an NEO.

These functions convert the data in these input files into structured Python
objects - `NearEarthObject`s and `CloseApproach`es.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neos = []
    with open(neo_csv_path, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Pass raw data to the NearEarthObject constructor
            neos.append(NearEarthObject(
                designation=row['pdes'],
                name=row['name'] or None,
                diameter=row['diameter'],  # Let the constructor handle type conversion
                hazardous=row['pha']      # Pass raw 'Y' or 'N' to the constructor
            ))
    return neos


def load_approaches(ca_json_path):
    """Read close approach data from a JSON file.

    :param ca_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    approaches = []
    with open(ca_json_path, mode='r') as file:
        data = json.load(file)
        for approach in data['data']:
                approaches.append(CloseApproach(
                    designation=approach[0],  # Example: '2020 AY1'
                    time=approach[3],        # Example: '2020-Jan-01 00:54'
                    distance=float(approach[4]),  # Example: '0.0211660525256395'
                    velocity=float(approach[7])   # Example: '5.62203195551878'
                ))
    return approaches
