
import os
import gradio as gr
from google import genai

# Get Gemini API key
API_KEY = os.getenv("Gemini_api")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured.")

# Create Gemini client
client = genai.Client(api_key=API_KEY)


def generate_questions(topic, difficulty, question_type, number_of_questions):

    if not topic.strip():
        return "⚠️ Please enter a topic."

    prompt = f"""
You are an educational question generator.

Generate exactly {number_of_questions} questions.

Topic: {topic}
Difficulty: {difficulty}
Question Type: {question_type}

Requirements:
- Make every question clear and educational.
- Match the selected difficulty.
- Number each question.

If the question type is Multiple Choice:
- Give four options A, B, C, and D.
- Give the correct answer.

If the question type is True/False:
- Give the correct True/False answer.

If the question type is Short Answer:
- Give a suitable short answer.

Format the output neatly.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"❌ Error: {str(e)}"


# Gradio interface
with gr.Blocks(title="Interactive Question Generator") as demo:

    gr.Markdown(
        """
        # 🧠 Interactive Question Generator

        Generate educational questions using **Google Gemini AI**.
        """
    )

    with gr.Row():

        with gr.Column():

            topic = gr.Textbox(
                label="📚 Enter Topic",
                placeholder="Example: Python Programming"
            )

            difficulty = gr.Dropdown(
                choices=["Easy", "Medium", "Hard"],
                value="Medium",
                label="🎯 Difficulty"
            )

            question_type = gr.Dropdown(
                choices=[
                    "Multiple Choice",
                    "True/False",
                    "Short Answer"
                ],
                value="Multiple Choice",
                label="📝 Question Type"
            )

            number_of_questions = gr.Slider(
                minimum=1,
                maximum=20,
                value=5,
                step=1,
                label="🔢 Number of Questions"
            )

            generate_button = gr.Button(
                "🚀 Generate Questions"
            )

        with gr.Column():

            output = gr.Markdown(
                label="Generated Questions"
            )

    generate_button.click(
        fn=generate_questions,
        inputs=[
            topic,
            difficulty,
            question_type,
            number_of_questions
        ],
        outputs=output
    )


# Start Gradio
if __name__ == "__main__":
    demo.launch(
        share=True,
        server_name="0.0.0.0"
    )
