import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="SJF CPU Scheduling Pro", 
    page_icon="⏱️", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. LITHOS DYNAMIC SPOTLIGHT BACKGROUND INJECTOR ---
lithos_bg_html = """
<script>
const pDoc = window.parent.document;
if (!pDoc.getElementById('lithos-bg')) {
    const bgContainer = pDoc.createElement('div');
    bgContainer.id = 'lithos-bg';
    Object.assign(bgContainer.style, {
        position: 'fixed', top: '0', left: '0', width: '100vw', height: '100vh', zIndex: '-999', pointerEvents: 'none'
    });

    const bg1 = pDoc.createElement('div');
    Object.assign(bg1.style, {
        position: 'absolute', inset: '0', 
        background: 'url("https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260609_195923_b0ba8ace-1d1d-4f2c-9a28-1ab84b330680.png&w=1280&q=85") center/cover no-repeat'
    });

    const bg2 = pDoc.createElement('div');
    Object.assign(bg2.style, {
        position: 'absolute', inset: '0', 
        background: 'url("https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260609_201152_bba90a12-bf12-459f-91f0-51f237dbaf3b.png&w=1280&q=85") center/cover no-repeat'
    });

    bgContainer.appendChild(bg1);
    bgContainer.appendChild(bg2);
    pDoc.body.prepend(bgContainer);

    const canvas = pDoc.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const SPOTLIGHT_R = 260;

    let mouse = { x: -999, y: -999 };
    let smooth = { x: -999, y: -999 };

    function resize() {
        canvas.width = window.parent.innerWidth;
        canvas.height = window.parent.innerHeight;
    }
    window.parent.addEventListener('resize', resize);
    resize();

    pDoc.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
        if (smooth.x === -999) {
            smooth.x = e.clientX;
            smooth.y = e.clientY;
        }
    });

    function renderLoop() {
        if (smooth.x !== -999) {
            smooth.x += (mouse.x - smooth.x) * 0.1;
            smooth.y += (mouse.y - smooth.y) * 0.1;

            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const gradient = ctx.createRadialGradient(smooth.x, smooth.y, 0, smooth.x, smooth.y, SPOTLIGHT_R);
            gradient.addColorStop(0, 'rgba(255,255,255,1)');
            gradient.addColorStop(0.4, 'rgba(255,255,255,1)');
            gradient.addColorStop(0.6, 'rgba(255,255,255,0.75)');
            gradient.addColorStop(0.75, 'rgba(255,255,255,0.4)');
            gradient.addColorStop(0.88, 'rgba(255,255,255,0.12)');
            gradient.addColorStop(1, 'rgba(255,255,255,0)');

            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.arc(smooth.x, smooth.y, SPOTLIGHT_R, 0, Math.PI * 2);
            ctx.fill();

            const maskUrl = canvas.toDataURL();
            bg2.style.maskImage = `url(${maskUrl})`;
            bg2.style.webkitMaskImage = `url(${maskUrl})`;
            bg2.style.maskSize = '100% 100%';
            bg2.style.webkitMaskSize = '100% 100%';
        }
        window.parent.requestAnimationFrame(renderLoop);
    }
    renderLoop();
}
</script>
"""
components.html(lithos_bg_html, width=0, height=0)

