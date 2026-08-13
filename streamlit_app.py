import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="SJF CPU Scheduling", 
    page_icon="✨", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. "SERENE" LUXURY WELLNESS THEME CSS ---
st.markdown("""
<style>
    /* Import Luxury Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* Global Dark Background & Fonts */
    [data-testid="stAppViewContainer"], .stApp { background-color: #0a0608 !important; font-family: 'Inter', sans-serif; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0) !important; }

    html, body { overflow-x: hidden !important; color: white; font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 2rem !important; padding-bottom: 5rem !important; max-width: 95% !important; }
    
    /* Typography */
    .brand-logo { font-family: 'Dancing Script', cursive; font-size: 2rem; text-align: center; color: white; margin-bottom: 10px; }
    .main-title { 
        color: #FFFFFF; font-size: 4.5rem; font-weight: normal; text-align: center; margin-bottom: 0px; 
        font-family: 'Instrument Serif', serif; line-height: 0.9; letter-spacing: -0.02em;
        text-shadow: 0 0 40px rgba(255, 255, 255, 0.4), 0 0 80px rgba(255, 255, 255, 0.2), 0 0 120px rgba(255, 255, 255, 0.1);
    }
    .sub-title { 
        color: rgba(255,255,255,0.7); font-size: 0.9rem; font-weight: 300; text-align: center; margin-bottom: 3.5rem; 
        text-transform: uppercase; letter-spacing: 3px; font-family: 'Inter', sans-serif; margin-top: 1.5rem;
    }
    h3 { 
        color: #FFFFFF !important; padding-bottom: 15px; border-bottom: 1px solid rgba(255,255,255,0.15); 
        margin-top: 2.5rem !important; font-family: 'Instrument Serif', serif; font-size: 2.5rem !important; 
        font-weight: normal !important; letter-spacing: 1px; 
    }

    /* Liquid Glass Containers */
    div[data-testid="metric-container"], [data-testid="stDataEditor"], [data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.02) !important;
        background-blend-mode: luminosity;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
        border-radius: 16px !important;
        padding: 1.5rem;
    }
    
    div[data-testid="metric-container"] { border-left: none !important; }
    div[data-testid="metric-container"] label { color: rgba(255,255,255,0.6) !important; font-weight: 400 !important; font-size: 0.85rem !important; text-transform: uppercase; letter-spacing: 2px; }
    div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 3.5rem !important; font-weight: normal !important; font-family: 'Instrument Serif', serif; text-shadow: 0 0 30px rgba(255, 255, 255, 0.2); }

    /* Button Glow (White Pill) */
    .stButton > button {
        background: #FFFFFF !important; color: #0a0608 !important; font-weight: 500 !important; font-size: 1rem !important; 
        padding: 1rem 2.5rem !important; border-radius: 9999px !important; border: none !important; width: 100%; margin-top: 10px; 
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.3), 0 0 40px rgba(255, 255, 255, 0.1) !important;
        font-family: 'Inter', sans-serif; letter-spacing: 0.05em; transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: rgba(255,255,255,0.9) !important; transform: scale(1.02);
        box-shadow: 0 0 30px rgba(255, 255, 255, 0.4), 0 0 60px rgba(255, 255, 255, 0.2) !important;
    }

    /* Ready Queue Styles (Minimalist Glass) */
    .step-box { 
        background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(10px); 
        border: 1px solid rgba(255,255,255,0.1); padding: 25px; border-radius: 12px; margin-bottom: 20px; 
        box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.05);
    }
    .array-wrapper { display: flex; align-items: center; margin: 15px 0; overflow-x: auto; padding-bottom: 5px; }
    .array-label { font-size: 0.9rem; color: rgba(255,255,255,0.6); margin-right: 20px; font-weight: 400; white-space: nowrap; font-family: 'Inter', sans-serif; text-transform: uppercase; letter-spacing: 1.5px;}
    .array-container { display: inline-flex; border: 1px solid rgba(255,255,255,0.2); background: rgba(0, 0, 0, 0.3); border-radius: 8px; overflow: hidden; }
    .array-cell { padding: 12px 28px; border-right: 1px solid rgba(255,255,255,0.2); color: #FFFFFF; font-size: 1.5rem; font-weight: normal; min-width: 70px; text-align: center; font-family: 'Instrument Serif', serif;}
    .array-cell:last-child { border-right: none; }
    
    /* Highlighted Queue Cell */
    .array-cell.selected { background: rgba(255, 255, 255, 0.15); color: #FFFFFF; text-shadow: 0 0 15px rgba(255,255,255,0.5); }
    .array-cell.idle { color: rgba(255,255,255,0.3); font-style: italic; }

    @media (max-width: 768px) {
        .block-container { padding: 1.5rem 1rem 3rem 1rem !important; }
        .main-title { font-size: 3rem !important; }
        .sub-title { font-size: 0.75rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- 4. Header ---
st.markdown("<div class='brand-logo'>Serene</div>", unsafe_allow_html=True)
st.markdown("<div class='main-title'>Shortest Job First.</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Refined scheduling, delivered with intention.</div>", unsafe_allow_html=True)

# --- 5. State Management ---
if 'processes' not in st.session_state:
    st.session_state.processes = pd.DataFrame({
        'Process': ['P1', 'P2', 'P3', 'P4'],
        'Arrival Time': [0, 1, 2, 3],
        'Burst Time': [6, 4, 2, 1]
    })

# --- 6. Inputs ---
st.subheader("Process Configuration")
edited_df = st.data_editor(st.session_state.processes, num_rows="dynamic", use_container_width=True)

# --- 7. Core Execution Logic ---
if st.button("Begin your sequence"):
    clean_df = edited_df.dropna().copy()
    
    if clean_df.empty:
        st.error("Please enter at least one valid process in the table.")
    else:
        try:
            processes = []
            for i, row in clean_df.iterrows():
                proc_id = str(row['Process']).strip()
                at = int(float(row['Arrival Time']))
                bt = int(float(row['Burst Time']))
                
                if bt <= 0:
                    st.error(f"Process {proc_id} must have a Burst Time greater than 0.")
                    st.stop()
                if at < 0:
                    st.error(f"Process {proc_id} cannot have a negative Arrival Time.")
                    st.stop()
                    
                processes.append({
                    'id': proc_id, 'at': at, 'bt': bt,
                    'ct': 0, 'tat': 0, 'wt': 0, 'is_completed': False
                })
            
            completed = 0
            current_time = 0
            n = len(processes)
            
            gantt_data = []
            queue_log = []

            while completed < n:
                available = [p for p in processes if p['at'] <= current_time and not p['is_completed']]
                
                if available:
                    available.sort(key=lambda x: (x['bt'], x['at'], x['id']))
                    queue_state = [{'id': p['id'], 'bt': p['bt']} for p in available]
                    current_p = available[0]
                    
                    queue_log.append({
                        'time': current_time, 'is_idle': False,
                        'queue_state': queue_state, 'selected': current_p['id'], 'burst': current_p['bt']
                    })
                    
                    start_time = current_time
                    current_time += current_p['bt']
                    
                    gantt_data.append({
                        'Task': current_p['id'], 
                        'Start': start_time, 
                        'Finish': current_time, 
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
                    queue_log.append({'time': current_time, 'is_idle': True})
                    start_time = current_time
                    current_time += 1
                    if not gantt_data or gantt_data[-1]['Task'] != 'IDLE':
                        gantt_data.append({'Task': 'IDLE', 'Start': start_time, 'Finish': current_time, 'Duration': 1})
                    else:
                        gantt_data[-1]['Finish'] = current_time
                        gantt_data[-1]['Duration'] += 1

            # --- 8. Metrics Output ---
            st.divider()
            results_df = pd.DataFrame(processes)
            results_df = results_df[['id', 'at', 'bt', 'ct', 'tat', 'wt']]
            results_df.columns = ['Process', 'Arrival Time', 'Burst Time', 'Completion Time', 'Turnaround Time', 'Waiting Time']
            
            st.subheader("Radiant Performance")
            col1, col2 = st.columns(2)
            col1.metric("Average Waiting Time", f"{results_df['Waiting Time'].mean():.2f} ms")
            col2.metric("Average Turnaround Time", f"{results_df['Turnaround Time'].mean():.2f} ms")
            
            st.write("<br>", unsafe_allow_html=True)
            
            # --- 9. Dynamic Ready Queue Visualizer ---
            st.subheader("Dynamic States")
            
            html_content = ""
            for log in queue_log:
                if log['is_idle']:
                    html_content += f"""
                    <div class='step-box'>
                        <div style='color:rgba(255,255,255,0.8); font-family: "Instrument Serif", serif; font-size: 1.5rem; margin-bottom:8px;'>Time {log['time']} ms</div>
                        <div class='array-wrapper'>
                            <div class='array-label'>Queue State</div>
                            <div class='array-container'><div class='array-cell idle'>Empty</div></div>
                        </div>
                        <div style='color:rgba(255,255,255,0.5); font-weight:300; font-size: 0.9em; letter-spacing: 0.5px;'>Silence. Awaiting processes.</div>
                    </div>
                    """
                else:
                    cells_html = ""
                    for i, p in enumerate(log['queue_state']):
                        if i == 0:
                            cells_html += f"<div class='array-cell selected'>{p['id']}</div>"
                        else:
                            cells_html += f"<div class='array-cell'>{p['id']}</div>"
                    
                    html_content += f"""
                    <div class='step-box'>
                        <div style='color:rgba(255,255,255,0.8); font-family: "Instrument Serif", serif; font-size: 1.5rem; margin-bottom:8px;'>Time {log['time']} ms</div>
                        <div class='array-wrapper'>
                            <div class='array-label'>Queue State</div>
                            <div class='array-container'>{cells_html}</div>
                        </div>
                        <div style='color:rgba(255,255,255,0.9); font-weight:300; font-size: 0.9em; letter-spacing: 0.5px;'>Selecting {log['selected']} — {log['burst']} ms burst.</div>
                    </div>
                    """
            st.markdown(html_content, unsafe_allow_html=True)
            st.write("<br>", unsafe_allow_html=True)

            # --- 10. FIXED Plotly Gantt Chart (Monochrome Luxury Theme) ---
            st.subheader("Execution Timeline")
            
            if gantt_data:
                df_gantt = pd.DataFrame(gantt_data)
                
                fig = px.bar(
                    df_gantt, 
                    x="Duration", 
                    y="Task", 
                    base="Start", 
                    color="Task", 
                    orientation='h', 
                    text="Task",
                    color_discrete_sequence=['#ffffff', '#cccccc', '#999999', '#666666', '#333333'] # Sleek greyscale palette
                )
                
                fig.update_yaxes(autorange="reversed")
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", 
                    plot_bgcolor="rgba(255,255,255,0.02)",
                    font_color="#FFFFFF", 
                    font_family="Inter",
                    xaxis_title="Timeline (ms)", 
                    yaxis_title="Processes", 
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=20),
                    showlegend=False
                )
                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(255,255,255,0.08)")
                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(255,255,255,0.08)")
                
                st.plotly_chart(fig, use_container_width=True)

            # --- 11. Detailed Logs ---
            st.subheader("Detailed Logs")
            st.dataframe(results_df, use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Input Processing Error: {str(e)}")
