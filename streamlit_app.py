import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="SJF CPU Scheduling Simulator",
    page_icon="⚡",
    layout="wide"
)

# --- 2. Global CSS Injection ---
st.markdown("""
<style>
    /* Main Background */
    .main {
        background-color: #F8FAFC;
    }
    
    /* Custom Header */
    .header-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
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

    /* Subheaders for Sections */
    h3 {
        color: #0F172A !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E2E8F0;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }

    /* Input Table (Data Editor) Styling */
    [data-testid="stDataEditor"] {
        background-color: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04);
        border: 1px solid #E2E8F0;
    }

    /* Output Table (DataFrame) Styling */
    [data-testid="stDataFrame"] {
        background-color: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04);
        border: 1px solid #E2E8F0;
    }

    /* Run Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        border: none;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
        transform: translateY(-2px);
    }

    /* =========================================================
       HIGHLIGHTED AVERAGE METRICS CSS 
       This makes the average times massive and highly visible
       ========================================================= */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border: 2px solid #60A5FA;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.15);
        text-align: center;
    }
    div[data-testid="metric-container"] label {
        color: #1E40AF !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="stMetricValue"] {
        color: #DC2626 !important; /* Bold Red to make it pop */
        font-size: 3rem !important;
        font-weight: 900 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Dashboard Header ---
st.markdown("""
<div class="header-container">
    <div class="header-title">⚡ SJF CPU Scheduling Solver</div>
    <div class="header-subtitle">Non-Preemptive Shortest Job First Algorithm Analytics & Execution Timeline</div>
</div>
""", unsafe_allow_html=True)

# --- 4. Default Data Setup ---
if 'processes' not in st.session_state:
    st.session_state.processes = pd.DataFrame({
        'Process': ['P1', 'P2', 'P3', 'P4'],
        'Arrival Time': [0, 1, 2, 3],
        'Burst Time': [6, 4, 2, 1]
    })

# --- 5. Input Section ---
st.subheader("1. Process Queue Configuration")
st.write("Modify the arrival and burst times directly in the table below:")

edited_df = st.data_editor(
    st.session_state.processes, 
    num_rows="dynamic", 
    use_container_width=True
)

st.write("") # Spacing before the button

# --- 6. Core Algorithm & Visualization ---
if st.button("🚀 Calculate SJF Scheduling"):
    
    # Read data from the table
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

    # Process Execution Loop (Non-Preemptive)
    while completed < n:
        available = [p for p in processes if p['at'] <= current_time and not p['is_completed']]
        
        if available:
            # Sort by Burst Time, then Arrival Time for tie-breaking
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
            
            # Calculate CT, TAT, and WT
            for p in processes:
                if p['id'] == current_p['id']:
                    p['ct'] = current_time
                    p['tat'] = p['ct'] - p['at']
                    p['wt'] = p['tat'] - p['bt']
                    p['is_completed'] = True
                    break
            completed += 1
        else:
            # CPU is idle waiting for the next process to arrive
            start_time = current_time
            current_time += 1
            if not gantt_data or gantt_data[-1]['Task'] != 'IDLE':
                 gantt_data.append({'Task': 'IDLE', 'Start': start_time, 'Duration': 1, 'End': current_time})
            else:
                 gantt_data[-1]['Duration'] += 1
                 gantt_data[-1]['End'] = current_time

    # Prepare final results dataframe
    results_df = pd.DataFrame(processes)
    results_df = results_df[['id', 'at', 'bt', 'ct', 'tat', 'wt']]
    results_df.columns = ['Process', 'Arrival Time', 'Burst Time', 'Completion Time', 'Turnaround Time', 'Waiting Time']
    
    avg_wt = results_df['Waiting Time'].mean()
    avg_tat = results_df['Turnaround Time'].mean()
    
    # --- 7. Highlighted Key Metrics ---
    st.divider()
    st.subheader("2. Key Performance Metrics")
    
    # Placed in columns so they appear side-by-side at the top
    col1, col2 = st.columns(2)
    col1.metric("Average Waiting Time", f"{avg_wt:.2f} ms")
    col2.metric("Average Turnaround Time", f"{avg_tat:.2f} ms")
    
    st.write("") # Spacing

    # --- 8. Styled & Locked Gantt Chart ---
    st.subheader("3. Execution Timeline (Gantt Chart)")
    
    df_gantt = pd.DataFrame(gantt_data)
    
    # Automatically assign professional colors to processes
    unique_tasks = df_gantt['Task'].unique()
    palette = px.colors.qualitative.Prism
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
        color_discrete_map=color_map
    )
    
    fig.update_traces(
        textposition='inside',
        insidetextanchor='middle',
        marker_line_color='white',
        marker_line_width=1.5,
        hovertemplate="<b>Process:</b> %{y}<br><b>Start:</b> %{base}<br><b>Duration:</b> %{x}<br><b>End:</b> %{customdata}<extra></extra>",
        customdata=df_gantt['End']
    )
    
    fig.update_layout(
        xaxis=dict(
            title="Time Units",
            showgrid=True,
            gridcolor="#E2E8F0",
            zeroline=True,
            zerolinecolor="#94A3B8",
            dtick=1,
            fixedrange=True  # DISABLES X-AXIS ZOOMING
        ),
        yaxis=dict(
            title="",
            autorange="reversed",
            showgrid=False,
            fixedrange=True  # DISABLES Y-AXIS ZOOMING
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=350,
        margin=dict(l=20, r=20, t=20, b=40),
        showlegend=False
    )
    
    # Hide the modebar to prevent any accidental tool clicks
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # --- 9. Detailed Final Table ---
    st.subheader("4. Detailed Calculation Table")
    st.dataframe(results_df, use_container_width=True, hide_index=True)
