import json
import gzip
from json.decoder import JSONDecodeError
import sys
from pathlib import Path
import csv
import os


def files_paths(path):
    list_of_paths = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            list_of_paths.append(os.path.join(root, name))
    return list_of_paths


def count_operations(file_path):
    result = {}
    file_path = Path(file_path)
    with gzip.open(file_path, "r") as f:
        try:
            data = f.read()
            json_content = json.loads(data.decode('utf-8'))
        except (JSONDecodeError, gzip.BadGzipFile):
            # if the file is not a valid json or gzip, we don't count operations and just skip it
            return {}
        for n in json_content['Records']:
            try:
                principal_id = (n['userIdentity']['arn'])
                event_name = (n['eventName'])
            except KeyError:
                continue
            if principal_id not in result:
                result[principal_id] = {}
                result[principal_id][event_name] = 1
            else:
                if event_name not in result[principal_id]:
                    result[principal_id][event_name] = 1
                else:
                    result[principal_id][event_name] = result[principal_id][event_name] + 1
    return result


def count_operations_in_all_files(folder_path):
    for path in files_paths(folder_path):
        one_dict = count_operations(path)
        for user_name, operations in one_dict.items():
            if user_name not in final_result:
                final_result[user_name] = {}
            for op_name, op_count in operations.items():
                if op_name not in final_result[user_name]:
                    final_result[user_name][op_name] = 0
                final_result[user_name][op_name] += op_count


def save_results_to_csv(file_name):
    with open(file_name, 'w') as csv_file:
        csv_file.write('user_name'+',')
        csv_columns = ["ListObjects", "UploadPart", "CreateMultipartUpload", "CompleteMultipartUpload",
                       "AbortMultipartUpload", "GetObject", "DeleteObject", "HeadObject", "GetObjectTagging"]
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()
        for user_name, operations in final_result.items():
            csv_file.write(user_name+',')
            writer.writerow(operations)


if __name__ == '__main__':
    final_result = {}
    print('Hello')
    count_operations_in_all_files(sys.argv[1])
    save_results_to_csv(sys.argv[2])

    print(f'Saved file {sys.argv[2]} in current directory')
