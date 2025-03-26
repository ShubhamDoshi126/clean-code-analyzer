import gradio as gr
import os
import tempfile
from analyzer import analyze_code

def process_file(file_path):
    """Process uploaded file and return analysis results."""
    # Get file extension
    file_extension = os.path.splitext(file_path)[1].lower()
    
    # Check if file extension is supported
    if file_extension not in [".js", ".jsx", ".py"]:
        return {
            "error": f"Unsupported file type: {file_extension}. Please upload a .js, .jsx, or .py file."
        }
    
    # Read file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Analyze code
        result = analyze_code(content, file_extension)
        
        # Format the results for display
        overall_score = result["overall_score"]
        breakdown = result["breakdown"]
        recommendations = result["recommendations"]
        
        # Create formatted output
        output = {
            "overall_score": overall_score,
            "breakdown": breakdown,
            "recommendations": recommendations
        }
        
        return output
    except Exception as e:
        return {
            "error": f"Error analyzing code: {str(e)}"
        }

def create_ui():
    """Create and configure the Gradio UI."""
    with gr.Blocks(title="Code Quality Analyzer", theme=gr.themes.Soft()) as app:
        gr.Markdown(
            """
            # Code Quality Analyzer
            
            Upload a JavaScript (.js), React (.jsx), or Python (.py) file to analyze code quality.
            The analyzer will score your code on clean code practices and provide recommendations for improvement.
            
            ## Scoring Categories:
            - Naming conventions (10 points)
            - Function length and modularity (20 points)
            - Comments and documentation (20 points)
            - Formatting/indentation (15 points)
            - Reusability and DRY principles (15 points)
            - Best practices in web development (20 points)
            """
        )
        
        with gr.Row():
            with gr.Column(scale=1):
                file_input = gr.File(
                    label="Upload Code File",
                    file_types=[".js", ".jsx", ".py"],
                    type="filepath"
                )
                analyze_btn = gr.Button("Analyze Code", variant="primary")
            
            with gr.Column(scale=2):
                with gr.Group():
                    with gr.Row():
                        overall_score = gr.Number(label="Overall Score", value=None, interactive=False)
                    
                    with gr.Row():
                        naming_score = gr.Number(label="Naming Conventions (out of 10)", value=None, interactive=False)
                        modularity_score = gr.Number(label="Modularity (out of 20)", value=None, interactive=False)
                    
                    with gr.Row():
                        comments_score = gr.Number(label="Comments (out of 20)", value=None, interactive=False)
                        formatting_score = gr.Number(label="Formatting (out of 15)", value=None, interactive=False)
                    
                    with gr.Row():
                        reusability_score = gr.Number(label="Reusability (out of 15)", value=None, interactive=False)
                        best_practices_score = gr.Number(label="Best Practices (out of 20)", value=None, interactive=False)
                
                recommendations = gr.Markdown(label="Recommendations")
                error_output = gr.Markdown(visible=False)
        
        # Set up event handlers
        def on_analyze(file):
            if file is None:
                return {
                    error_output: gr.update(value="Please upload a file to analyze.", visible=True),
                    overall_score: None,
                    naming_score: None,
                    modularity_score: None,
                    comments_score: None,
                    formatting_score: None,
                    reusability_score: None,
                    best_practices_score: None,
                    recommendations: ""
                }
            
            result = process_file(file)
            
            if "error" in result:
                return {
                    error_output: gr.update(value=f"**Error:** {result['error']}", visible=True),
                    overall_score: None,
                    naming_score: None,
                    modularity_score: None,
                    comments_score: None,
                    formatting_score: None,
                    reusability_score: None,
                    best_practices_score: None,
                    recommendations: ""
                }
            
            # Format recommendations as markdown list
            recommendations_md = "### Recommendations:\n" + "\n".join([f"- {rec}" for rec in result["recommendations"]])
            
            return {
                error_output: gr.update(visible=False),
                overall_score: result["overall_score"],
                naming_score: result["breakdown"]["naming"],
                modularity_score: result["breakdown"]["modularity"],
                comments_score: result["breakdown"]["comments"],
                formatting_score: result["breakdown"]["formatting"],
                reusability_score: result["breakdown"]["reusability"],
                best_practices_score: result["breakdown"]["best_practices"],
                recommendations: recommendations_md
            }
        
        analyze_btn.click(
            fn=on_analyze,
            inputs=[file_input],
            outputs=[
                error_output,
                overall_score,
                naming_score,
                modularity_score,
                comments_score,
                formatting_score,
                reusability_score,
                best_practices_score,
                recommendations
            ]
        )
        
        # Add examples
        examples_dir = os.path.join(os.path.dirname(__file__), "examples")
        example_files = []
        if os.path.exists(examples_dir):
            for filename in os.listdir(examples_dir):
                if filename.endswith((".js", ".jsx", ".py")):
                    example_files.append(os.path.join(examples_dir, filename))
        
        if example_files:
            gr.Examples(
                examples=example_files,
                inputs=file_input,
                outputs=[
                    error_output,
                    overall_score,
                    naming_score,
                    modularity_score,
                    comments_score,
                    formatting_score,
                    reusability_score,
                    best_practices_score,
                    recommendations
                ],
                fn=on_analyze,
                cache_examples=True
            )
    
    return app
