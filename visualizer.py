from graphviz import Digraph
import networkx as nx
import plotly.graph_objects as go

def build_flow_graph(use_case_data):
    """
    Build a data flow graph from use case data.
    For simplicity, use the manual input dict structure.
    """
    dot = Digraph(comment='Data Flow Mapping')
    # Add nodes for use case, steps, entities
    dot.node('UC', use_case_data['use_case'])
    
    # Create nodes for each step
    for i, step in enumerate(use_case_data['steps']):
        dot.node(f'S{i}', step)
        dot.edge('UC', f'S{i}')
        
    # Create nodes for each entity and connect them to the corresponding steps
    for j, entity in enumerate(use_case_data['entities']):
        dot.node(f'E{j}', entity)
        # This is a simplified example; in practice, relationships would determine edges.
        dot.edge(f'S0', f'E{j}')
    
    # Relationships can be added as additional edges if specified.
    for rel in use_case_data['relationships']:
        # Parse the relationship string; here assume format "StepA->EntityB"
        if '->' in rel:
            src, dst = rel.split('->')
            dot.edge(src.strip(), dst.strip())
    return dot

def export_diagram(dot_graph, file_format='png', output_file='data_flow_diagram'):
    """
    Export the diagram to a file in the specified format.
    """
    dot_graph.format = file_format
    dot_graph.render(output_file, view=False)
    print(f"Diagram exported as {output_file}.{file_format}")
