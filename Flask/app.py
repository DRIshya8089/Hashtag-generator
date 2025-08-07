import os
from flask import Flask, render_template, request, flash
from config import GEMINI_API_KEY
import logging
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "your-default-secret-key")
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET', 'POST'])
def index():
    description = None
    input_text = ""
    if request.method == 'POST':
        input_text = request.form.get('input_text', '').strip()
        if not input_text:
            flash("Please enter some text to generate a caption and hashtags.", "warning")
        elif not GEMINI_API_KEY:
            flash("Gemini API key is not set. Please set the GEMINI_API_KEY environment variable.", "danger")
        else:
            prompt = (
                "You are a helpful assistant that generates creative Instagram captions and relevant hashtags.\n"
                f"Write a catchy 2-line Instagram caption and 10 relevant hashtags for this post: '{input_text}'. "
                "Keep the total under 100 characters."
            )
            try:
                response = model.generate_content(prompt)
                description = response.text.strip()
            except Exception as e:
                import traceback
                traceback.print_exc()
                flash(f"Error: {str(e)}", "danger")
    return render_template('index.html', description=description, input_text=input_text)

if __name__ == '__main__':
    app.run(debug=True)
