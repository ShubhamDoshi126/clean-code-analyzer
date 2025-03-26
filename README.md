Hosted on 
https://huggingface.co/spaces/Shubham126/Clean-code-analyzer

# Code Analyzer for Hugging Face Spaces

A lightweight tool that analyzes React (JavaScript) or FastAPI (Python) code files and scores them on clean code practices, while also offering recommendations for improvement.

## Features

- Analyzes JavaScript (.js), React (.jsx), and Python (.py) files
- Scores code quality on a scale of 0-100
- Provides detailed breakdown of scores across 6 categories:
  - Naming conventions (10 points)
  - Function length and modularity (20 points)
  - Comments and documentation (20 points)
  - Formatting/indentation (15 points)
  - Reusability and DRY principles (15 points)
  - Best practices in web development (20 points)
- Offers 3-5 actionable recommendations for improving code quality
- Simple, intuitive Gradio interface
- Ready for Hugging Face Spaces deployment

- ## Project Structure

```
code-analyzer-huggingface/
├── app.py                 # Main entry point for Hugging Face Spaces
├── analyzer.py            # Code analysis logic
├── ui.py                  # Gradio UI implementation
├── requirements.txt       # Python dependencies
├── examples/              # Example files for testing
│   ├── example_react.jsx
│   ├── example_javascript.js
│   └── example_fastapi.py
└── README.md              # Documentation
```

## How It Works

The code analyzer evaluates code quality based on established best practices:

1. **Naming Conventions (10 points)**
   - JavaScript: camelCase for variables, PascalCase for components
   - Python: snake_case for variables/functions, PascalCase for classes

2. **Function Length and Modularity (20 points)**
   - Evaluates function length and complexity
   - Checks for nested callbacks and conditionals

3. **Comments and Documentation (20 points)**
   - Assesses comment ratio and quality
   - Checks for function/class documentation

4. **Formatting/Indentation (15 points)**
   - Evaluates consistent indentation
   - Checks for line length and spacing

5. **Reusability and DRY (15 points)**
   - Identifies repeated code blocks
   - Checks for hardcoded values

6. **Best Practices (20 points)**
   - JavaScript: modern features, error handling, accessibility
   - Python: type hints, error handling, context managers

## Customization

To add more analysis rules or modify existing ones:

1. Edit `analyzer.py` to add new analysis functions
2. Update the scoring weights in the main analysis functions
3. Add new recommendations in the recommendation generator functions

## License

MIT
