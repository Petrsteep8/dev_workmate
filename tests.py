import pytest
import tempfile
import os
from main import read_csv_data, process_employee_data, payout_report


@pytest.fixture
def sample_csv_file():
    """Creates a temporary CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write("id,email,name,department,hours,rate\n")
        f.write("1,alice@example.com,Alice Johnson,Marketing,160,50\n")
        f.write("2,bob@example.com,Bob Smith,Design,150,40\n")
    yield f.name
    os.unlink(f.name)


def test_read_csv_data(sample_csv_file):
    data = read_csv_data(sample_csv_file)
    assert len(data) == 2
    assert data[0]['name'] == 'Alice Johnson'
    assert data[0]['department'] == 'Marketing'
    assert data[0]['hours'] == '160'
    assert data[0]['rate'] == '50'
    assert data[1]['name'] == 'Bob Smith'
    assert data[1]['department'] == 'Design'


def test_process_employee_data():
    sample_data = [
        {'name': 'Alice Johnson', 'department': 'Marketing', 'hours': '160', 'rate': '50'},
        {'name': 'Bob Smith', 'department': 'Design', 'hours': '150', 'rate': '40'}
    ]
    result = process_employee_data(sample_data)
    assert 'Marketing' in result
    assert 'Design' in result
    assert result['Marketing'][0]['employee_name'] == 'Alice Johnson'
    assert result['Marketing'][0]['hours_worked'] == 160.0
    assert result['Marketing'][0]['hourly_rate'] == 50.0
    assert result['Marketing'][0]['total_pay'] == 8000.0
    assert result['Design'][0]['employee_name'] == 'Bob Smith'
    assert result['Design'][0]['total_pay'] == 6000.0


def test_format_payout_report():
    sample_data = [[
        {'name': 'Alice Johnson', 'department': 'Marketing', 'hours': '160', 'rate': '50'},
        {'name': 'Bob Smith', 'department': 'Design', 'hours': '150', 'rate': '40'}
    ]]
    output = payout_report(sample_data)
    expected_output = (
        "Marketing\n"
        "---------\n"
        "name                  hours   rate   payout\n"
        "Alice Johnson           160     50    $8000\n"
        "--------------------\n"
        "                        160           $8000\n"
        "\n"
        "Design\n"
        "------\n"
        "name                  hours   rate   payout\n"
        "Bob Smith               150     40    $6000\n"
        "--------------------\n"
        "                        150           $6000"
    )
    assert output == expected_output


def test_empty_file():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write("id,email,name,department,hours,rate\n")
    data = read_csv_data(f.name)
    os.unlink(f.name)
    assert data == []
    result = payout_report([data])
    assert result == ""
