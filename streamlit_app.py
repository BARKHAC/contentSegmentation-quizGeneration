import streamlit as st
import nltk
import PyPDF2
from docx import Document
import random

# Download the punkt tokenizer if it isn't already present
nltk.download('punkt', download_dir='/home/vscode/nltk_data')

# Display the NLTK data path in the Streamlit app

def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF file."""
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ''
    
    for page in reader.pages:
        text += page.extract_text() + '\n'
    
    return text

def extract_text_from_docx(uploaded_file):
    """Extract text from a Word document."""
    doc = Document(uploaded_file)
    text = ''
    
    for para in doc.paragraphs:
        text += para.text + '\n'
    
    return text

def segment_content(text):
    """Segment the text into categories based on keywords."""
    sentences = nltk.sent_tokenize(text)
    segments = {}
    
    for sentence in sentences:
        # Check for keywords to determine the segment
        if "introduction" in sentence.lower():
            segments.setdefault("Introduction", []).append(sentence)
        elif "background" in sentence.lower():
            segments.setdefault("Background", []).append(sentence)
        elif "method" in sentence.lower():
            segments.setdefault("Method", []).append(sentence)
        elif "results" in sentence.lower():
            segments.setdefault("Results", []).append(sentence)
        elif "conclusion" in sentence.lower():
            segments.setdefault("Conclusion", []).append(sentence)
    
    return segments

def generate_questions(segmented_content):
    """Generate quiz questions based on the segmented content."""
    questions = []
    
    for segment in segmented_content.values():
        if segment:  # Ensure there are sentences to work with
            question_sentence = random.choice(segment)
            question = f"What can you tell about: '{question_sentence}'?"
            answer_choices = [
                question_sentence,
                "Something irrelevant.",
                "An answer that is not correct.",
                "Another incorrect option."
            ]
            random.shuffle(answer_choices)  # Shuffle the choices
            
            questions.append({
                'question': question,
                'choices': answer_choices,
                'answer': question_sentence  # The correct answer
            })
    
    return questions

def main():
    """Main function to run the Streamlit app."""
    st.title("Content Extraction and Quiz Generation Tool")
    
    uploaded_file = st.file_uploader("Upload a PDF or Word document", type=["pdf", "docx"])
    
    if uploaded_file is not None:
        # Check the file type and extract text accordingly
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
            st.subheader("Extracted Text from PDF:")
            st.write(text)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_text_from_docx(uploaded_file)
            st.subheader("Extracted Text from Word Document:")
            st.write(text)
        
        # Segment the content
        segmented_content = segment_content(text)
        st.subheader("Segmented Content:")
        for segment, sentences in segmented_content.items():
            st.write(f"{segment}:")
            for sentence in sentences:
                st.write(f"- {sentence}")
        
        # Generate questions based on the segmented content
        questions = generate_questions(segmented_content)
        
        # Display the questions
        st.subheader("Generated Quiz Questions:")
        for idx, q in enumerate(questions):
            st.write(f"{idx + 1}. {q['question']}")
            for choice in q['choices']:
                st.write(f"- {choice}")

if __name__ == "__main__":
    main()
