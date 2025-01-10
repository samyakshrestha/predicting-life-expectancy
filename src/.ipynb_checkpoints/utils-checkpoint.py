import pandas as pd
import requests

def fetch_and_merge_acs_variable(variable_code, variable_name, year, api_key):
    """
    Fetches an ACS variable from the Census API and merges it with the preprocessed DataFrame.
    
    Parameters:
    variable_code (str): ACS variable code to fetch (e.g., 'B19083_001E' for Gini Index).
    variable_name (str): Descriptive name for the variable (e.g., 'Gini_Index').
    year (int): Year of the ACS data (e.g., 2011).
    api_key (str): API key for accessing the Census API.
    
    Returns:
    pd.DataFrame: Final merged DataFrame with the ACS variable and life expectancy column added.
    """
    # Paths for input and output
    preprocessed_path = f'../data/processed/preprocessed_fips_life_expectancy/preprocessed_life_fips_{year}.csv'
    output_path = f'../data/processed/final_dataset/dataset_with_{variable_name}_{year}.csv'
    
    # Load preprocessed life expectancy and FIPS DataFrame
    print(f"Loading preprocessed data for {year}...")
    preprocessed_df = pd.read_csv(preprocessed_path)
    
    # API Endpoint and Parameters
    print(f"Fetching {variable_name} ({variable_code}) from the Census API for {year}...")
    acs_endpoint = f'https://api.census.gov/data/{year}/acs/acs5'
    params = {
        'get': variable_code,
        'for': 'county:*',  # All counties
        'in': 'state:*',    # All states
        'key': api_key      # Authentication
    }
    
    # Make the GET request
    response = requests.get(acs_endpoint, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch {variable_name}. Status code: {response.status_code}")
    
    # Parse the API Response
    acs_data = response.json()
    acs_df = pd.DataFrame(columns=acs_data[0], data=acs_data[1:])
    acs_df = acs_df.rename(columns={
        variable_code: variable_name,
        'state': 'State_FIPS',
        'county': 'County_FIPS'
    })

    # Ensure FIPS codes are formatted as strings in preprocessed_df
    preprocessed_df['State_FIPS'] = preprocessed_df['State_FIPS'].astype(str).str.zfill(2)
    preprocessed_df['County_FIPS'] = preprocessed_df['County_FIPS'].astype(str).str.zfill(3)
        
    # str.zfill() ensures that the State_FIPS and County_FIPS columns are properly formatted with leading zeros
    acs_df['State_FIPS'] = acs_df['State_FIPS'].str.zfill(2)
    acs_df['County_FIPS'] = acs_df['County_FIPS'].str.zfill(3)
    acs_df[variable_name] = pd.to_numeric(acs_df[variable_name], errors='coerce')
    
    # Merge ACS Data with Preprocessed Data
    final_df = pd.merge(
        preprocessed_df,
        acs_df[['State_FIPS', 'County_FIPS', variable_name]],
        on=['State_FIPS', 'County_FIPS'],
        how='left'
    )
    
    # Ensure `MeanLifeExpectancy` is in the final dataset
    if 'mean_life_expectancy' not in final_df.columns:
        raise ValueError("'mean_life_expectancy' column is missing in the final merged dataset.")
    
    # Save the Merged Dataset
    final_df.to_csv(output_path, index=False)
    
    print(f"Task completed. Final dataset saved: {output_path}")
    return final_df

def fetch_and_merge_acs_variable_summary(variable_code, variable_name, year, api_key):
    """
    Fetches an ACS variable from the Census API and merges it with the preprocessed DataFrame.
    
    Parameters:
    variable_code (str): ACS variable code to fetch (e.g., 'B19083_001E' for Gini Index).
    variable_name (str): Descriptive name for the variable (e.g., 'Gini_Index').
    year (int): Year of the ACS data (e.g., 2011).
    api_key (str): API key for accessing the Census API.
    
    Returns:
    pd.DataFrame: Final merged DataFrame with the ACS variable and life expectancy column added.
    """
    # Paths for input and output
    preprocessed_path = f'../data/processed/preprocessed_fips_life_expectancy/preprocessed_life_fips_{year}.csv'
    output_path = f'../data/processed/final_dataset/dataset_with_{variable_name}_{year}.csv'
    
    # Load preprocessed life expectancy and FIPS DataFrame
    print(f"Loading preprocessed data for {year}...")
    preprocessed_df = pd.read_csv(preprocessed_path)
      
    # API Endpoint and Parameters
    print(f"Fetching {variable_name} ({variable_code}) from the Census API for {year}...")
    acs_endpoint = f'https://api.census.gov/data/{year}/acs/acs5/subject'
    params = {
        'get': variable_code,
        'for': 'county:*',  # All counties
        'in': 'state:*',    # All states
        'key': api_key      # Authentication
    }
    
    # Make the GET request
    response = requests.get(acs_endpoint, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch {variable_name}. Status code: {response.status_code}")
    
    # Parse the API Response
    acs_data = response.json()
    acs_df = pd.DataFrame(columns=acs_data[0], data=acs_data[1:])
    acs_df = acs_df.rename(columns={
        variable_code: variable_name,
        'state': 'State_FIPS',
        'county': 'County_FIPS'
    })

    # Ensure FIPS codes are formatted as strings in preprocessed_df
    preprocessed_df['State_FIPS'] = preprocessed_df['State_FIPS'].astype(str).str.zfill(2)
    preprocessed_df['County_FIPS'] = preprocessed_df['County_FIPS'].astype(str).str.zfill(3)
        
    # str.zfill() ensures that the State_FIPS and County_FIPS columns are properly formatted with leading zeros
    acs_df['State_FIPS'] = acs_df['State_FIPS'].str.zfill(2)
    acs_df['County_FIPS'] = acs_df['County_FIPS'].str.zfill(3)
    acs_df[variable_name] = pd.to_numeric(acs_df[variable_name], errors='coerce')
    
    # Merge ACS Data with Preprocessed Data
    final_df = pd.merge(
        preprocessed_df,
        acs_df[['State_FIPS', 'County_FIPS', variable_name]],
        on=['State_FIPS', 'County_FIPS'],
        how='left'
    )
    
    # Ensure `MeanLifeExpectancy` is in the final dataset
    if 'mean_life_expectancy' not in final_df.columns:
        raise ValueError("'mean_life_expectancy' column is missing in the final merged dataset.")
    
    # Save the Merged Dataset
    final_df.to_csv(output_path, index=False)
    
    print(f"Task completed. Final dataset saved: {output_path}")
    return final_df