# --- 3. LITHOS-THEMED CSS FOR STREAMLIT ---
st.markdown("""
<style>
    /* Transparent backgrounds to show Lithos */
    [data-testid="stAppViewContainer"], .stApp { background: transparent !important; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0) !important; }

    html, body { overflow-x: hidden !important; }
    .block-container { padding-top: 2rem !important; padding-bottom: 5rem !important; max-width: 95% !important; }
    
    /* Typography matching Lithos vibe */
    .main-title { color: #FFFFFF; font-size: 3.5rem; font-weight: 900; text-align: center; margin-bottom: 0px; text-shadow: 0 8px 16px rgba(0,0,0,0.9); font-family: 'Playfair Display', serif; font-style: italic; }
    .sub-title { color: #e8702a; font-size: 1.2rem; font-weight: 600; text-align: center; margin-bottom: 3rem; text-transform: uppercase; text-shadow: 0 4px 8px rgba(0,0,0,0.9); letter-spacing: 2px; }
    h3 { color: #F8FAFC !important; padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); margin-top: 2rem !important; text-shadow: 0 2px 5px rgba(0,0,0,0.8); }

    /* Dark frosted glass containers */
    div[data-testid="metric-container"] {
        background: rgba(10, 10, 10, 0.75); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05); 
        border-left: 6px solid #e8702a; padding: 1.5rem; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }
    div[data-testid="metric-container"] label { color: #94A3B8 !important; font-weight: 600 !important; font-size: 1rem !important; text-transform: uppercase; }
    div[data-testid="stMetricValue"] { color: #e8702a !important; font-size: 3.2rem !important; font-weight: 900 !important; text-shadow: 0 0 15px rgba(232, 112, 42, 0.3); }

    [data-testid="stDataEditor"], [data-testid="stDataFrame"] {
        background: rgba(10, 10, 10, 0.75); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 1.5rem; box-shadow: 0 12px 30px rgba(0,0,0,0.8);
    }

    /* Amber Lithos Button */
    .stButton > button {
        background: linear-gradient(135deg, #e8702a 0%, #c2571a 100%); color: white; font-weight: 800; font-size: 1.2rem; padding: 0.8rem 2.5rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); width: 100%; margin-top: 10px; box-shadow: 0 8px 20px rgba(0,0,0,0.6); transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #f08343 0%, #d2611f 100%); transform: translateY(-3px); box-shadow: 0 12px 25px rgba(232, 112, 42, 0.4); color: white;
    }

    /* Ready Queue Styles (Earthy Tones) */
    .step-box { background: rgba(10, 10, 10, 0.8); backdrop-filter: blur(10px); border-left: 4px solid #e8702a; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-top: 1px solid rgba(255,255,255,0.05); border-right: 1px solid rgba(255,255,255,0.05); border-bottom: 1px solid rgba(255,255,255,0.05); box-shadow: 0 8px 25px rgba(0,0,0,0.6); }
    .array-wrapper { display: flex; align-items: center; margin: 15px 0; overflow-x: auto; padding-bottom: 5px; }
    .array-label { font-size: 1.1rem; color: #94A3B8; margin-right: 20px; font-weight: 600; white-space: nowrap; }
    .array-container { display: inline-flex; border: 2px solid rgba(255,255,255,0.1); background: rgba(0, 0, 0, 0.4); border-radius: 4px; }
    .array-cell { padding: 10px 24px; border-right: 2px solid rgba(255,255,255,0.1); color: #F8FAFC; font-size: 1.3rem; font-weight: bold; min-width: 60px; text-align: center; }
    .array-cell:last-child { border-right: none; }
    
    /* Highlighted Queue Cell matches Lithos Accent */
    .array-cell.selected { background: rgba(232, 112, 42, 0.2); color: #e8702a; border: 2px solid #e8702a; box-shadow: inset 0 0 10px rgba(232, 112, 42, 0.2); }
    .array-cell.idle { color: #64748b; font-style: italic; }

    @media (max-width: 768px) {
        .block-container { padding: 1.5rem 1rem 3rem 1rem !important; }
        .main-title { font-size: 2.2rem !important; }
        .sub-title { font-size: 0.9rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- 4. Header ---
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

# --- 7. Core Execution Logic ---
if st.button("Initialize Execution Sequence 🚀"):
    clean_df = edited_df.dropna().copy()
    
    if clean_df.empty:
        st.error("⚠️ Please enter at least one valid process in the table.")
    else:
        try:
            processes = []
            for i, row in clean_df.iterrows():
                proc_id = str(row['Process']).strip()
                at = int(float(row['Arrival Time']))
                bt = int(float(row['Burst Time']))
                
                if bt <= 0:
                    st.error(f"⚠️ Process {proc_id} must have a Burst Time greater than 0.")
                    st.stop()
                if at < 0:
                    st.error(f"⚠️ Process {proc_id} cannot have a negative Arrival Time.")
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
            
            st.subheader("2. Key Performance Indicators")
            col1, col2 = st.columns(2)
            col1.metric("Average Waiting Time", f"{results_df['Waiting Time'].mean():.2f} ms")
            col2.metric("Average Turnaround Time", f"{results_df['Turnaround Time'].mean():.2f} ms")
            
            st.write("<br>", unsafe_allow_html=True)
            
            # --- 9. Dynamic Ready Queue Visualizer ---
            st.subheader("3. Dynamic Ready Queue Visualizer")
            
            html_content = ""
            for log in queue_log:
                if log['is_idle']:
                    html_content += f"""
                    <div class='step-box'>
                        <div style='color:#94A3B8; font-weight:bold; margin-bottom:8px;'>⏱️ Time = {log['time']} ms</div>
                        <div class='array-wrapper'>
                            <div class='array-label'>Ready Queue:</div>
                            <div class='array-container'><div class='array-cell idle'>Empty</div></div>
                        </div>
                        <div style='color:#64748b; font-weight:500; font-size: 0.95em;'>➔ CPU waits. No processes have arrived yet.</div>
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
                        <div style='color:#94A3B8; font-weight:bold; margin-bottom:8px;'>⏱️ Time = {log['time']} ms</div>
                        <div class='array-wrapper'>
                            <div class='array-label'>Ready Queue:</div>
                            <div class='array-container'>{cells_html}</div>
                        </div>
                        <div style='color:#e8702a; font-weight:600; font-size: 0.95em;'>➔ SJF selects {log['selected']} (BT: {log['burst']} ms)</div>
                    </div>
                    """
            st.markdown(html_content, unsafe_allow_html=True)
            st.write("<br>", unsafe_allow_html=True)

            # --- 10. FIXED Plotly Gantt Chart ---
            st.subheader("4. Execution Timeline (Gantt Chart)")
            
            if gantt_data:
                df_gantt = pd.DataFrame(gantt_data)
                
                # Using px.bar with base offset to fix the integer timeline issue perfectly
                fig = px.bar(
                    df_gantt, 
                    x="Duration", 
                    y="Task", 
                    base="Start", 
                    color="Task", 
                    orientation='h', 
                    text="Task",
                    color_discrete_sequence=['#e8702a', '#f39c6b', '#c2571a', '#8f3e10', '#4a4a4a']
                )
                
                fig.update_yaxes(autorange="reversed")
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", 
                    plot_bgcolor="rgba(10, 10, 10, 0.75)",
                    font_color="#F8FAFC", 
                    xaxis_title="Timeline (ms)", 
                    yaxis_title="Processes", 
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=20),
                    showlegend=False
                )
                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(255,255,255,0.05)")
                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(255,255,255,0.05)")
                
                st.plotly_chart(fig, use_container_width=True)

            # --- 11. Detailed Logs ---
            st.subheader("5. Detailed Calculation Logs")
            st.dataframe(results_df, use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"⚠️ Input Processing Error: {str(e)}")
