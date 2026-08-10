import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="SJF CPU Scheduling Pro", 
    page_icon="⏱️", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. Safely Load Your Specific Background Image ---
@st.cache_data
def get_base64_of_bin_file(bin_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, bin_file)
    
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.error(f"⚠️ Looked for the image here, but couldn't find it: {file_path}")
        return None

bg_image = get_base64_of_bin_file("Screenshot 2026-08-08 215442.png")

if bg_image:
    background_css = f"""
    <style>
        /* The ultimate mobile-safe fixed background trick */
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-image: url("data:image/png;base64,{bg_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            z-index: -999;
        }}
        /* Make sure the main containers are transparent so the background shows */
        [data-testid="stAppViewContainer"], .stApp {{
            background: transparent !important;
        }}
        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0) !important;
        }}
    </style>
    """
else:
    background_css = """
    <style>
        [data-testid="stAppViewContainer"] { background-color: #0B1121; }
        [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    </style>
    """

# --- 3. Advanced CSS: Desktop & AGGRESSIVE Mobile Overrides ---
st.markdown(background_css + """
<style>
    /* Prevent horizontal scrolling/wobble on the whole app */
    html, body {
        overflow-x: hidden !important;
    }

    /* DESKTOP SPACING & TYPOGRAPHY */
    .block-container {
        padding-top: 2rem !important;
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

    /* HIGHLIGHTED AVERAGES */
    div[data-testid="metric-container"] {
        background: #0B1121; 
        border: 1px solid #1E293B;
        border-left: 6px solid #00F6FF; 
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
        color: #00F6FF !important; 
        font-size: 3.2rem !important;
        font-weight: 900 !important;
        text-shadow: 0 0 20px rgba(0, 246, 255, 0.3);
    }

    /* TABLES */
    [data-testid="stDataEditor"], [data-testid="stDataFrame"] {
        background: rgba(11, 17, 33, 0.6); 
        backdrop-filter: blur(12px); 
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5);
    }

    /* MODERN BUTTON */
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

    /* =========================================
       📱 AGGRESSIVE MOBILE FIXES (max-width: 768px)
       ========================================= */
    @media (max-width: 768px) {
        /* Tightly control the main container padding */
        .block-container {
            padding-top: 1.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-bottom: 3rem !important;
        }

        /* Squish text significantly for small phone screens */
        .main-title {
            font-size: 1.8rem !important;
        }
        .sub-title {
            font-size: 0.85rem !important;
            margin-bottom: 1.5rem !important;
            letter-spacing: 1px !important;
        }
        h3 {
            font-size: 1.1rem !important;
            margin-top: 1rem !important;
        }

        /* Compact Metric Cards */
        div[data-testid="metric-container"] {
            padding: 1rem !important;
            border-left: 4px solid #00F6FF !important; /* Thinner line */
        }
        div[data-testid="metric-container"] label {
            font-size: 0.85rem !important;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.8rem !important; /* Huge reduction so it fits */
        }

        /* Compact Data Tables */
        [data-testid="stDataEditor"], [data-testid="stDataFrame"] {
            padding: 0.5rem !important;
        }
        
        /* Button scaling */
        .stButton > button {
            font-size: 1rem !important;
            padding: 0.6rem 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- 4. Header Area ---
st.markdown("<div class='main-title'>SJF Simulator</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Shortest Job First CPU Scheduling</div>", unsafe_allow_html=True)

# --- 5. State Management ---
if 'processes' not in st.session_state:
    st.session_state.processes = pd.DataFrame({
        'Process': ['P1', 'P2', 'P3', 'P4'],
        'Arrival Time': [0, 1, 2, 3],
        'Burst Time': [6, 4, 2, 1]
    })

# --- 6. Inputs ---
st.subheader("1. Process Configuration Queue")
st.write("Adjust the parameters below. The environment will update dynamically.")
edited_df = st.data_editor(st.session_state.processes, num_rows="dynamic", use_container_width=True)

# --- 7. Core Logic & Ready Queue Processing ---
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
    ready_queue_log = [] # New tracking array for the Ready Queue

    while completed < n:
        # Find all processes that have arrived and are not finished
        available = [p for p in processes if p['at'] <= current_time and not p['is_completed']]
        
        if available:
            # Format the ready queue visually for the logs
            rq_display = " | ".join([f"{p['id']} (BT:{p['bt']})" for p in available])
            
            # Sort by Burst Time first (SJF logic), then Arrival Time if there's a tie
            available.sort(key=lambda x: (x['bt'], x['at']))
            current_p = available[0]
            
            # Log the decision
            ready_queue_log.append({
                'Time Unit': current_time,
                'Ready Queue State': rq_display,
                'Selected Process': current_p['id']
            })
            
            # Execute Process
            start_time = current_time
            current_time += current_p['bt']
            
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
            # CPU is IDLE
            ready_queue_log.append({
                'Time Unit': current_time,
                'Ready Queue State': "Empty",
                'Selected Process': "IDLE"
            })
            
            start_time = current_time
            current_time += 1
            if not gantt_data or gantt_data[-1]['Task'] != 'IDLE':
                 gantt_data.append({'Task': 'IDLE', 'Start': start_time, 'Duration': 1})
            else:
                 gantt_data[-1]['Duration'] += 1

    # --- 8. Metric Output ---
    st.divider()
    
    results_df = pd.DataFrame(processes)
    results_df = results_df[['id', 'at', 'bt', 'ct', 'tat', 'wt']]
    results_df.columns = ['Process', 'Arrival Time', 'Burst Time', 'Completion Time', 'Turnaround Time', 'Waiting Time']
    
    st.subheader("2. Key Performance Indicators")
    col1, col2 = st.columns(2)
    col1.metric("Average Waiting Time", f"{results_df['Waiting Time'].mean():.2f} ms")
    col2.metric("Average Turnaround Time", f"{results_df['Turnaround Time'].mean():.2f} ms")
    
    st.write("<br>", unsafe_allow_html=True)
    
    # --- 9. Ready Queue Trace (NEW FEATURE) ---
    st.subheader("3. Ready Queue Decision Trace")
    st.write("This log shows the state of the Ready Queue at every scheduling decision point.")
    rq_df = pd.DataFrame(ready_queue_log)
    st.dataframe(rq_df, use_container_width=True, hide_index=True)
    
    st.write("<br>", unsafe_allow_html=True)

    # --- 10. Visual Output (Gantt) ---
    st.subheader("4. Execution Timeline (Gantt Chart)")
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
        height=350,
        plot_bgcolor='#0B1121', 
        paper_bgcolor='#0B1121', 
        font=dict(color="#F8FAFC"),
        xaxis=dict(showgrid=True, gridcolor='#1E293B', fixedrange=True, dtick=1),
        yaxis=dict(showgrid=False, fixedrange=True),
        margin=dict(t=20, b=30, l=10, r=10) 
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # --- 11. Data Output ---
    st.subheader("5. Detailed Calculation Logs")
    st.dataframe(results_df, use_container_width=True, hide_index=True)
