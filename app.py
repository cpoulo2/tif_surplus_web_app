import streamlit as st
import pandas as pd
import numpy as np

# Load data
@st.cache_data
def load_data():
    """Load the TIF surplus data"""
    try:
        df = pd.read_csv(r"data.csv")
        # Filter out expiration data for 2024
        df = df[df['expiration_date'].astype(str).str[-4:] != '2024']
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
    
    st.set_page_config(page_title="TIF Surplus Estimates", layout="centered")

# Show City Surplus Totals

    st.header("Total TIF Surplus Estimates for 2025")

    unallocated_tot = df['unallocated_funds_2025'].sum()
    surplus_city_tot = df['surplus_2025'].sum()
    ctu_method1_tot = df['full_surplus_avg_method_25'].sum()
    ctu_method2_tot = df['full_surplus_poly_method_25'].sum()
    ctu_method3_tot = df['full_surplus_weighted_method_25'].sum()
    
    # Calculate portion alloted to CPS and City
    # First calculate % of total property tax rate (https://www.chicago.gov/content/dam/city/depts/fin/supp_info/CAFR/2024CAFR/ACFR_2024.pdf, pp. 234-5)

    chi = 1.741/6.995
    cps = 3.829/6.995

    unallocated_tot_cps = unallocated_tot * cps
    surplus_city_tot_cps = surplus_city_tot * cps
    ctu_method1_tot_cps = ctu_method1_tot * cps
    ctu_method2_tot_cps = ctu_method2_tot * cps
    ctu_method3_tot_cps = ctu_method3_tot * cps
    unallocated_tot_chi = unallocated_tot * chi
    surplus_city_tot_chi = surplus_city_tot * chi
    ctu_method1_tot_chi = ctu_method1_tot * chi
    ctu_method2_tot_chi = ctu_method2_tot * chi
    ctu_method3_tot_chi = ctu_method3_tot * chi
    
    table = pd.DataFrame({
        "Surplus method": ["Unallocated Funds", "Surplus (City OMB Method)", "CTU Method 1", "CTU Method 2", "CTU Method 3"],
        "Surplus amount": [unallocated_tot, surplus_city_tot, ctu_method1_tot, ctu_method2_tot, ctu_method3_tot],
        "CPS surplus revenue": [unallocated_tot_cps, surplus_city_tot_cps, ctu_method1_tot_cps, ctu_method2_tot_cps, ctu_method3_tot_cps],
        "City of Chicago surplus revenue": [unallocated_tot_chi, surplus_city_tot_chi, ctu_method1_tot_chi, ctu_method2_tot_chi, ctu_method3_tot_chi]
    })
    
    # Center the table using columns - make it a bit wider
    col1, col2, col3 = st.columns([.5, 20, .5])
    with col2:
        # Try a different approach - format numbers but keep them sortable
        st.dataframe(
            table.style.format({
                "Surplus amount": "${:,.0f}",
                "CPS surplus revenue": "${:,.0f}",
                "City of Chicago surplus revenue": "${:,.0f}"
            }), 
            use_container_width=True, 
            hide_index=True
        )
    st.header("TIF Surplus 2025 Estimates by District")

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
    
    unallocated_cps = unallocated * cps
    surplus_city_cps = surplus_city * cps
    ctu_method1_cps = ctu_method1 * cps
    ctu_method2_cps = ctu_method2 * cps
    ctu_method3_cps = ctu_method3 * cps
    unallocated_chi = unallocated * chi
    surplus_city_chi = surplus_city * chi
    ctu_method1_chi = ctu_method1 * chi
    ctu_method2_chi = ctu_method2 * chi
    ctu_method3_chi = ctu_method3 * chi
    
    table = pd.DataFrame({
        "Surplus method": ["Unallocated Funds", "Surplus (City OMB Method)", "CTU Method 1", "CTU Method 2", "CTU Method 3"],
        "Surplus amount": [unallocated, surplus_city, ctu_method1, ctu_method2, ctu_method3],
        "CPS surplus revenue": [unallocated_cps, surplus_city_cps, ctu_method1_cps, ctu_method2_cps, ctu_method3_cps],
        "City of Chicago surplus revenue": [unallocated_chi, surplus_city_chi, ctu_method1_chi, ctu_method2_chi, ctu_method3_chi]
    })
    
    # Center the table using columns - make it a bit wider
    col1, col2, col3 = st.columns([.5, 20, .5])
    with col2:
        # Try a different approach - format numbers but keep them sortable
        st.dataframe(
            table.style.format({
                "Surplus amount": "${:,.0f}",
                "CPS surplus revenue": "${:,.0f}",
                "City of Chicago surplus revenue": "${:,.0f}"
            }), 
            use_container_width=True, 
            hide_index=True
        )
        
    st.header("Top 5 TIF Districts with Largest Surplus Estimates")
# Filter for top 5 districts

    tif_districts = df['tif_name_comptroller_report'].unique()
    
    # Filter for districts with the top 5 largest fully_surplus_poly_method_25 amounts
    top5 = df.nlargest(5, 'full_surplus_poly_method_25')
    
    # Filter for needed columns
    filter_cols = ['tif_name_comptroller_report', 'expiration_date','unallocated_funds_2025', 
                   'surplus_2025','full_surplus_avg_method_25','full_surplus_poly_method_25',
                   'full_surplus_weighted_method_25']
    
    top5 = top5[filter_cols]
    
    # Rename columns for clarity
    top5.rename(columns={
        'unallocated_funds_2025': 'Unallocated Funds',
        'surplus_2025': 'Surplus (City OMB Method)',
        'full_surplus_avg_method_25': 'CTU Method 1',
        'full_surplus_poly_method_25': 'CTU Method 2',
        'full_surplus_weighted_method_25': 'CTU Method 3'
    }, inplace=True)
    
    # Center the table using columns - make it a bit wider
    col1, col2, col3 = st.columns([.5, 20, .5])
    with col2:
        # Try a different approach - format numbers but keep them sortable
        # Formate the unallocated funds, surplus, and CTU methods as currency
        top5['Unallocated Funds'] = top5['Unallocated Funds'].apply(lambda x: f"${x:,.0f}")
        top5['Surplus (City OMB Method)'] = top5['Surplus (City OMB Method)'].apply(lambda x: f"${x:,.0f}")
        top5['CTU Method 1'] = top5['CTU Method 1'].apply(lambda x: f"${x:,.0f}")
        top5['CTU Method 2'] = top5['CTU Method 2'].apply(lambda x: f"${x:,.0f}")
        top5['CTU Method 3'] = top5['CTU Method 3'].apply(lambda x: f"${x:,.0f}")
        st.dataframe(top5,hide_index=True, use_container_width=True)
        

# Download the data.csv file

    st.header("Download Data")
    st.markdown("You can download the full data used in this app as a CSV file.")
    csv = df.to_csv(index=False)

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="tif_surplus_data.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()