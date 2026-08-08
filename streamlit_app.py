import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Page Setup ---
st.set_page_config(page_title="SJF Simulator", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Parallax & Tiered Transparency CSS ---
st.markdown("""
<style>
    /* Parallax Background Implementation */
    .stApp {
        /* High-resolution, professional dark tech/abstract background */
        background-image: url("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop");
        background-attachment: fixed; /* Parallax scrolling effect */
        background-position: center;
        background-repeat: no-repeat;
        background-size: cover;
    }
    
    /* Adjust spacing for a cinematic feel */
    .block-container {
        padding-top: 4rem !important;
        padding-bottom: 5rem !important;
    }

    /* Header Typography */
    .hero-title {
        color: #ffffff;
        font-size: 3.2rem;
        font-weight: 900;
        text-shadow: 0 4px 10px rgba(0,0,0,0.8);
        margin-bottom: 0.2rem;
        text-align: center;
    }
    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.2rem;
        font-weight: 500;
        margin-bottom: 3rem;
        text-shadow: 0 2px 5px rgba(0,0,0,0.8);
        text-align: center;
    }

    /* Subheaders */
    h3 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.6);
        margin-top: 2rem !important;
    }

    /* Text */
    p {
        color: #E2E8F0;
        text-shadow: 0 1px 3px rgba(0,0,0,0.8);
    }

    /* --- HIGHEST IMPORTANCE: SOLID CONTAINERS --- */
    /* Highlighted Metric Boxes (Averages) - 100% Solid */
    div[data-testid="metric-container"] {
        background-color: #0F172A; /* 100% Solid Dark Navy */
        border: 2px solid #38BDF8; 
        border-left: 8px solid #38BDF8; 
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
    }
    div[data-testid="metric-container"] label {
        color: #94A3B8 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase;
    }
    div[data-testid="stMetricValue"] {
        color: #38BDF8 !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
    }

    /* --- LOWER IMPORTANCE: 50% TRANSPARENT CONTAINERS --- */
    /* Data Tables - 50% Transparent with slight blur for readability */
    [data-testid="stDataEditor"], [data-testid="stDataFrame"] {
        background-color: rgba(15, 23, 42, 0.5); /* 50% Transparent */
        backdrop-filter: blur(8px); /* Blurs the background image slightly behind the table */
        -webkit-backdrop-filter: blur(8px);
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid rgba(51, 65, 85, 0.6); /* Slightly transparent border */
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
    }

    /* Custom Button */
    .stButton > button {
        background-color: #2563EB;
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.6rem 2rem;
        border-radius: 6px;
        border: none;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
        transition: transform 0.2s ease, background-color 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #1D4ED8;
        transform: translateY(-2px);
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
st.write("Modify the arrival and burst times below. The simulation will adapt dynamically.")
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
    
    # Highlighted Averages (Solid background)
    st.subheader("Performance Metrics")
    col1, col2 = st.columns(2)
    col1.metric("Average Waiting Time", f"{results_df['Waiting Time'].mean():.2f}")
    col2.metric("Average Turnaround Time", f"{results_df['Turnaround Time'].mean():.2f}")
    
    st.write("<br>", unsafe_allow_html=True)
    
    # Gantt Chart (Solid background)
    st.subheader("Execution Timeline")
    df_gantt = pd.DataFrame(gantt_data)
    
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
        plot_bgcolor='#0F172A', /* 100% Solid Dark Navy for chart */
        paper_bgcolor='#0F172A',
        font=dict(color="#F8FAFC"),
        xaxis=dict(showgrid=True, gridcolor='#1E293B', fixedrange=True, dtick=1),
        yaxis=dict(showgrid=False, fixedrange=True)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Final Detailed Table (50% Transparent background applied via CSS above)
    st.subheader("Detailed Calculation Logs")
    st.dataframe(results_df, use_container_width=True, hide_index=True)
