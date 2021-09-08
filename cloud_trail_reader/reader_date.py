import json
import gzip
from json.decoder import JSONDecodeError
from pathlib import Path
import csv
import os
import datetime


def files_paths(path):
    # input: path to file folder (folder could include subfolders)
    # output: list of paths to every file in the indicated folder
    list_of_paths = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            list_of_paths.append(os.path.join(root, name))
    return list_of_paths


def list_of_operations(file_path):
    # input: the single-file path
    # output: list of values from a single file: [[date, user_name, event_name],[date, user_name, event_name],...]
    result = []
    file_path = Path(file_path)
    with gzip.open(file_path, "r") as f:
        try:
            data = f.read()
            json_content = json.loads(data.decode('utf-8'))
        except (JSONDecodeError, gzip.BadGzipFile):
            # if the file is not a valid json or gzip, we don't count operations and just skip it
            return []
        for n in json_content['Records']:
            try:
                user_name = (n['userIdentity']['arn'])
                event_name = (n['eventName'])
                event_time = (n['eventTime'])
                day = datetime.datetime.strptime(event_time[:10], '%Y-%m-%d')
            except KeyError:
                continue
            result.append([str(day)[:10], user_name, event_name])
    return result


def count_operations_in_all_files(folder_path):
    # input: path to file folder (folder could include subfolders)
    # output: counting events to an external dictionary (final_result) by the date of the event and the user name
    for path in files_paths(folder_path):
        single_file = list_of_operations(path)
        for item in single_file:
            date_user_name = item[0]+item[1]
            op_name = item[2]
            if date_user_name not in final_result:
                final_result[date_user_name] = {}
            if op_name not in final_result[date_user_name]:
                final_result[date_user_name][op_name] = 0
            final_result[date_user_name][op_name] += 1


def save_results_to_csv(file_name):
    # input: name of new csv file
    # output: csv file with header
    with open(file_name, 'w') as csv_file:
        csv_file.write('date'+','+'user_name'+',')
        csv_columns = ["ListObjects", "UploadPart", "CreateMultipartUpload", "CompleteMultipartUpload",
                       "AbortMultipartUpload", "GetObject", "DeleteObject", "HeadObject", "GetObjectTagging"]
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()
        for date_user_name, operations in final_result.items():
            csv_file.write(date_user_name[:10]+','+date_user_name[10:])
            writer.writerow(operations)


if __name__ == '__main__':

    final_result = {}

    print('Hello')
    file_path = input('Indicate the path of the folder with the files >>')
    result_csv = input('Indicate the name of result csv file >>')
    print('Wait...')

    count_operations_in_all_files(file_path)
    save_results_to_csv(result_csv)

    print('Saved file')
