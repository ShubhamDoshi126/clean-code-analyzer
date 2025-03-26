import os
import gradio as gr
from ui import create_ui

# Create example files directory if it doesn't exist
os.makedirs("examples", exist_ok=True)

# Create the Gradio UI
app = create_ui()

# Launch the app with Hugging Face Spaces compatible settings
if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",  # Required for Hugging Face Spaces
        server_port=7860,       # Default port for Hugging Face Spaces
        share=False,            # No need for sharing link on Spaces
        debug=False             # Disable debug mode in production
    )
