import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    page_title="SJF CPU Scheduling Simulator",
    page_icon="⚡",
    layout="wide"
)

# --- Professional CSS Styling ---
st.markdown("""
<style>
    /* Main Background & Padding */
    .main {
        background-color: #F8FAFC;
    }
    
    /* Header Container */
    .header-container {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .header-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        color: #FFFFFF;
    }
    .header-subtitle {
        font-size: 1rem;
        color: #94A3B8;
        margin-top: 0.4rem;
    }

    /* Metric Cards Styling (Highlighting Average Values) */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border: 1.5px solid #BFDBFE;
        padding: 1.25rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px -3px rgba(37, 99, 235, 0.2);
    }

    div[data-testid="metric-container"] label {
        color: #1E40AF !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    div[data-testid="stMetricValue"] {
        color: #2563EB !important;
        font-size: 2.4rem !important;
        font-weight: 800 !important;
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
        font-weight: 700;
        font-size: 1rem;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: none;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# --- Header UI ---
st.markdown("""
<div class="header-container">
    <div class="header-title">⚡ SJF CPU Scheduling Simulator</div>
    <div class="header-subtitle">Non-Preemptive Shortest Job First Algorithm Analytics & Interactive Gantt Chart</div>
</div>
""", unsafe_allow_html=True)

# --- Default Data ---
if 'processes' not in st.session_state:
    st.session_state.processes = pd.DataFrame({
        'Process': ['P1', 'P2', 'P3', 'P4'],
        'Arrival Time': [0, 1, 2, 3],
        'Burst Time': [6, 4, 2, 1]
    })

# --- Section 1: Input Table ---
st.subheader("1. Process Queue Configuration")
st.write("Modify process parameters directly in the table below:")

edited_df = st.data_editor(
    st.session_state.processes, 
    num_rows="dynamic", 
    use_container_width=True
)

st.write("") # Spacing

# --- Section 2: Calculation & Visualization ---
if st.button("🚀 Calculate & Generate Gantt Chart"):
    
    # Format inputs into dictionaries
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

    # Non-Preemptive SJF Execution Loop
    while completed < n:
        available = [p for p in processes if p['at'] <= current_time and not p['is_completed']]
        
        if available:
            # Sort by Burst Time (Primary) and Arrival Time (Secondary)
            available.sort(key=lambda x: (x['bt'], x['at']))
            current_p = available[0]
            
            start_time = current_time
            current_time += current_p['bt']
            
            gantt_data.append({
                'Task': current_p['id'], 
                'Start': start_time, 
                'Duration': current_p['bt'],
                'End': current_time
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
            # CPU is IDLE
            start_time = current_time
            current_time += 1
            if not gantt_data or gantt_data[-1]['Task'] != 'IDLE':
                 gantt_data.append({'Task': 'IDLE', 'Start': start_time, 'Duration': 1, 'End': current_time})
            else:
                 gantt_data[-1]['Duration'] += 1
                 gantt_data[-1]['End'] = current_time

    # --- Section 3: Highlighting Average Metrics ---
    st.divider()
    st.subheader("2. Key Performance Metrics")
    
    results_df = pd.DataFrame(processes)
    results_df = results_df[['id', 'at', 'bt', 'ct', 'tat', 'wt']]
    results_df.columns = ['Process', 'Arrival Time', 'Burst Time', 'Completion Time', 'Turnaround Time', 'Waiting Time']
    
    avg_wt = results_df['Waiting Time'].mean()
    avg_tat = results_df['Turnaround Time'].mean()
    
    col1, col2 = st.columns(2)
    col1.metric("Average Waiting Time (AWT)", f"{avg_wt:.2f} ms")
    col2.metric("Average Turnaround Time (ATAT)", f"{avg_tat:.2f} ms")
    
    st.write("") # Spacing

    # --- Section 4: Styled Plotly Gantt Chart ---
    st.subheader("3. Interactive Gantt Chart")
    
    df_gantt = pd.DataFrame(gantt_data)
    
    # Dynamic Palette Generation for any process names
    unique_tasks = df_gantt['Task'].unique()
    palette = px.colors.qualitative.Bold
    color_map = {}
    color_idx = 0
    
    for task in unique_tasks:
        if task == 'IDLE':
            color_map['IDLE'] = '#94A3B8' # Slate Grey for Idle time
        else:
            color_map[task] = palette[color_idx % len(palette)]
            color_idx += 1

    fig = px.bar(
        df_gantt, 
        base="Start", 
        x="Duration", 
        y="Task", 
        color="Task", 
        orientation='h',
        text="Task",
        color_discrete_map=color_map,
        labels={"Duration": "Time Units", "Task": "Process"}
    )
    
    # Custom hover info and styling
    fig.update_traces(
        textposition='inside',
        insidetextanchor='middle',
        marker_line_color='white',
        marker_line_width=1.5,
        opacity=0.9,
        hovertemplate="<b>Process:</b> %{y}<br><b>Start Time:</b> %{base}<br><b>Duration:</b> %{x} units<br><b>End Time:</b> %{customdata}<extra></extra>",
        customdata=df_gantt['End']
    )
    
    fig.update_layout(
        xaxis=dict(
            title="Time (ms)",
            showgrid=True,
            gridcolor="#E2E8F0",
            zeroline=True,
            zerolinecolor="#94A3B8",
            dtick=1
        ),
        yaxis=dict(
            title="Execution Queue",
            autorange="reversed", # Keeps P1/first process at top
            showgrid=False
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=320,
        margin=dict(l=20, r=20, t=30, b=40),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # --- Section 5: Process Results Table ---
    st.subheader("4. Detailed Execution Table")
    st.dataframe(results_df, use_container_width=True, hide_index=True)
