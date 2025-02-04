import pandas as pd

def clean_data(data):
    """
    Validate and transform the input data.
    'data' can be a dict from manual input or a DataFrame from file upload.
    """
    # If data is a DataFrame, apply cleaning steps
    if isinstance(data, pd.DataFrame):
        # Example: Drop rows where key fields are missing
        data_clean = data.dropna(subset=['use_case', 'steps', 'entities', 'relationships'])
        # Additional cleaning (e.g., trimming whitespace)
        data_clean = data_clean.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return data_clean
    elif isinstance(data, dict):
        # Validate manual input fields and standardize them
        for key in ['use_case']:
            if not data.get(key):
                raise ValueError(f"Missing required field: {key}")
        # You can also clean list items if needed
        data['steps'] = [s.strip() for s in data['steps']]
        data['entities'] = [e.strip() for e in data['entities']]
        data['relationships'] = [r.strip() for r in data['relationships']]
        return data
    else:
        raise TypeError("Unsupported data type for cleaning.")

