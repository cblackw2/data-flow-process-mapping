import streamlit as st
import pandas as pd
import graphviz

# -------------------------------------------------------
# Helper Functions
# -------------------------------------------------------

def process_manual_input(use_case, functional_area, dcl, data_source,
                         platform_aggregate, platform_analyze, platform_publish, compliance):
    """
    Converts manual input fields into a structured dictionary.
    """
    return {
        "use_case": use_case,
        "functional_area": functional_area,
        "dcl": dcl,
        "data_source": data_source,
        "platform_aggregate": platform_aggregate,
        "platform_analyze": platform_analyze,
        "platform_publish": platform_publish,
        "compliance": compliance
    }

def process_excel_file(uploaded_file):
    """
    Reads an Excel file (which must contain the columns:
    "Use Case/Scenario", "Functional Area", "DCL", "Where data is sourced from",
    "Platform used to aggregate data", "Platform used to analyze data",
    "Platform used to publish curated data", and "compliance")
    and returns the first row as a dictionary.
    """
    df = pd.read_excel(uploaded_file)
    if df.empty:
        st.error("Uploaded file is empty.")
        return None
    required_columns = [
        "Use Case/Scenario", "Functional Area", "DCL", "Where data is sourced from",
        "Platform used to aggregate data", "Platform used to analyze data",
        "Platform used to publish curated data", "compliance"
    ]
    if not all(col in df.columns for col in required_columns):
        st.error(f"Excel file must contain the following columns: {', '.join(required_columns)}")
        return None
    # For simplicity, use the first row of data:
    row = df.iloc[0]
    return {
        "use_case": row["Use Case/Scenario"],
        "functional_area": row["Functional Area"],
        "dcl": row["DCL"],
        "data_source": row["Where data is sourced from"],
        "platform_aggregate": row["Platform used to aggregate data"],
        "platform_analyze": row["Platform used to analyze data"],
        "platform_publish": row["Platform used to publish curated data"],
        "compliance": row["compliance"]
    }

def build_dot_diagram(data):
    """
    Constructs a simple Graphviz DOT diagram using the input data.
    The "use case" is treated as the root node and each additional parameter 
    is added as a child node.
    """
    dot = graphviz.Digraph(comment="Data Flow Diagram")
    
    # Root node for the use case/scenario
    dot.node("UC", data["use_case"])
    
    # Create nodes for each additional parameter
    dot.node("FA", f"Functional Area: {data['functional_area']}")
    dot.node("DCL", f"DCL: {data['dcl']}")
    dot.node("DS", f"Data Source: {data['data_source']}")
    dot.node("PA", f"Platform Aggregate: {data['platform_aggregate']}")
    dot.node("PAn", f"Platform Analyze: {data['platform_analyze']}")
    dot.node("PP", f"Platform Publish: {data['platform_publish']}")
    dot.node("C", f"Compliance: {data['compliance']}")
    
    # Connect the use case node to each parameter node
    dot.edge("UC", "FA")
    dot.edge("UC", "DCL")
    dot.edge("UC", "DS")
    dot.edge("UC", "PA")
    dot.edge("UC", "PAn")
    dot.edge("UC", "PP")
    dot.edge("UC", "C")
    
    return dot

# -------------------------------------------------------
# Main Application
# -------------------------------------------------------

def main():
    st.title("Data Flow Mapping Application")
    
    # Sidebar: Choose the input method
    input_method = st.sidebar.radio("Select Input Method", ("Manual Input", "Excel Upload"))
    
    with st.form(key="data_form"):
        if input_method == "Manual Input":
            # Updated manual input fields
            use_case = st.text_input("Use Case/Scenario", "Customer Order Processing")
            functional_area = st.text_input("Functional Area", "Sales")
            dcl = st.text_input("DCL", "Level 1")
            data_source = st.text_input("Where data is sourced from", "CRM System")
            platform_aggregate = st.text_input("Platform used to aggregate data", "Data Warehouse")
            platform_analyze = st.text_input("Platform used to analyze data", "BI Tool")
            platform_publish = st.text_input("Platform used to publish curated data", "Reporting Dashboard")
            compliance = st.text_input("Compliance", "GDPR Compliant")
        else:
            # File uploader for Excel mode
            uploaded_file = st.file_uploader("Upload an Excel File", type=["xlsx", "xls"])
        
        submit_button = st.form_submit_button(label="Process Data")
    
    input_data = None
    if submit_button:
        if input_method == "Manual Input":
            if not use_case:
                st.error("Please enter a use case/scenario.")
            else:
                input_data = process_manual_input(use_case, functional_area, dcl, data_source,
                                                  platform_aggregate, platform_analyze, platform_publish, compliance)
        else:
            if uploaded_file is None:
                st.error("Please upload an Excel file.")
            else:
                input_data = process_excel_file(uploaded_file)
        
        if input_data:
            st.success("Input data processed successfully!")
            st.write("### Processed Input Data:")
            st.json(input_data)
            
            # Build and display the data flow diagram
            dot_diagram = build_dot_diagram(input_data)
            st.write("### Data Flow Diagram")
            st.graphviz_chart(dot_diagram.source)

if __name__ == "__main__":
    main()
