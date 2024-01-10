import plotly.graph_objects as go
from setup import read, Instance
import pandas as pd

# Read data and create instance
G, F, TO, TM, ids, a, d, gates = read("GAP4_15.txt")
instance_verif = Instance(G, F, TO, TM, ids, a, d, gates)

# Solution list from your example
solution_list = [['ZI454', 'KL023', 'LH218', 'IB8776'], ['KL018', 'KL055', 'CX444', 'LH1009'], ['ZI442', 'ZI412', 'ZI734', 'EZY4025'], ['CX403', 'KL002', 'FR2105']]

# Create a list to store flight information
flight_data = []

# Fill the list with flight information from the solution
for i, gate_solution in enumerate(solution_list):
    for flight_id in gate_solution:
        flight = instance_verif.search_flight(flight_id)
        flight_data.append({
            "Flight": flight.id,
            "Gate": f"Gate {i + 1}",
            "Start": flight.a,
            "End": flight.d
        })

# Create a DataFrame from the list
flight_df = pd.DataFrame(flight_data)

# Create a line chart using plotly.graph_objects
fig = go.Figure()

# Add a line for each flight
for index, row in flight_df.iterrows():
    fig.add_trace(go.Scatter(
        x=[row["Start"], row["End"]],
        y=[row["Gate"], row["Gate"]],
        line=dict(width=6),
        mode='lines',
        name=f"Flight {row['Flight']}",
        text=f"Flight {row['Flight']}",
        hoverinfo="text",
    ))

# Update the layout for better readability
fig.update_layout(
    xaxis_title="Time",
    yaxis_title="Gates",
    showlegend=True,
    height=400,
    margin=dict(l=0, r=0, t=50, b=0),  # Adjust margin for better space utilization
)

# Display the plot
fig.show(renderer='browser')