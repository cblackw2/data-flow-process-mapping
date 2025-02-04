import sys
from input_handler import get_manual_input, process_excel_upload
from data_processor import clean_data
from storage_manager import store_use_case, search_use_cases
from visualizer import build_flow_graph, export_diagram

def main():
    # Determine the mode based on command-line arguments or configuration.
    # For demonstration, we use a simple flag.
    mode = sys.argv[1] if len(sys.argv) > 1 else 'manual'
    
    if mode == 'manual':
        # Get manual input data
        raw_data = get_manual_input()
    elif mode == 'excel':
        # For file upload, assume file path is provided as second argument
        file_path = sys.argv[2]
        raw_data = process_excel_upload(file_path)
        # For simplicity, we may work with the first row of data:
        raw_data = raw_data.iloc[0].to_dict()
    else:
        print("Invalid mode selected. Choose 'manual' or 'excel'.")
        sys.exit(1)
    
    # Clean and validate data
    try:
        clean = clean_data(raw_data)
    except Exception as e:
        print(f"Error in data cleaning: {e}")
        sys.exit(1)
    
    # Store the use case
    store_use_case(clean)
    
    # Build and export the data flow diagram
    diagram = build_flow_graph(clean)
    export_diagram(diagram, file_format='png', output_file='data_flow_diagram')
    
    # Optionally, allow searching (this can be triggered by additional CLI flags)
    # Example: results = search_use_cases("customer")
    # print(results)

if __name__ == '__main__':
    main()
