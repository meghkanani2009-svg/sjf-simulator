import streamlit as st
import pandas as pd
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

# --- 3. Advanced CSS: Desktop, Mobile Overrides & EXACT Textbook Array Style ---
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
    
    /* Typography */
    .main-title { color: #FFFFFF; font-size: 3.5rem; font-weight: 900; text-align: center; margin-bottom: 0px; }
    .sub-title { color: #38BDF8; font-size: 1.2rem; font-weight: 600; text-align: center; margin-bottom: 3rem; text-transform: uppercase; }
    h3 { color: #F8FAFC !important; padding-bottom: 10px; border-bottom: 2px solid rgba(255,255,255,0.1); margin-top: 2rem !important; }

    /* Tables & Cards */
    div[data-testid="metric-container"] {
        background: rgba(15, 23, 42, 0.85); 
        border: 1px solid #1E293B; border-left: 6px solid #00F6FF; 
        padding: 1.5rem; border-radius: 12px;
    }
    div[data-testid="metric-container"] label { color: #94A3B8 !important; font-weight: 700 !important; text-transform: uppercase; }
    div[data-testid="stMetricValue"] { color: #00F6FF !important; font-size: 3rem !important; font-weight: 900 !important; }
    
    [data-testid="stDataEditor"], [data-testid="stDataFrame"] {
        background: rgba(11, 17, 33, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 1.5rem;
    }

    .stButton > button {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%); color: white; font-weight: 800; font-size: 1.2rem; padding: 0.8rem 2.5rem; border-radius: 8px; border: none; width: 100%; margin-top: 10px;
    }
    .stButton > button:hover { background: linear-gradient(135deg, #0369A1 0%, #075985 100%); color: #00F6FF; }

    /* =========================================
       📏 TEXTBOOK STRAIGHT-LINE ARRAY CSS
       ========================================= */
    .array-container {
        display: flex;
        flex-direction: row;
        align-items: center;
        margin: 40px 0 60px 0;
        overflow-x: auto;
        padding-bottom: 30px;
        -webkit-overflow-scrolling: touch;
    }
    .array-container::-webkit-scrollbar { height: 8px; }
    .array-container::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.05); border-radius: 10px; }
    .array-container::-webkit-scrollbar-thumb { background: #38BDF8; border-radius: 10px; }

    .array-box {
        border: 2px solid #F8FAFC;
        border-right: none;
        padding: 15px 35px;
        font-size: 1.4rem;
        font-weight: 900;
        color: #F8FAFC;
        position: relative;
        text-align: center;
        background: rgba(15, 23, 42, 0.8);
        min-width: 80px;
    }
    .array-box:last-child {
        border-right: 2px solid #F8FAFC; /* Close the array at the end */
    }
    .array-box.idle {
        color: #F87171;
        font-style: italic;
    }
    
    /* Timestamps exactly on the dividers */
    .time-start {
        position: absolute;
        bottom: -35px;
        left: -12px; /* Shifts text left to align under the border */
        color: #94A3B8;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .time-end {
        position: absolute;
        bottom: -35px;
        right: -12px;
        color: #94A3B8;
        font-size: 1.2rem;
        font-weight: bold;
    }

    @media (max-width: 768px) {
        .block-container { padding-top: 1.5rem !important; padding-left: 1rem !important; padding-right: 1rem !important; padding-bottom: 3rem !important; }
        .main-title { font-size: 2rem !important; }
        .sub-title { font-size: 0.9rem !important; }
        .array-box { padding: 12px 20px; font-size: 1.1rem; min-width: 60px; }
        .time-start, .time-end { font-size: 1rem; bottom: -30px; }
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
edited_df = st.data_editor(st.session_state.processes, num_rows="dynamic", use_container_width=True)

# --- 7. Core Logic ---
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
    
    # --- 9. TEXTBOOK STYLE READY QUEUE ---
    st.subheader("3. Ready Queue Sequence")
    st.write("The order in which processes entered the CPU, formatted exactly like your notebook.")
    
    rq_html = "<div class='array-container' style='margin-bottom: 20px;'>"
    # Filter out IDLE times for the ready queue sequence
    rq_sequence = [t for t in gantt_data if t['Task'] != 'IDLE']
    
    if not rq_sequence:
        rq_html += "<div class='array-box idle' style='border-right: 2px solid #F8FAFC;'>Empty</div>"
    else:
        for i, task in enumerate(rq_sequence):
            # The last box needs a right border to close the array
            is_last = (i == len(rq_sequence) - 1)
            border_style = "border-right: 2px solid #F8FAFC;" if is_last else ""
            rq_html += f"<div class='array-box' style='{border_style}'>{task['Task']}</div>"
    
    rq_html += "</div>"
    st.markdown(rq_html, unsafe_allow_html=True)


    # --- 10. TEXTBOOK STYLE GANTT CHART ---
    st.subheader("4. Execution Timeline (Gantt Chart)")
    st.write("The execution timeline with timestamps exactly underneath the array dividers.")
    
    gantt_html = "<div class='array-container'>"
    
    if not gantt_data:
        gantt_html += "<div class='array-box idle' style='border-right: 2px solid #F8FAFC;'>No Data</div>"
    else:
        for i, task in enumerate(gantt_data):
            is_last = (i == len(gantt_data) - 1)
            end_time = task['Start'] + task['Duration']
            
            # Print the end time ONLY on the very last box to complete the timeline
            end_time_html = f"<div class='time-end'>{end_time}</div>" if is_last else ""
            
            # Highlight IDLE states in red
            css_class = "array-box idle" if task['Task'] == 'IDLE' else "array-box"
            
            gantt_html += f"""
            <div class='{css_class}'>
                {task['Task']}
                <div class='time-start'>{task['Start']}</div>
                {end_time_html}
            </div>
            """
            
    gantt_html += "</div>"
    st.markdown(gantt_html, unsafe_allow_html=True)

    # --- 11. Data Output ---
    st.subheader("5. Detailed Calculation Logs")
    st.dataframe(results_df, use_container_width=True, hide_index=True)
