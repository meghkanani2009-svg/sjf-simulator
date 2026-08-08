import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="SJF CPU Scheduling Pro", 
    page_icon="⏱️", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. Advanced CSS: Parallax & Glassmorphism ---
st.markdown("""
<style>
    /* 1. PARALLAX BACKGROUND */
    .stApp {
        /* Pulls a premium dark tech background directly from the web */
        background-image: url("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop");
        background-attachment: fixed; /* Enables the parallax scroll effect */
        background-position: center;
        background-repeat: no-repeat;
        background-size: cover;
    }
    
    /* 2. PAGE SPACING & TYPOGRAPHY */
    .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 5rem !important;
        max-width: 95% !important;
    }
    .main-title {
        color: #FFFFFF;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        text-shadow: 0 8px 16px rgba(0,0,0,0.8);
        margin-bottom: 0px;
        letter-spacing: 1px;
    }
    .sub-title {
        color: #38BDF8;
        font-size: 1.2rem;
        font-weight: 600;
        text-align: center;
        text-shadow: 0 4px 8px rgba(0,0,0,0.8);
        margin-bottom: 3rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    h3 {
        color: #F8FAFC !important;
        text-shadow: 0 2px 5px rgba(0,0,0,0.8);
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(255,255,255,0.1);
        margin-top: 2rem !important;
    }

    /* 3. HIGHLIGHTED AVERAGES (100% Solid Dark) */
    div[data-testid="metric-container"] {
        background: #0B1121; /* Solid ultra-dark navy */
        border: 1px solid #1E293B;
        border-left: 6px solid #00F6FF; /* Neon Cyan Accent */
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.7);
    }
    div[data-testid="metric-container"] label {
        color: #94A3B8 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div[data-testid="stMetricValue"] {
        color: #00F6FF !important; /* Neon Cyan text */
        font-size: 3.2rem !important;
        font-weight: 900 !important;
        text-shadow: 0 0 20px rgba(0, 246, 255, 0.3);
    }

    /* 4. TABLES (50% Transparent Glassmorphism) */
    [data-testid="stDataEditor"], [data-testid="stDataFrame"] {
        background: rgba(11, 17, 33, 0.6); /* 60% Dark Transparency */
        backdrop-filter: blur(12px); /* Blurs the background image */
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5);
    }

    /* 5. MODERN BUTTON */
    .stButton > button {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
        color: white;
        font-weight: 800;
        font-size: 1.2rem;
        padding: 0.8rem 2.5rem;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 10px;
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(2, 132, 199, 0.6);
        background: linear-gradient(135deg, #0369A1 0%, #075985 100%);
        color: #00F6FF;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Header Area ---
st.markdown("<div class='main-title'>SJF Simulator</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Shortest Job First CPU Scheduling</div>", unsafe_allow_html=True)

# --- 4. State Management ---
if 'processes' not in st.session_state:
    st.session_state.processes = pd.DataFrame({
        'Process': ['P1', 'P2', 'P3', 'P4'],
        'Arrival Time': [0, 1, 2, 3],
        'Burst Time': [6, 4, 2, 1]
    })

# --- 5. Inputs ---
st.subheader("1. Process Configuration Queue")
st.write("Adjust the parameters below. The environment will update dynamically.")
edited_df = st.data_editor(st.session_state.processes, num_rows="dynamic", use_container_width=True)

# --- 6. Core Logic ---
if st.button("Initialize Execution Sequence 🚀"):
    
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

    # --- 7. Metric Output ---
    st.divider()
    
    results_df = pd.DataFrame(processes)
    results_df = results_df[['id', 'at', 'bt', 'ct', 'tat', 'wt']]
    results_df.columns = ['Process', 'Arrival Time', 'Burst Time', 'Completion Time', 'Turnaround Time', 'Waiting Time']
    
    st.subheader("2. Key Performance Indicators")
    col1, col2 = st.columns(2)
    col1.metric("Average Waiting Time", f"{results_df['Waiting Time'].mean():.2f} ms")
    col2.metric("Average Turnaround Time", f"{results_df['Turnaround Time'].mean():.2f} ms")
    
    st.write("<br>", unsafe_allow_html=True)
    
    # --- 8. Visual Output (Gantt) ---
    st.subheader("3. Execution Timeline (Gantt Chart)")
    df_gantt = pd.DataFrame(gantt_data)
    
    color_discrete_map = {
        'IDLE': '#1E293B', 'P1': '#0EA5E9', 'P2': '#8B5CF6', 
        'P3': '#10B981', 'P4': '#F43F5E', 'P5': '#F59E0B', 
        'P6': '#EF4444', 'P7': '#D946EF', 'P8': '#14B8A6', 
        'P9': '#84CC16', 'P10': '#64748B'
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
        xaxis_title="Time Units (ms)", 
        yaxis_title="",
        showlegend=False,
        height=380,
        plot_bgcolor='#0B1121', # Solid dark background so chart is easy to read
        paper_bgcolor='#0B1121', 
        font=dict(color="#F8FAFC"),
        xaxis=dict(showgrid=True, gridcolor='#1E293B', fixedrange=True, dtick=1),
        yaxis=dict(showgrid=False, fixedrange=True),
        margin=dict(t=40, b=40, l=20, r=20)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # --- 9. Data Output ---
    st.subheader("4. Detailed Calculation Logs")
    st.dataframe(results_df, use_container_width=True, hide_index=True)
