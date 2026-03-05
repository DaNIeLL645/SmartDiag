import streamlit as st
import ollama
import os

# Setări interfață
st.set_page_config(page_title="SmartDiag", page_icon="🚗")
st.title("🚗 SmartDiag - Asistent Diagnoză Auto")

# Aici vom lega codurile de eroare de videoclipurile tale
video_database = {
    "P0102": "videos/P0102.mp4",
    "P0135": "videos/P0135.mp4"
}

# Căsuțele unde utilizatorul introduce datele
col1, col2 = st.columns(2)
with col1:
    car_model = st.text_input("Modelul Mașinii (ex: VW Golf 7)")
with col2:
    error_code = st.text_input("Cod Eroare (ex: P0102)").strip().upper()

# Butonul care pornește AI-ul
if st.button("Diagnostichează"):
    if car_model and error_code:
        st.info("⏳ Analizez problema...")
        
        prompt = f"Ești un mecanic auto. Explică scurt în română ce înseamnă codul {error_code} pentru {car_model}. Ce piesă e defectă?"
        
        try:
            # Apelăm Ollama
            response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
            
            st.subheader("💡 Explicația Problemei")
            st.write(response['message']['content'])
            
            # Partea de video
            st.subheader("🎥 Senzor / Tutorial")
            video_path = video_database.get(error_code)
            
            if video_path and os.path.exists(video_path):
                st.video(video_path)
            else:
                st.warning(f"Nu ai adăugat încă un video pentru {error_code} în folderul 'videos'.")
                
        except Exception as e:
            st.error(f"Eroare Ollama. Ai pornit aplicația Ollama pe PC? Detalii: {e}")
    else:
        st.error("Introdu modelul și codul de eroare!")