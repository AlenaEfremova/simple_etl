import os
import csv
import json
import argparse
from xml.etree import ElementTree


def parser_cmd():
    """Parses command line arguments"""

    parser = argparse.ArgumentParser(prog='simple_etl',
                                     description='The program is a simple ETL with different file formats.')
    parser.add_argument('-i', '--in_files', nargs='*', type=argparse.FileType('r'),
                        required=True, help='files with different formats')
    parser.add_argument('-ob', '--out_basic', type=argparse.FileType('w'),
                        help='optional file path for recording results')
    parser.add_argument('-oa', '--out_advanced', type=argparse.FileType('w'),
                        help='optional file path for recording results')
    args = parser.parse_args()
    return args


def open_file(file):
    """Opens a file and converts it to a dictionary list,
    acceptable file types '.csv', '.json', '.xml'
    """

    lst_of_dicts = list()

    if os.path.splitext(file)[1] == ".csv":
        with open(file, 'r') as csv_file:
            reader_csv = csv.DictReader(csv_file)
            lst_of_dicts = list(reader_csv)

    elif os.path.splitext(file)[1] == ".json":
        with open(file, newline='') as json_file:
            reader_json = json.load(json_file)
            lst_of_dicts = reader_json['fields']

    elif os.path.splitext(file)[1] == ".xml":
        tree = ElementTree.parse(file)
        root = tree.getroot()
        lst_of_dicts = list()
        for obs in root.findall(".//objects"):
            dict_xml = dict()
            for obj in obs:
                dict_xml[obj.attrib['name']] = obj.find('value').text
            lst_of_dicts.append(dict_xml)
    else:
        print("Acceptable file types: '.csv', '.json', '.xml'")
    return lst_of_dicts


def list_intersection(list_of_lists):
    """Looking for intersection of keys that are present in all
    dictionary lists, generates one list of dictionaries with
    these keys and their values
    """

    inter_keys = list_of_lists[0][0].keys()

    for lst in list_of_lists:
        inter_keys &= lst[0].keys()

    list_of_dicts = list()
    for lst in list_of_lists:
        list_of_dicts.extend([{key: dct[key] for key in inter_keys} for dct in lst])
    return list_of_dicts


def sorted_list_of_dicts(list_of_dicts, key):
    """Sorts by dictionary key, and then by the values of the specified key"""

    key_sorted_dicts = [{k: dct[k] for k in sorted(dct)} for dct in list_of_dicts]
    dicts_sorted_by_val = sorted(key_sorted_dicts, key=lambda i: i[key])
    return dicts_sorted_by_val


def write_tsv(list_of_dicts, pathname):
    """Writes the list of dictionaries into the '.tsv' file"""

    with open(pathname, 'w') as out_file:
        tsv_writer = csv.DictWriter(out_file, delimiter='\t', fieldnames=list_of_dicts[0].keys())
        tsv_writer.writeheader()
        tsv_writer.writerows(list_of_dicts)


def key_separation(list_of_keys):
    """Divides the list of keys into two, a list in which the key names begin with a 'D'
    and a list where the key names begin with an 'M'
    """

    keys_with_d, keys_with_m = list(), list()
    for key in list_of_keys:
        if key.startswith('D'):
            keys_with_d.append(key)
        elif key.startswith('M'):
            keys_with_m.append(key)
    return keys_with_d, keys_with_m


def value_conversion(list_of_dicts):
    """Conversion of values by specified keys to 'int' type"""

    _, keys_with_m = key_separation(list_of_dicts[0].keys())
    converted_list = list()
    for dct in list_of_dicts:
        new_dct = dict()
        for key, value in dct.items():
            if key in keys_with_m:
                try:
                    value = int(value)
                except ValueError as err:
                    print('The {} column contains {}'.format(key, err))
                    value = 0
            new_dct[key] = value
        converted_list.append(new_dct)
    return converted_list


def dictionary_comparison(list_of_dicts):
    """Sums the values corresponding to the specified dictionary keys
    by unique combinations of dictionary values
    and forms a new list of dictionaries
    """

    keys_with_d, keys_with_m = key_separation(list_of_dicts[0].keys())
    multi_key_dict = dict()
    for dct in list_of_dicts:
        key = tuple([dct.get(key) for key in keys_with_d])
        if key in multi_key_dict:
            value = [dct.get(key) for key in keys_with_m]
            multi_key_dict[key] = list(map(lambda a, b: a + b, multi_key_dict[key], value))
        else:
            multi_key_dict[key] = [dct.get(key) for key in keys_with_m]
    transformed_list_of_dicts = list()

    for keys, values in multi_key_dict.items():
        dct = dict()
        for key, d in zip(keys, keys_with_d):
            dct[d] = key
        for val, m in zip(values, keys_with_m):
            dct[m.replace('M', 'MS')] = val
        transformed_list_of_dicts.append(dct)
    return transformed_list_of_dicts


def main():
    args = parser_cmd()
    list_of_lists = list()

    for arg in args.in_files:
        file = arg.name
        list_of_lists.append(open_file(file))

    # ----------------The first part----------------
    intersect_list_of_dicts = list_intersection(list_of_lists)
    sorted_list_by_value = sorted_list_of_dicts(intersect_list_of_dicts, 'D1')
    if args.out_basic is not None:
        write_tsv(sorted_list_by_value, args.out_basic.name)
    else:
        write_tsv(sorted_list_by_value, 'result_basic.tsv')

    # ----------------The second  part--------------
    convert_val = value_conversion(sorted_list_by_value)
    processed_list = dictionary_comparison(convert_val)
    if args.out_basic is not None:
        write_tsv(processed_list, args.out_advanced.name)
    else:
        write_tsv(processed_list, 'result_advanced.tsv')


if __name__ == "__main__":
    main()
