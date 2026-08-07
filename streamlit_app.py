import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="SJF Scheduling Simulator", layout="wide")
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
# The data_editor creates an interactive Excel-like grid right in the browser
edited_df = st.data_editor(st.session_state.processes, num_rows="dynamic", use_container_width=True)

# --- 2. Simulation Logic ---
if st.button("Solve & Generate Gantt Chart", type="primary"):
    
    # Convert dataframe into a list of dictionaries for easier calculation
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
        # Find available processes
        available = [p for p in processes if p['at'] <= current_time and not p['is_completed']]
        
        if available:
            # Sort by Burst Time, then Arrival Time
            available.sort(key=lambda x: (x['bt'], x['at']))
            current_p = available[0]
            
            start_time = current_time
            current_time += current_p['bt']
            
            # Record for Gantt chart
            gantt_data.append({
                'Task': current_p['id'], 
                'Start': start_time, 
                'Duration': current_p['bt']
            })
            
            # Update metrics
            for p in processes:
                if p['id'] == current_p['id']:
                    p['ct'] = current_time
                    p['tat'] = p['ct'] - p['at']
                    p['wt'] = p['tat'] - p['bt']
                    p['is_completed'] = True
                    break
            completed += 1
        else:
            # CPU is idle
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
    
    # Create an interactive horizontal bar chart using Plotly
    fig = px.bar(
        df_gantt, 
        base="Start", 
        x="Duration", 
        y="Task", 
        color="Task", 
        orientation='h',
        text="Task",
        title="CPU Execution Timeline"
    )
    
    fig.update_layout(
        xaxis_title="Time", 
        yaxis_title="Process",
        showlegend=False,
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # --- 4. Render Final Results Table ---
    st.subheader("3. Scheduling Results")
    
    results_df = pd.DataFrame(processes)
    results_df = results_df[['id', 'at', 'bt', 'ct', 'tat', 'wt']]
    results_df.columns = ['Process', 'Arrival Time', 'Burst Time', 'Completion Time', 'Turnaround Time', 'Waiting Time']
    
    st.dataframe(results_df, use_container_width=True, hide_index=True)
    
    # Render Average Metrics
    col1, col2 = st.columns(2)
    col1.metric("Average Waiting Time", f"{results_df['Waiting Time'].mean():.2f}")
    col2.metric("Average Turnaround Time", f"{results_df['Turnaround Time'].mean():.2f}")
