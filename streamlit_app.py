import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="SJF Scheduling Simulator", layout="wide")

# --- Custom CSS Just for Highlighting Averages ---
st.markdown("""
<style>
    /* Styling to make the average metric boxes pop out */
    div[data-testid="metric-container"] {
        background-color: #eef6fc;
        border: 2px solid #1f77b4;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Make the titles of the averages bold and blue */
    div[data-testid="metric-container"] > div:first-child > div > div > label {
        color: #1f77b4 !important; 
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }
    
    /* Make the actual number values bold and red */
    div[data-testid="metric-container"] > div:nth-child(2) > div {
        color: #d62728 !important;
        font-size: 2.5rem !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)


st.title("CPU Scheduling Solver (Shortest Job First)")
st.markdown("An interactive web simulator for Non-Preemptive SJF.")

# --- Default Data ---
if 'processes' not in st.session_state:
    st.session_state.processes = pd.DataFrame({
        'Process': ['P1', 'P2', 'P3', 'P4'],
        'Arrival Time': [0, 1, 2, 3],
        'Burst Time': [6, 4, 2, 1]
    })

# --- 1. Input Section ---
st.subheader("1. Add Processes")
st.write("Edit the table below to add, remove, or modify processes.")
edited_df = st.data_editor(st.session_state.processes, num_rows="dynamic", use_container_width=True)

# --- 2. Simulation Logic ---
if st.button("Solve & Generate Gantt Chart", type="primary"):
    
    processes = []
    for i, row in edited_df.iterrows():
        processes.append({
            'id': str(row['Process']),
            'at': int(row['Arrival Time']),
            'bt': int(row['Burst Time']),
            'ct': 0, 'tat': 0, 'wt': 0,
            'is_completed': False
        })
    
    completed = 0
    current_time = 0
    n = len(processes)
    gantt_data = []

    while completed < n:
        available = [p for p in processes if p['at'] <= current_time and not p['is_completed']]
        
        if available:
            available.sort(key=lambda x: (x['bt'], x['at']))
            current_p = available[0]
            
            start_time = current_time
            current_time += current_p['bt']
            
            gantt_data.append({
                'Task': current_p['id'], 
                'Start': start_time, 
                'Duration': current_p['bt']
            })
            
            for p in processes:
                if p['id'] == current_p['id']:
                    p['ct'] = current_time
                    p['tat'] = p['ct'] - p['at']
                    p['wt'] = p['tat'] - p['bt']
                    p['is_completed'] = True
                    break
            completed += 1
        else:
            start_time = current_time
            current_time += 1
            if not gantt_data or gantt_data[-1]['Task'] != 'IDLE':
                 gantt_data.append({'Task': 'IDLE', 'Start': start_time, 'Duration': 1})
            else:
                 gantt_data[-1]['Duration'] += 1
    
    # --- 3. Render Gantt Chart ---
    st.divider()
    st.subheader("2. Gantt Chart")
    
    df_gantt = pd.DataFrame(gantt_data)
    
    # Define a clean color palette
    color_discrete_map = {
        'IDLE': '#d3d3d3', 'P1': '#1f77b4', 'P2': '#ff7f0e', 
        'P3': '#2ca02c', 'P4': '#d62728', 'P5': '#9467bd', 
        'P6': '#8c564b', 'P7': '#e377c2', 'P8': '#7f7f7f', 
        'P9': '#bcbd22', 'P10': '#17becf'
    }
    
    fig = px.bar(
        df_gantt, 
        base="Start", 
        x="Duration", 
        y="Task", 
        color="Task", 
        orientation='h',
        text="Task",
        title="CPU Execution Timeline",
        color_discrete_map=color_discrete_map
    )
    
    # Apply fixedrange=True so the chart cannot be accidentally zoomed in
    fig.update_layout(
        xaxis_title="Time", 
        yaxis_title="Process",
        showlegend=False,
        height=300,
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='#e0e0e0', fixedrange=True, dtick=1),
        yaxis=dict(showgrid=False, fixedrange=True)
    )
    
    # Remove the floating menu bar
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # --- 4. Render Final Results Table and Metrics ---
    st.subheader("3. Scheduling Results")
    
    results_df = pd.DataFrame(processes)
    results_df = results_df[['id', 'at', 'bt', 'ct', 'tat', 'wt']]
    results_df.columns = ['Process', 'Arrival Time', 'Burst Time', 'Completion Time', 'Turnaround Time', 'Waiting Time']
    
    # Render Average Metrics FIRST so the CSS highlights them at the top
    col1, col2 = st.columns(2)
    col1.metric("Average Waiting Time", f"{results_df['Waiting Time'].mean():.2f}")
    col2.metric("Average Turnaround Time", f"{results_df['Turnaround Time'].mean():.2f}")
    
    st.write("<br>", unsafe_allow_html=True)
    
    st.dataframe(results_df, use_container_width=True, hide_index=True)
