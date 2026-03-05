import streamlit as st
import ollama
import os
import re
import sqlite3
import bcrypt
os.environ["OLLAMA_NUM_GPU"] = "0"
st.set_page_config(page_title="SmartDiag", layout="centered")
def get_connection():
    return sqlite3.connect('database.db')
def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                car_model TEXT,
                error_code TEXT,
                defective_part TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()
init_db()
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
def add_user(username, email, password):
    try:
        conn = get_connection()
        c = conn.cursor()
        hash_pw = hash_password(password)
        c.execute("INSERT INTO users(username, email, password) VALUES (?, ?, ?)", (username, email, hash_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
def login_user(email, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, password, username FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    if user and check_password(password, user[1]):
        return user[0], user[2]
    return None, None
def add_history(user_id, car_model, error_code, defective_part):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO history (user_id, car_model, error_code, defective_part) VALUES (?, ?, ?, ?)", 
              (user_id, car_model, error_code, defective_part))
    conn.commit()
    conn.close()
def get_history(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT car_model, error_code, defective_part, timestamp FROM history WHERE user_id = ? ORDER BY timestamp DESC LIMIT 5", (user_id,))
    data = c.fetchall()
    conn.close()
    return data
video_mapping = {
    "clutch": "videos/CLUTCH_PEDAL_POSITION_AND-BRAKE_PEDAL_SENZOR.mp4",
    "brake pedal": "videos/CLUTCH_PEDAL_POSITION_AND-BRAKE_PEDAL_SENZOR.mp4",
    "coolant": "videos/COOLANT_TEMPERATURE_SENSOR.mp4",
    "crankshaft": "videos/CRANKSHAFT_POSITION_SENSOR.mp4",
    "egr": "videos/EGR_SYSTEM.mp4",
    "oil": "videos/ENGINE_OIL_SENZOR.mp4",
    "nox": "videos/EXHAUST_GAS_TEMPERATURE-NITROGEN_OXIDE_SENSOR.mp4",
    "nitrogen oxide": "videos/EXHAUST_GAS_TEMPERATURE-NITROGEN_OXIDE_SENSOR.mp4",
    "exhaust gas temperature": "videos/EXHAUST_GAS_TEMPERATURE-NITROGEN_OXIDE_SENSOR.mp4",
    "iat": "videos/IAT_AND_MAP_SENSOR.mp4",
    "intake air temperature": "videos/IAT_AND_MAP_SENSOR.mp4",
    "map": "videos/MAP_SENSOR.mp4",
    "knock": "videos/KNOCK_SENSOR.mp4",
    "maf": "videos/MAF_SENSOR.mp4",
    "mass air flow": "videos/MAF_SENSOR.mp4",
    "oxygen": "videos/OXYGEN_SENSOR_AND_LAMBDA_SESNOR.mp4",
    "o2": "videos/OXYGEN_SENSOR_AND_LAMBDA_SESNOR.mp4",
    "lambda": "videos/OXYGEN_SENSOR_AND_LAMBDA_SESNOR.mp4",
    "rough road": "videos/ROUGHT_ROAD_SENSOR.mp4",
    "throttle": "videos/THROTTLE_POSITION_SENSOR.mp4",
    "tps": "videos/THROTTLE_POSITION_SENSOR.mp4"
}
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None
st.title("SmartDiag - Auto Diagnostic Assistant")
if st.session_state["user_id"] is None:
    st.info("Vă rugăm să vă autentificați pentru a folosi asistentul AI.")
    tab1, tab2 = st.tabs(["Login", "Creare Cont"])
    
    with tab1:
        email_in = st.text_input("Email")
        pass_in = st.text_input("Parolă", type="password")
        if st.button("Intră în cont"):
            uid, uname = login_user(email_in, pass_in)
            if uid:
                st.session_state["user_id"] = uid
                st.session_state["username"] = uname
                st.rerun()
            else:
                st.error("Email sau parolă incorectă.")

    with tab2:
        new_user = st.text_input("Nume utilizator")
        new_email = st.text_input("Email pentru cont")
        new_pass = st.text_input("Parolă nouă", type="password")
        if st.button("Înregistrare"):
            if new_user and new_email and new_pass:
                if add_user(new_user, new_email, new_pass):
                    st.success("Cont creat cu succes! Acum te poți loga.")
                else:
                    st.error("Eroare: Email-ul sau Numele sunt deja folosite.")
            else:
                st.warning("Te rugăm să completezi toate câmpurile.")
else:
    st.sidebar.success(f"Autentificat ca: {st.session_state['username']}")
    if st.sidebar.button("Deconectare"):
        st.session_state["user_id"] = None
        st.rerun()     
    st.sidebar.divider()
    st.sidebar.subheader("Istoric")
    history_data = get_history(st.session_state["user_id"])
    if history_data:
        for item in history_data:
            st.sidebar.caption(f"{item[3][:16]}")
            st.sidebar.text(f"{item[0]} | {item[1]}\nPart: {item[2]}")
            st.sidebar.markdown("---")
    else:
        st.sidebar.info("Nu ai nicio diagnoză recentă.")
    col1, col2 = st.columns(2)
    with col1:
        car_model = st.text_input("Car Model (e.g., VW Golf 7)")
    with col2:
        error_code = st.text_input("Error Code (e.g., P0102)").strip().upper()
    if st.button("Diagnose", type="primary"):
        if car_model and error_code:
            st.divider()
            st.info("Analyzing the issue, please wait...")
            
            prompt = f"""Act as a Senior Master Auto Technician with 20 years of experience specializing in OBD2 diagnostics. Your task is to provide a 100% accurate diagnostic report. Never guess.
            Vehicle: {car_model}
            Error Code: {error_code}
            STRICT RULES:
            1. Provide the exact standard OBD2 definition for this specific code.
            2. Be highly specific. Do not confuse related systems (e.g., MAF vs MAP, O2 vs NOx).
            3. Keep the explanation technical, concise, and purely factual.
            4. You MUST format your response EXACTLY as shown below, with no introductory or concluding chat:
            DEFINITION: [Write standard OBD2 definition here]
            DESCRIPTION: [Write a 2-3 sentence technical explanation of the fault]
            CHECKS: [List 2 initial physical checks the mechanic should perform]
            DEFECTIVE_PART: [Write ONLY the exact name of the main sensor or part, e.g., MAF, MAP, O2 Sensor. Do not write a full sentence.]"""
     
            try:
                response = ollama.chat(model='phi3', messages=[{'role': 'user', 'content': prompt}], options={'temperature': 0.0})
                ai_text = response['message']['content']
                match = re.search(r'DEFECTIVE_PART:\s*(.*)', ai_text, re.IGNORECASE)
                defective_part_name = match.group(1).strip() if match else "Unknown Part"
                add_history(st.session_state["user_id"], car_model, error_code, defective_part_name)
                st.subheader("Issue Explanation")
                st.write(ai_text)
                videos_to_show = []
                if match:
                    search_keyword = defective_part_name.lower()
                    for keyword, video_file in video_mapping.items():
                        pattern = r'\b' + re.escape(keyword) + r'\b'
                        if re.search(pattern, search_keyword) and video_file not in videos_to_show:
                            videos_to_show.append(video_file)
                else:
                    ai_text_lower = ai_text.lower()
                    for keyword, video_file in video_mapping.items():
                        pattern = r'\b' + re.escape(keyword) + r'\b'
                        if re.search(pattern, ai_text_lower) and video_file not in videos_to_show:
                            videos_to_show.append(video_file)
                            
                if videos_to_show:
                    st.subheader("Relevant Sensor Videos")
                    for vid in videos_to_show:
                        if os.path.exists(vid):
                            st.video(vid)
                        else:
                            st.warning(f"Found a match, but the file `{vid}` is missing from your folder.")
                else:
                    st.info("No specific video available for this component yet.")   
            except Exception as e:
                st.error(f"Ollama connection error: {e}")
        else:
            st.error("Please enter both the car model and the error code!")