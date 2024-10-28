import streamlit as st
from groq import Groq
import os
import base64
# Initialize Groq client
client = Groq(api_key=os.getenv("groq"))

# Function to generate a learning path using Groq's LLaMA 3 model
def generate_learning_path(learning_goal, skill_level):
    prompt = f"Generate a personalized learning path for learning {learning_goal}. The user is at {skill_level} level."
    
    # API request to Groq's LLaMA 3 model
    completion = client.chat.completions.create(
        model="llama3-8b-8192",  # Adjust based on the correct LLaMA model version
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=1024,
        top_p=1
    )

    # Extract the content correctly from the 'choices' field
    generated_content = completion.choices[0].message.content
    
    return generated_content

# Function to create downloadable checklist as text with checkboxes
def create_downloadable_text(learning_tasks):
    checklist_text = "Personalized Learning Path Checklist\n\n"
    for i, task in enumerate(learning_tasks, 1):
        checklist_text += f"[ ] {task}\n"
    return checklist_text

# Function to create a download link
def download_link(content, filename, file_label="Download"):
    b64 = base64.b64encode(content.encode()).decode()  # Convert to base64
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{file_label}</a>'
    return href

# Customize Streamlit page settings
st.set_page_config(
    page_title="AI-Powered Learning Path Generator",
    page_icon="🎓",
    layout="centered"
)

# App Header
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎓 AI-Powered Personalized Learning Path Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Generate a custom learning path tailored to your goals and skill level!</p>", unsafe_allow_html=True)

# Add a separator line
st.markdown("---")

# Input section with styling
st.markdown("#### Tell us about your learning journey:")

learning_goal = st.text_input(
    "What do you want to learn?", 
    "Python programming", 
    help="Enter the skill or topic you want to master."
)

skill_level = st.selectbox(
    "Your current skill level", 
    ["Beginner", "Intermediate", "Advanced"],
    help="Choose your current level of proficiency in the selected topic."
)

# Add a call to action button with a gradient
st.markdown(
    """
    <style>
    .stButton>button {
        background: linear-gradient(90deg, #4CAF50, #66BB6A);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: none;
        font-size: 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: #388E3C;
        color: white;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

def hide_streamlit_style():
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

hide_streamlit_style()
# Generate learning path button
if st.button("Generate Learning Path"):
    if learning_goal:
        learning_path = generate_learning_path(learning_goal, skill_level)
        st.markdown("### 🎯 Your Personalized Learning Path:")
        st.write(learning_path)
        
        # Split learning path into tasks
        learning_tasks = [task.strip() for task in learning_path.split("\n") if task.strip()]
        
        # Create downloadable text with the checklist format
        checklist_text = create_downloadable_text(learning_tasks)
        
        # Display download link for the checklist
        st.markdown(download_link(checklist_text, f"{skill_level} {learning_goal} learning path.txt", "📥 Download Your Learning Path with Checkboxes"), unsafe_allow_html=True)

# Add another separator line
st.markdown("---")

# Motivational message with emoji
st.markdown("### 🌟 Keep Learning!")
st.info("Keep learning and advancing! You're doing great. 🎉")

# Footer with a clean message
st.markdown("<footer style='text-align: center;'>Made with ❤️ by your AI assistant.</footer>", unsafe_allow_html=True)
