import pytest
import pandas as pd
import numpy as np
from src.cleaning import clean_data

@pytest.fixture
def mock_raw_data():
    return pd.DataFrame({
        'Week': ['2020-01-W1', '2020-01-W2', '2020-01-W3', 'invalid-week', '2020-01-W4'],
        'Item': ['Rice', 'Rice', 'Rice', 'Dhal', 'Rice'],
        'Unit': ['1 kg', '1 kg', '1 kg', '1 kg', '1 kg'],
        'Avg Price (Rs.)': ['100.0', '110.0', 'NaN', '150.0', '0.0'],
        'Price Range - low (Rs.)': ['90.0', '105.0', 'NaN', '140.0', '0.0'],
        'Price Range - High (Rs.)': ['110.0', '115.0', 'NaN', '160.0', '0.0']
    })

def test_clean_data_week_parsing(mock_raw_data):
    df_clean = clean_data(mock_raw_data)
    
    # Check successful parses
    assert df_clean.loc[df_clean['original_week'] == '2020-01-W1', 'date'].iloc[0] == pd.Timestamp(2020, 1, 1)
    assert df_clean.loc[df_clean['original_week'] == '2020-01-W2', 'date'].iloc[0] == pd.Timestamp(2020, 1, 8)
    
    # Check invalid parse
    assert pd.isna(df_clean.loc[df_clean['original_week'] == 'invalid-week', 'date'].iloc[0])
    
    # Year, month, quarter derived
    assert df_clean.loc[df_clean['original_week'] == '2020-01-W1', 'year'].iloc[0] == 2020
    assert df_clean.loc[df_clean['original_week'] == '2020-01-W1', 'month'].iloc[0] == 1

def test_clean_data_numeric_conversion(mock_raw_data):
    df_clean = clean_data(mock_raw_data)
    assert pd.api.types.is_numeric_dtype(df_clean['avg_price'])
    assert df_clean.loc[df_clean['original_week'] == '2020-01-W1', 'avg_price'].iloc[0] == 100.0

def test_clean_data_missing_values(mock_raw_data):
    df_clean = clean_data(mock_raw_data)
    # The 'NaN' string should become actual numpy NaN
    assert pd.isna(df_clean.loc[df_clean['original_week'] == '2020-01-W3', 'avg_price'].iloc[0])

def test_clean_data_price_range(mock_raw_data):
    df_clean = clean_data(mock_raw_data)
    assert df_clean.loc[df_clean['original_week'] == '2020-01-W1', 'price_range'].iloc[0] == 20.0
    
def test_clean_data_percentage_change(mock_raw_data):
    df_clean = clean_data(mock_raw_data)
    
    # W1 to W2 (100 -> 110) = 10%
    w2 = df_clean[df_clean['original_week'] == '2020-01-W2'].iloc[0]
    assert w2['price_change'] == 10.0
    assert w2['price_change_percentage'] == 10.0
    
    # W2 to W3 (110 -> NaN) = NaN
    w3 = df_clean[df_clean['original_week'] == '2020-01-W3'].iloc[0]
    assert pd.isna(w3['price_change'])
    assert pd.isna(w3['price_change_percentage'])
    
    # W3 to W4 (NaN -> 0.0) = NaN
    w4 = df_clean[df_clean['original_week'] == '2020-01-W4'].iloc[0]
    # In pandas, if prev is NaN, shift is NaN, so 0.0 - NaN = NaN
    assert pd.isna(w4['price_change'])
    assert pd.isna(w4['price_change_percentage'])
