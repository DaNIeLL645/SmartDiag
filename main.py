import streamlit as st
import ollama
import os
import re
os.environ["OLLAMA_NUM_GPU"] = "0" 
st.set_page_config(page_title="SmartDiag", layout="centered")
st.title("SmartDiag - Auto Diagnostic Assistant")

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
            response = ollama.chat(model='llama3.1', messages=[{'role': 'user', 'content': prompt}], options={'temperature': 0.0})
            ai_text = response['message']['content']
            st.subheader("Issue Explanation")
            st.write(ai_text)
            match = re.search(r'DEFECTIVE_PART:\s*(.*)', ai_text, re.IGNORECASE)
            videos_to_show = []
            if match:
                defective_part_name = match.group(1).lower()
                for keyword, video_file in video_mapping.items():
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                    if re.search(pattern, defective_part_name) and video_file not in videos_to_show:
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