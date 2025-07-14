import streamlit as st
import pandas as pd
import numpy as np

# Load data
@st.cache_data
def load_data():
    """Load the TIF surplus data"""
    try:
        df = pd.read_csv(r"data.csv")
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please ensure the CSV file is in the correct location.")
        return None


def main():    
# Load data

    df = load_data()

    if df is None:
        return

# Main app

    # Set the width of the app to be 75% of layout = "wide"
    
    st.set_page_config(page_title="TIF Surplus Estimates", layout="wide")

    st.title("TIF Surplus Estimates")
    
    # Print column names
    
    st.write("Column names in the dataset:")
    st.write(df.columns.tolist())
    
# Show 

    unallocated_tot = filtered_df['unallocated_funds_2025'].sum()
    surplus_city_tot = filtered_df['surplus_2025'].sum()
    ctu_method1_tot = filtered_df['full_surplus_avg_method_25'].sum()
    ctu_method2_tot = filtered_df['full_surplus_poly_method_25'].sum()
    ctu_method3_tot = filtered_df['full_surplus_weighted_method_25'].sum()

# Create a filter to select by TIF district default
    tif_districts = df['tif_name_comptroller_report'].unique()
    selected_district = st.selectbox("Select TIF District", tif_districts)

    filtered_df = df[(df['tif_name_comptroller_report'] == selected_district)]

    # Create a table where rows are unallocated funds, Surplus (City OMB method), Declared surplus (IL Comptroller data), and CTU methods 1,2, and 3
    unallocated = filtered_df['unallocated_funds_2025'].values[0]
    surplus_city = filtered_df['surplus_2025'].values[0]
    ctu_method1 = filtered_df['full_surplus_avg_method_25'].values[0]
    ctu_method2 = filtered_df['full_surplus_poly_method_25'].values[0]
    ctu_method3 = filtered_df['full_surplus_weighted_method_25'].values[0]
    
    table = pd.DataFrame({
        "Surplus method": ["Unallocated Funds", "Surplus (City OMB Method)", "CTU Method 1", "CTU Method 2", "CTU Method 3"],
        "Surplus amount": [unallocated, surplus_city, ctu_method1, ctu_method2, ctu_method3]
    })
    
    # Format the surplus amount column with currency formatting
    table['Surplus amount'] = table['Surplus amount'].apply(lambda x: f"${x:,.0f}")
    
    # Center the table using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.dataframe(table, use_container_width=True)

# Present total full_surplus_avg_method, full_surplus_poly_method, full_surplus_avg_method

if __name__ == "__main__":
    main()