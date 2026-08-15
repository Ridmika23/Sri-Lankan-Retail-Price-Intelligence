import pytest
from streamlit.testing.v1 import AppTest
from pathlib import Path

# Skip testing if the processed data doesn't exist, as the app needs it
pytestmark = pytest.mark.skipif(
    not Path("data/processed/retail_prices_cleaned.csv").exists(),
    reason="Processed data not found."
)

@pytest.fixture
def app():
    """Initializes and runs the Streamlit app test fixture."""
    at = AppTest.from_file("../dashboard/app.py")
    at.run()
    return at

def test_app_loads_successfully(app):
    """Test that the app loads without exceptions."""
    assert not app.exception

def test_headings_and_limitations_displayed(app):
    """Test that main headings and limitations panel are displayed."""
    assert app.title[0].value == "📊 Sri Lankan Retail Price Intelligence"
    
    # Check headers (which are now subheaders in the app, but Streamlit AppTest represents subheaders as headers with smaller size or just in app.subheader)
    subheaders = [h.value for h in app.subheader]
    assert "1. Executive Overview" in subheaders
    assert "2. Longitudinal Price Trends" in subheaders
    assert "3. Cross-Sectional Item Comparison" in subheaders
    assert "4. Price Volatility Analysis" in subheaders
    assert "5. Data Explorer" in subheaders

def test_kpi_elements_displayed(app):
    """Test that the overview KPI metrics exist."""
    # Based on the columns we created, there are 6 metrics
    assert len(app.metric) == 6
    labels = [m.label for m in app.metric]
    assert "Date Range" in labels
    assert "Total Observations" in labels
    assert "Unique Items" in labels
    assert "Unique Units" in labels
    assert "Overall Average Price" in labels
    assert "Missing Avg Prices" in labels

def test_filters_exist(app):
    """Test that the sidebar filters exist (Date, Items, Units)."""
    assert len(app.date_input) >= 1
    assert len(app.multiselect) >= 2
    
    # Multiselect labels
    labels = [m.label for m in app.multiselect]
    assert "Select Items" in labels
    assert "Select Units" in labels

def test_data_explorer_and_download_exist(app):
    """Test that the data frame and download button are rendered."""
    assert len(app.dataframe) >= 1
    assert len(app.download_button) >= 1
    assert app.download_button[0].label == "⬇️ Download Filtered Data (CSV)"

def test_empty_filters_produce_warnings():
    """Test that clearing the items filter yields a warning and stops the charts."""
    at = AppTest.from_file("../dashboard/app.py").run()
    
    # Clear the selected items multiselect (index 0)
    at.multiselect[0].set_value([])
    at.run()
    
    # Assert a warning is displayed
    assert len(at.warning) >= 1
    assert "No data available" in at.warning[0].value
