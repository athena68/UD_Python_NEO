"""Write data to CSV and JSON files.

The `write_to_csv` function exports a collection of close approaches to a CSV file.
The `write_to_json` function exports a collection of close approaches to a JSON file.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A path to the CSV file to write.
    """
    fieldnames = [
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    ]
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for approach in results:
            writer.writerow({
                'datetime_utc': approach.time_str,
                'distance_au': approach.distance,
                'velocity_km_s': approach.velocity,
                'designation': approach.neo.designation,
                'name': approach.neo.name if approach.neo.name else '',
                'diameter_km': approach.neo.diameter if approach.neo else 'nan',
                'potentially_hazardous': 'Yes' if approach.neo and approach.neo.hazardous else 'No',
            })


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A path to the JSON file to write.
    """
    data = []
    for approach in results:
        data.append({
            'datetime_utc': approach.time_str,
            'distance_au': approach.distance,
            'velocity_km_s': approach.velocity,
            'neo': {
                'designation': approach.neo.designation,
                'name': approach.neo.name if approach.neo.name else '',
                'diameter_km': approach.neo.diameter if approach.neo else 'nan',
                'potentially_hazardous': approach.neo.hazardous if approach.neo else False,
            }
        })

    with open(filename, mode='w') as file:
        json.dump(data, file, indent=2)
