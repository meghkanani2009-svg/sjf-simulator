import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Page Setup ---
st.set_page_config(page_title="SJF Simulator", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Advanced Parallax & Glassmorphism CSS ---
st.markdown("""
<style>
    /* Parallax Background Implementation */
    .stApp {
        /* High-resolution abstract cinematic background */
        background-image: url("https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=2070&auto=format&fit=crop");
        background-attachment: fixed; /* This creates the parallax effect */
        background-position: center;
        background-repeat: no-repeat;
        background-size: cover;
    }
    
    /* Make the top padding a bit larger for a hero-section feel */
    .block-container {
        padding-top: 5rem !important;
        padding-bottom: 5rem !important;
    }

    /* Cinematic Header Typography */
    .hero-title {
        color: #ffffff;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        letter-spacing: -1px;
        text-shadow: 0 10px 20px rgba(0,0,0,0.5);
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        color: #e2e8f0;
        font-size: 1.2rem;
        text-align: center;
        font-weight: 300;
        letter-spacing: 1px;
        text-shadow: 0 4px 10px rgba(0,0,0,0.5);
        margin-bottom: 3rem;
    }

    /* Subheaders */
    h3 {
        color: #ffffff !important;
        font-weight: 600 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        margin-top: 2rem !important;
    }

    /* Text */
    p {
        color: #f8fafc;
        text-shadow: 0 1px 2px rgba(0,0,0,0.4);
    }

    /* --- GLASSMORPHISM FOR ALL CONTAINERS --- */
    /* Metric Boxes (Averages) */
    div[data-testid="metric-container"] {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-left: 5px solid #38bdf8; /* Bright neon blue accent */
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    div[data-testid="metric-container"] label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        text-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    }

    /* Data Tables */
    [data-testid="stDataEditor"], [data-testid="stDataFrame"] {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }

    /* Custom Button */
    .stButton > button {
        background: rgba(56, 189, 248, 0.9);
        color: #0f172a;
        font-weight: 800;
        font-size: 1.1rem;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.4);
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4);
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(56, 189, 248, 0.6);
        background: rgba(56, 189, 248, 1);
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Hero Section ---
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
st.write("Modify the arrival and burst times below. The interface will adapt dynamically.")
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
    
    color_discrete_map = {
        'IDLE': '#475569', 'P1': '#38bdf8', 'P2': '#818cf8', 
        'P3': '#34d399', 'P4': '#f472b6', 'P5': '#fbbf24', 
        'P6': '#f87171', 'P7': '#a78bfa', 'P8': '#2dd4bf', 
        'P9': '#e879f9', 'P10': '#94a3b8'
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
        # Make the chart background completely transparent to let the parallax show through
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', fixedrange=True, dtick=1),
        yaxis=dict(showgrid=False, fixedrange=True)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Final Detailed Table
    st.subheader("Detailed Calculation Logs")
    st.dataframe(results_df, use_container_width=True, hide_index=True)
