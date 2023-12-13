import plotly.graph_objects as go
from setup import read, Instance
import pandas as pd

# Read data and create instance
G, F, TO, TM, ids, a, d, gates = read("GAP18_80.txt")
instance_verif = Instance(G, F, TO, TM, ids, a, d, gates)

# Solution list from your example
solution_list = [['EZY18DT', 'ASL16W', 'BRU865', 'EZY82AR', 'EZY79DY', 'AUI129'], ['CSA3DZ', 'AUI3FU', 'EZY57NG', 'AFR17DP'], [], ['AFR12ZK', 'CSA2DZ', 'EZY68NG', 'ASL98F', 'EZY3798'], ['LZB431', 'EZY27YN', 'BTI3CE', 'CSA4CZ', 'EZY329C'], ['EZY81LX', 'AEA1011', 'EZY23YB', 'EZY14EZ', 'EZY657Y', 'EZY68HP'], ['AFR93XX', 'EZY696H', 'EZY48UH', 'EZY14ML', 'EZY36QF'], ['AUI130', 'AFR14CJ', 'EZY49QU', 'EZY64RH', 'EZY42NK', 'EZY81YK', 'EZY57QB'], ['EZY9004', 'AFR52EU', 'EZY7043', 'EZY56LP', 'CTN476'], [], ['EZY929H', 'AHY073', 'FIN6M', 'FIN2AP', 'EZY3672'], ['AFR132F', 'EZY35HL', 'AUA415C', 'AFR126N', 'EZY241B'], ['EZY43VJ', 'AUA411C', 'AUA413', 'EZY64UH', 'AFR15FX'], [], ['EZY41KM', 'FIN8PY', 'EZY86WT', 'EZY69KT', 'EZY13XV', 'EZY28KJ'], ['EZY31UP', 'AMC478', 'EZY59FD', 'EZY716N', 'AFR18PP'], ['EZY37FM', 'FIN4LF', 'EZY18NT', 'EZY92UE', 'AUA417C', 'EZY15NM'], ['EZY39CX', 'EZY48EP', 'CTN25F', 'EZY2439', 'EZY23PK']]

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