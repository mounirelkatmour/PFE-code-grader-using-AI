from flask import Flask, request, render_template
import google.generativeai as genai
from config import GOOGLE_GENAI_API_KEY  # Import the API key from the config file

# Configure the Generative AI model with the API key
genai.configure(api_key=GOOGLE_GENAI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    grade = None
    if request.method == 'POST':
        context = request.form['context']
        code = request.form['code']
        
        # Clear and concise grading prompt
        grading_prompt = f"""
        Grade the following code based on its functionality and correctness in the provided context:
        1. Start with a grade of 20/20.
        2. Deduct 0.1 points for every 10 syntax mistakes (round down to the nearest integer).
        3. Deduct up to 10 points for critical errors that prevent the code from running.
        4. Always output the grade as X/20, where X is an integer.
        6. The expected output is the grade in this format X/20 only without any explications.

        Context: {context}
        Code: {code}
        """
        
        # Generate the grade using the AI model
        response = model.generate_content(grading_prompt)
        grade = response.text

    return render_template('index.html', grade=grade)

if __name__ == '__main__':
    app.run(debug=True)
