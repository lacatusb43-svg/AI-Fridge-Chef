import streamlit as st
from openai import OpenAI
import base64

# Configurare pagină
st.set_page_config(page_title="AI Fridge Chef", page_icon="👨‍🍳")

st.title("👨‍🍳 AI Fridge Chef")
st.write("Încarcă o poză cu frigiderul tău și primește o rețetă!")

# Folosim variabilele de mediu pentru securitate (sau poți pune cheia aici doar pentru test)
# Pe Streamlit Cloud, cheia va veni din "Secrets"
api_key = st.secrets.get("OPENAI_API_KEY") or "PUNE_CHEIA_AICI"
client = OpenAI(api_key=api_key)

uploaded_file = st.file_uploader("Alege o poză...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Frigiderul tău', use_column_width=True)
    
    if st.button("Generează rețeta"):
        with st.spinner('Chef-ul AI gătește...'):
            try:
                # Citire și codare imagine
                image_data = base64.b64encode(uploaded_file.read()).decode('utf-8')
                
                # Apel API
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "user", "content": [
                            {"type": "text", "text": "Ești un Chef profesionist. Analizează ingredientele din poză și propune o rețetă delicioasă, explicată pas cu pas."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                        ]}
                    ]
                )
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"A apărut o eroare: {e}")