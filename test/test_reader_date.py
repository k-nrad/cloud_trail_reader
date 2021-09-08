from cloud_trail_reader.reader_date import list_of_operations


def test_happy_path():
    assert list_of_operations(
        'test/fixtures/cloud_trail_records.json.gz') == [
        ['2021-08-31', 'arn:aws:iam::121212121212:user/test_user', 'UploadPart'],
        ['2021-08-31', 'arn:aws:iam::121212121212:user/test_user', 'GetObject']
    ]


def test_should_skip_file_if_not_json():
    assert list_of_operations('test/fixtures/not_json.gz') == []


def test_should_skip_file_if_not_gzip():
    assert list_of_operations('test/fixtures/not_gzip.gz') == []


def test_should_skip_file_if_json_gzip_file_content_is_wrong():
    assert list_of_operations('test/fixtures/bad_json_gzip_content.json.gz') == []


def test_should_skip_wrong_dict_row_among_good_data_in_json_file():
    assert list_of_operations(
        'test/fixtures/cloud_trail_records.json.gz') == [
        ['2021-08-31', 'arn:aws:iam::121212121212:user/test_user', 'UploadPart'],
        ['2021-08-31', 'arn:aws:iam::121212121212:user/test_user', 'GetObject']
    ]
