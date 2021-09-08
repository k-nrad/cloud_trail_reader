from cloud_trail_reader.reader import count_operations


def test_happy_path():
    assert count_operations(
        'test/fixtures/cloud_trail_records.json.gz') == {
           "arn:aws:iam::121212121212:user/test_user": {"UploadPart": 1, "GetObject": 1}}


def test_should_skip_file_if_not_json():
    assert count_operations('test/fixtures/not_json.gz') == {}


def test_should_skip_file_if_not_gzip():
    assert count_operations('test/fixtures/not_gzip.gz') == {}


def test_should_skip_file_if_json_gzip_file_content_is_wrong():
    assert count_operations('test/fixtures/bad_json_gzip_content.json.gz') == {}
