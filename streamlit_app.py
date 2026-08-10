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

# --- 3. Advanced CSS: Desktop, Mobile Overrides & Queue Chart Blocks ---
st.markdown(background_css + """
<style>
    html, body {
        overflow-x: hidden !important;
    }

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

    [data-testid="stDataEditor"], [data-testid="stDataFrame"] {
        background: rgba(11, 17, 33, 0.6); 
        backdrop-filter: blur(12px); 
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5);
    }

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
       📦 VISUAL QUEUE CHART BOXES
       ========================================= */
    .step-box {
        background: rgba(15, 23, 42, 0.85);
        border-left: 4px solid #38BDF8;
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .queue-container {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 12px;
        margin-bottom: 15px;
        flex-wrap: wrap; /* Wraps to next line on small phones */
    }
    .queue-box {
        background: #1E293B;
        border: 2px solid #475569;
        padding: 10px 18px;
        border-radius: 6px;
        color: #F8FAFC;
        font-weight: 800;
        text-align: center;
        min-width: 80px;
        box-shadow: inset 0 2px 4px rgba(255,255,255,0.05), 0 4px 6px rgba(0,0,0,0.4);
    }
    .queue-box .bt-label {
        font-size: 0.75rem;
        color: #94A3B8;
        font-weight: 500;
        display: block;
        margin-top: 4px;
        text-transform: uppercase;
    }
    /* Highlight the process picked by SJF */
    .queue-box.selected {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        border-color: #34D399;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.4);
        transform: scale(1.05);
    }
    .queue-box.selected .bt-label {
        color: #ECFDF5;
    }
    /* Highlight for empty queue */
    .queue-box.idle {
        background: linear-gradient(135deg, #991B1B 0%, #DC2626 100%);
        border-color: #F87171;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-top: 1.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-bottom: 3rem !important;
        }
        .main-title { font-size: 1.8rem !important; }
        .sub-title { font-size: 0.85rem !important; margin-bottom: 1.5rem !important; letter-spacing: 1px !important; }
        h3 { font-size: 1.1rem !important; margin-top: 1rem !important; }
        div[data-testid="metric-container"] { padding: 1rem !important; border-left: 4px solid #00F6FF !important; }
        div[data-testid="metric-container"] label { font-size: 0.85rem !important; }
        div[data-testid="stMetricValue"] { font-size: 1.8rem !important; }
        [data-testid="stDataEditor"], [data-testid="stDataFrame"] { padding: 0.5rem !important; }
        .stButton > button { font-size: 1rem !important; padding: 0.6rem 1rem !important; }
        
        /* Mobile scale down for queue boxes */
        .queue-box { padding: 8px 12px; min-width: 60px; font-size: 0.9rem; }
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

# --- 7. Core Logic & Queue Block Tracker ---
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
    queue_log = [] # Tracks data for the block-by-block chart

    while completed < n:
        available = [p for p in processes if p['at'] <= current_time and not p['is_completed']]
        
        if available:
            # Sort by Burst Time (SJF logic)
            available.sort(key=lambda x: (x['bt'], x['at']))
            
            # Save the queue state to draw boxes later
            queue_state = [{'id': p['id'], 'bt': p['bt']} for p in available]
            current_p = available[0]
            
            queue_log.append({
                'time': current_time,
                'is_idle': False,
                'queue_state': queue_state,
                'selected': current_p['id'],
                'burst': current_p['bt']
            })
            
            # Execute
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
            queue_log.append({
                'time': current_time,
                'is_idle': True
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
    
    # --- 9. Visual Box-by-Box Queue Chart ---
    st.subheader("3. Dynamic Ready Queue Visualizer")
    st.write("Visualizes the sorted queue blocks. The green block indicates the Shortest Job selected.")
    
    # Generate the HTML for the blocks dynamically based on python log
    html_content = ""
    for log in queue_log:
        if log['is_idle']:
            html_content += f"""
            <div class='step-box'>
                <div style='color:#94A3B8; font-weight:bold;'>⏱️ Evaluation at Time = {log['time']} ms</div>
                <div class='queue-container'>
                    <div class='queue-box idle'>IDLE<span class='bt-label'>Empty Queue</span></div>
                </div>
                <div style='color:#F87171; font-weight:bold; font-size: 0.95em;'>
                    ➔ CPU waits. No processes have arrived yet.
                </div>
            </div>
            """
        else:
            boxes_html = ""
            for i, p in enumerate(log['queue_state']):
                # The first item in the sorted queue is selected
                if i == 0: 
                    boxes_html += f"<div class='queue-box selected'>{p['id']}<span class='bt-label'>BT: {p['bt']}</span></div>"
                else:
                    boxes_html += f"<div class='queue-box'>{p['id']}<span class='bt-label'>BT: {p['bt']}</span></div>"
            
            html_content += f"""
            <div class='step-box'>
                <div style='color:#94A3B8; font-weight:bold;'>⏱️ Evaluation at Time = {log['time']} ms</div>
                <div class='queue-container'>
                    {boxes_html}
                </div>
                <div style='color:#34D399; font-weight:bold; font-size: 0.95em;'>
                    ➔ Decision: {log['selected']} is dispatched for {log['burst']} ms.
                </div>
            </div>
            """
    
    # Render all the generated HTML
    st.markdown(html_content, unsafe_allow_html=True)

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
