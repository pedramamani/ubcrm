import json
import csv


def json_to_csv(json_file, csv_filename):
    """
    Convert a two-level deep .json file to a .csv file
    :param json_file: with depth of two
    :param csv_filename: to save the .csv output file
    """
    data = json.load(json_file)
    writer = csv.writer(open("assets/" + csv_filename, 'w+', newline=''))

    writer.writerow(['#'] + list(list(data.values())[0]))
    for item, item_info in data.items():
        writer.writerow([item] + list(item_info.values()))
