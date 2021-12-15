import os
import json
import sys


DATA_DIRECTORY = sys.argv[1]
JSON_DATA_DIRECTIRY = sys.argv[2]


def serialize_taiga_ru(location):
    file_names = os.listdir(location)
    data = []
    for elem in file_names:
        with open(f"{location}/{elem}", "r") as data_file:
            data.append((elem, data_file.read()))
    return data


def save_data(data, location):
    with open(location, "w") as data_file:
        json.dump(data, data_file)


def main():
    serialized_data = serialize_taiga_ru(DATA_DIRECTORY)
    save_data(serialized_data, JSON_DATA_DIRECTIRY)


if __name__ == '__main__':
    main()