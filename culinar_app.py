import streamlit as st
from openai import OpenAI
import base64

# Configurare pagină
st.set_page_config(page_title="AI Fridge Chef", layout="wide")

# Adăugăm CSS pentru fundal cu legume și stilizare
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f0f7f0;
    background-image: url("https://img.freepik.com/free-vector/vegetables-seamless-pattern_1284-46904.jpg");
    background-size: cover;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("👨‍🍳 AI Fridge Chef")
st.write("Încarcă o poză cu frigiderul tău și primește o rețetă delicioasă!")

# Configurare OpenAI
# Asigură-te că în Streamlit Cloud, la Settings -> Secrets ai pus: OPENAI_API_KEY = "sk-..."
api_key = st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("Cheia API nu este setată! Mergi la Settings -> Secrets în Streamlit Cloud.")
else:
    client = OpenAI(api_key=api_key)
    
    uploaded_file = st.file_uploader("Alege o poză...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Poza ta", use_column_width=True)
        
        if st.button("Generează rețeta!"):
            with st.spinner("Chef AI gătește..."):
                # Conversie imagine în base64
                image_data = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
                
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Ce pot găti cu ingredientele din această poză? Oferă-mi o rețetă simplă și delicioasă."},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}},
                                ],
                            }
                        ],
                    )
                    st.success("Rețeta ta:")
                    st.write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"A apărut o eroare: {e}")
