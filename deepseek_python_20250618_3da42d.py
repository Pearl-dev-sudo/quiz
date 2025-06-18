# quiz_app.py
import streamlit as st
from fpdf import FPDF
import base64
from datetime import datetime
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="G35 AI Quiz",
    page_icon=":brain:",
    layout="centered"
)

# Encabezado y subtítulo
st.title("G35 AI Quiz")
st.subheader("Artificial Intelligence Knowledge Assessment")

# Formulario para nombre
with st.form("user_form"):
    full_name = st.text_input("Full Name", placeholder="Enter your full name here")
    
    # Preguntas del quiz
    questions = [
        "What is the primary goal of Machine Learning?",
        "Which neural network architecture is best for image recognition?",
        "What does the term 'overfitting' mean in ML?",
        "Which algorithm is used for unsupervised learning?",
        "What is the purpose of a loss function?",
        "What does NLP stand for?",
        "Which activation function is commonly used in output layers for binary classification?",
        "What is a Transformer in deep learning?",
        "What is the main advantage of using CNNs over fully connected networks for image processing?"
    ]
    
    options = [
        ["A) Mimic human intelligence", "B) Learn from data without explicit programming", "C) Automate repetitive tasks", "D) Create expert systems"],
        ["A) RNN", "B) CNN", "C) LSTM", "D) Transformer"],
        ["A) Model performs well on training data but poorly on new data", "B) Model is too simple", "C) High bias in the model", "D) Model ignores important features"],
        ["A) Linear Regression", "B) K-Means Clustering", "C) Decision Tree", "D) Support Vector Machine"],
        ["A) Measure model accuracy", "B) Quantify the difference between predictions and actual values", "C) Optimize hyperparameters", "D) Regularize the model"],
        ["A) Natural Language Processing", "B) Neural Linguistic Programming", "C) Network Learning Protocol", "D) Native Language Processing"],
        ["A) ReLU", "B) Tanh", "C) Sigmoid", "D) Softmax"],
        ["A) A type of GPU", "B) A neural network architecture using attention mechanisms", "C) A data preprocessing technique", "D) A regularization method"],
        ["A) Better handling of sequential data", "B) Parameter sharing and spatial hierarchy", "C) Higher computational efficiency", "D) Better handling of categorical data"]
    ]
    
    answers = {}
    for i, question in enumerate(questions):
        st.markdown(f"**{i+1}. {question}**")
        answers[i] = st.radio("", options[i], key=f"q{i}", index=None)
    
    submit = st.form_submit_button("Submit Answers")

# Generar PDF
def create_pdf(full_name, answers, questions, options):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Encabezado
    pdf.cell(200, 10, txt="G35 AI Quiz Results", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Participant: {full_name}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(10)
    
    # Respuestas
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt="Quiz Answers:", ln=True)
    pdf.set_font("Arial", size=10)
    
    for i in range(len(questions)):
        pdf.multi_cell(0, 10, txt=f"{i+1}. {questions[i]}")
        pdf.multi_cell(0, 8, txt=f"Answer: {answers[i] if answers[i] else 'Not answered'}")
        pdf.ln(2)
    
    return pdf.output(dest='S').encode('latin1')

# Mostrar resultados y botones después de enviar
if submit:
    if not full_name:
        st.warning("Please enter your full name")
    else:
        st.success("Quiz submitted successfully!")
        
        # Generar contenido para WhatsApp y PDF
        whatsapp_text = f"*G35 AI Quiz Results*\n\n*Name:* {full_name}\n*Date:* {datetime.now().strftime('%Y-%m-%d')}\n\n"
        for i, question in enumerate(questions):
            whatsapp_text += f"*{i+1}. {question}*\nAnswer: {answers[i] if answers[i] else 'Not answered'}\n\n"
        
        # Botón de WhatsApp
        whatsapp_link = f"https://wa.me/?text={whatsapp_text.replace(' ', '%20').replace('\n', '%0A')}"
        st.markdown(f'<a href="{whatsapp_link}" target="_blank"><button style="background-color:#25D366;color:white;border-radius:5px;padding:10px;border:none;cursor:pointer;">Share via WhatsApp</button></a>', unsafe_allow_html=True)
        
        # Botón de PDF
        pdf_data = create_pdf(full_name, answers, questions, options)
        st.download_button(
            label="Download PDF",
            data=pdf_data,
            file_name=f"G35_AI_Quiz_{full_name.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
        
        # Mostrar respuestas en la app
        st.divider()
        st.subheader("Your Answers")
        for i, question in enumerate(questions):
            st.markdown(f"**{i+1}. {question}**")
            st.info(f"Your answer: {answers[i] if answers[i] else 'Not answered'}")