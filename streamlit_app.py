import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Page Setup ---
st.set_page_config(page_title="SJF Simulator", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Professional Dark Theme CSS ---
st.markdown("""
<style>
    /* Solid Dark Background for the whole app */
    .stApp {
        background-color: #0B0F19;
    }
    
    /* Adjust spacing */
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
    }

    /* Header Typography */
    .hero-title {
        color: #F8FAFC;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* Subheaders */
    h3 {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
        margin-top: 1.5rem !important;
        border-bottom: 1px solid #1E293B;
        padding-bottom: 0.5rem;
    }

    /* Text */
    p {
        color: #94A3B8;
    }

    /* --- SOLID DARK CARDS --- */
    /* Metric Boxes (Averages) */
    div[data-testid="metric-container"] {
        background-color: #151E2D; /* Solid dark slate */
        border: 1px solid #1E293B;
        border-left: 5px solid #38BDF8; /* Blue accent line */
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    div[data-testid="metric-container"] label {
        color: #94A3B8 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }
    div[data-testid="stMetricValue"] {
        color: #38BDF8 !important; /* Bright blue to pop against dark background */
        font-size: 2.8rem !important;
        font-weight: 700 !important;
    }

    /* Data Tables */
    [data-testid="stDataEditor"], [data-testid="stDataFrame"] {
        background-color: #151E2D;
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid #1E293B;
    }

    /* Custom Button */
    .stButton > button {
        background-color: #2563EB;
        color: white;
        font-weight: 700;
        font-size: 1.05rem;
        padding: 0.5rem 2rem;
        border-radius: 6px;
        border: none;
        transition: background-color 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #1D4ED8;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Header Section ---
st.markdown("<div class='hero-title'>SJF Scheduling Engine</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Non-Preemptive Shortest Job First Algorithm Visualization</div>", unsafe_allow_html=True)

# --- 4. Default Data ---
if 'processes' not in st.session_state:
    st.session_state.processes = pd.DataFrame({
        'Process': ['P1', 'P2', 'P3', 'P4'],
        'Arrival Time': [0, 1, 2, 3],
        'Burst Time': [6, 4, 2, 1]
    })

# --- 5. Input Section ---
st.subheader("Process Queue Configuration")
st.write("Modify the arrival and burst times below.")
edited_df = st.data_editor(st.session_state.processes, num_rows="dynamic", use_container_width=True)

st.write("<br>", unsafe_allow_html=True)

# --- 6. Simulation Logic ---
if st.button("Initialize Simulation Sequence"):
    
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

    # --- 7. Output UI Integration ---
    st.divider()
    
    results_df = pd.DataFrame(processes)
    results_df = results_df[['id', 'at', 'bt', 'ct', 'tat', 'wt']]
    results_df.columns = ['Process', 'Arrival Time', 'Burst Time', 'Completion Time', 'Turnaround Time', 'Waiting Time']
    
    # Highlighted Averages
    st.subheader("Performance Metrics")
    col1, col2 = st.columns(2)
    col1.metric("Average Waiting Time", f"{results_df['Waiting Time'].mean():.2f}")
    col2.metric("Average Turnaround Time", f"{results_df['Turnaround Time'].mean():.2f}")
    
    st.write("<br>", unsafe_allow_html=True)
    
    # Gantt Chart
    st.subheader("Execution Timeline")
    df_gantt = pd.DataFrame(gantt_data)
    
    # Professional color palette for dark mode
    color_discrete_map = {
        'IDLE': '#334155', 'P1': '#38BDF8', 'P2': '#818CF8', 
        'P3': '#34D399', 'P4': '#F472B6', 'P5': '#FBBF24', 
        'P6': '#F87171', 'P7': '#A78BFA', 'P8': '#2DD4BF', 
        'P9': '#E879F9', 'P10': '#94A3B8'
    }
    
    fig = px.bar(
        df_gantt, 
        base="Start", 
        x="Duration", 
        y="Task", 
        color="Task", 
        orientation='h',
        text="Task",
        color_discrete_map=color_discrete_map
    )
    
    fig.update_layout(
        xaxis_title="Time", 
        yaxis_title="",
        showlegend=False,
        height=350,
        # Solid dark background for the chart area
        plot_bgcolor='#151E2D',
        paper_bgcolor='#151E2D',
        font=dict(color="#F8FAFC"),
        xaxis=dict(showgrid=True, gridcolor='#1E293B', fixedrange=True, dtick=1),
        yaxis=dict(showgrid=False, fixedrange=True)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Final Detailed Table
    st.subheader("Detailed Calculation Logs")
    st.dataframe(results_df, use_container_width=True, hide_index=True)
