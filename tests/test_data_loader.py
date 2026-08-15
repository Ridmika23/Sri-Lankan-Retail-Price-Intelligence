import pytest
import pandas as pd
from pathlib import Path
from src.data_loader import load_data, validate_data, generate_quality_report, REQUIRED_COLUMNS

@pytest.fixture
def mock_valid_data():
    return pd.DataFrame({
        'Week': ['2020-01-W1', '2020-01-W2'],
        'Item': ['Rice', 'Dhal'],
        'Unit': ['1 kg', '1 kg'],
        'Avg Price (Rs.)': [100.0, 150.0],
        'Price Range - low (Rs.)': [90.0, 140.0],
        'Price Range - High (Rs.)': [110.0, 160.0]
    })

@pytest.fixture
def mock_invalid_data():
    return pd.DataFrame({
        'Week': ['2020-01-W1', 'invalid-date', '2020-01-W1'],
        'Item': ['Rice', 'Dhal', 'Rice'],
        'Unit': ['1 kg', '1 kg', '1 kg'],
        'Avg Price (Rs.)': [100.0, -10.0, 100.0], # Negative price and duplicate row
        'Price Range - low (Rs.)': [90.0, 140.0, 90.0],
        'Price Range - High (Rs.)': [110.0, 160.0, 110.0]
    })

def test_load_data_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_data('nonexistent_path.csv')

def test_validate_data_valid(mock_valid_data):
    report = validate_data(mock_valid_data)
    assert report['total_rows'] == 2
    assert not report['missing_columns']
    assert sum(report['missing_values'].values()) == 0
    assert report['negative_prices'] == 0
    assert report['invalid_dates'] == 0
    assert report['duplicate_rows'] == 0

def test_validate_data_invalid(mock_invalid_data):
    report = validate_data(mock_invalid_data)
    assert report['total_rows'] == 3
    assert report['negative_prices'] == 1
    assert report['invalid_dates'] == 1
    assert report['duplicate_rows'] == 1

def test_validate_data_missing_columns():
    df = pd.DataFrame({'Week': ['2020-01-W1']})
    report = validate_data(df)
    assert len(report['missing_columns']) > 0
    assert 'Item' in report['missing_columns']

def test_generate_quality_report(tmp_path, mock_valid_data):
    report = validate_data(mock_valid_data)
    out_file = tmp_path / "report.md"
    generate_quality_report(report, out_file)
    assert out_file.exists()
    content = out_file.read_text()
    assert "Data Quality Report" in content
    assert "**Total Rows:** 2" in content
