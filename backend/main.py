from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
import shutil
from typing import Dict, List, Union
import re

app = FastAPI(title="Code Analyzer API")

# Add CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supported file extensions
SUPPORTED_EXTENSIONS = {".js", ".jsx", ".py"}

@app.get("/")
async def root():
    return {"message": "Code Analyzer API is running"}

@app.post("/analyze-code")
async def analyze_code(file: UploadFile = File(...)) -> Dict:
    """
    Analyze a code file and return a score with recommendations.
    
    Accepts .js, .jsx, or .py files.
    """
    # Check if file extension is supported
    filename = file.filename
    file_extension = os.path.splitext(filename)[1].lower()
    
    if file_extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type. Supported types: {', '.join(SUPPORTED_EXTENSIONS)}"
        )
    
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name
    
    try:
        # Read file content
        with open(temp_file_path, "r", encoding="utf-8") as f:
            code_content = f.read()
        
        # Analyze the code based on file type
        if file_extension in [".js", ".jsx"]:
            analysis_result = analyze_javascript_code(code_content)
        elif file_extension == ".py":
            analysis_result = analyze_python_code(code_content)
        
        return analysis_result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing code: {str(e)}")
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def analyze_javascript_code(code_content: str) -> Dict:
    """Analyze JavaScript/JSX code and return scores and recommendations."""
    # Initialize scores
    naming_score = analyze_js_naming_conventions(code_content)
    modularity_score = analyze_js_modularity(code_content)
    comments_score = analyze_comments(code_content)
    formatting_score = analyze_formatting(code_content)
    reusability_score = analyze_js_reusability(code_content)
    best_practices_score = analyze_js_best_practices(code_content)
    
    # Calculate overall score
    overall_score = (
        naming_score + 
        modularity_score + 
        comments_score + 
        formatting_score + 
        reusability_score + 
        best_practices_score
    )
    
    # Generate recommendations
    recommendations = generate_js_recommendations(
        code_content, 
        naming_score, 
        modularity_score,
        comments_score,
        formatting_score,
        reusability_score,
        best_practices_score
    )
    
    return {
        "overall_score": overall_score,
        "breakdown": {
            "naming": naming_score,
            "modularity": modularity_score,
            "comments": comments_score,
            "formatting": formatting_score,
            "reusability": reusability_score,
            "best_practices": best_practices_score
        },
        "recommendations": recommendations
    }

def analyze_python_code(code_content: str) -> Dict:
    """Analyze Python code and return scores and recommendations."""
    # Initialize scores
    naming_score = analyze_py_naming_conventions(code_content)
    modularity_score = analyze_py_modularity(code_content)
    comments_score = analyze_comments(code_content)
    formatting_score = analyze_formatting(code_content)
    reusability_score = analyze_py_reusability(code_content)
    best_practices_score = analyze_py_best_practices(code_content)
    
    # Calculate overall score
    overall_score = (
        naming_score + 
        modularity_score + 
        comments_score + 
        formatting_score + 
        reusability_score + 
        best_practices_score
    )
    
    # Generate recommendations
    recommendations = generate_py_recommendations(
        code_content, 
        naming_score, 
        modularity_score,
        comments_score,
        formatting_score,
        reusability_score,
        best_practices_score
    )
    
    return {
        "overall_score": overall_score,
        "breakdown": {
            "naming": naming_score,
            "modularity": modularity_score,
            "comments": comments_score,
            "formatting": formatting_score,
            "reusability": reusability_score,
            "best_practices": best_practices_score
        },
        "recommendations": recommendations
    }

# Analysis functions for JavaScript/JSX
def analyze_js_naming_conventions(code_content: str) -> int:
    """Analyze naming conventions in JavaScript/JSX code. Max score: 10."""
    score = 10
    
    # Check for camelCase variables (standard JS convention)
    non_camel_case_vars = re.findall(r'(?:let|const|var)\s+([A-Z][a-zA-Z0-9]*|[a-z]+_[a-zA-Z0-9_]*)\s*=', code_content)
    if non_camel_case_vars:
        score -= min(3, len(non_camel_case_vars))
    
    # Check for PascalCase components (React convention)
    if ".jsx" in code_content or "React" in code_content:
        non_pascal_case_components = re.findall(r'function\s+([a-z][a-zA-Z0-9]*)\s*\(\s*(?:props|{)', code_content)
        if non_pascal_case_components:
            score -= min(3, len(non_pascal_case_components))
    
    # Check for ALL_CAPS constants
    non_caps_constants = re.findall(r'const\s+([a-z][a-zA-Z0-9]*)\s*=\s*["\'\d\[]', code_content)
    if non_caps_constants:
        score -= min(2, len(non_caps_constants))
    
    # Check for consistent naming
    mixed_styles = re.findall(r'(?:let|const|var)\s+([a-z][a-zA-Z0-9]*_[a-zA-Z0-9]*|[a-z][a-zA-Z0-9]*-[a-zA-Z0-9]*)', code_content)
    if mixed_styles:
        score -= min(2, len(mixed_styles))
    
    return max(0, score)

def analyze_js_modularity(code_content: str) -> int:
    """Analyze function length and modularity in JavaScript/JSX code. Max score: 20."""
    score = 20
    
    # Find all function definitions
    function_matches = re.finditer(r'(?:function\s+\w+\s*\(.*?\)\s*{|const\s+\w+\s*=\s*(?:\(.*?\)|.*?)\s*=>\s*{|\(\s*\)\s*=>\s*{)', code_content)
    
    # Extract function bodies and count lines
    long_functions = 0
    very_long_functions = 0
    extremely_long_functions = 0
    
    for match in function_matches:
        start_pos = match.end()
        # Find matching closing brace
        brace_count = 1
        end_pos = start_pos
        
        for i in range(start_pos, len(code_content)):
            if code_content[i] == '{':
                brace_count += 1
            elif code_content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_pos = i
                    break
        
        if end_pos > start_pos:
            function_body = code_content[start_pos:end_pos]
            line_count = function_body.count('\n') + 1
            
            if line_count > 50:
                extremely_long_functions += 1
            elif line_count > 30:
                very_long_functions += 1
            elif line_count > 15:
                long_functions += 1
    
    # Deduct points based on function length
    score -= min(10, long_functions * 2)
    score -= min(15, very_long_functions * 3)
    score -= min(20, extremely_long_functions * 5)
    
    # Check for nested callbacks (callback hell)
    nested_callbacks = 0
    callback_depth = code_content.count('=>') - code_content.count('=>{')
    if callback_depth > 3:
        nested_callbacks = callback_depth - 3
    
    score -= min(5, nested_callbacks)
    
    # Check for component nesting (React)
    if ".jsx" in code_content or "React" in code_content:
        component_nesting = code_content.count('<') - code_content.count('</')
        if component_nesting > 10:
            score -= min(5, (component_nesting - 10) // 2)
    
    return max(0, score)

def analyze_js_reusability(code_content: str) -> int:
    """Analyze reusability and DRY principles in JavaScript/JSX code. Max score: 15."""
    score = 15
    
    # Check for repeated code blocks
    lines = code_content.split('\n')
    code_blocks = {}
    
    for i in range(len(lines)):
        for j in range(i+3, min(i+20, len(lines))):
            block = '\n'.join(lines[i:j])
            if len(block) > 50:  # Only consider substantial blocks
                if block in code_blocks:
                    code_blocks[block] += 1
                else:
                    code_blocks[block] = 1
    
    repeated_blocks = sum(1 for count in code_blocks.values() if count > 1)
    score -= min(10, repeated_blocks * 2)
    
    # Check for utility functions or hooks (positive)
    utility_functions = len(re.findall(r'(?:export\s+)?(?:function|const)\s+(?:use[A-Z]|format|convert|transform|calculate|get|is|has)', code_content))
    if utility_functions < 2:
        score -= 3
    
    # Check for hardcoded values that should be constants
    hardcoded_values = len(re.findall(r'[^A-Za-z0-9_](?:\d{3,}|"[^"]{10,}"|\'[^\']{10,}\')', code_content))
    score -= min(5, hardcoded_values)
    
    return max(0, score)

def analyze_js_best_practices(code_content: str) -> int:
    """Analyze web development best practices in JavaScript/JSX code. Max score: 20."""
    score = 20
    
    # Check for use of modern JS features
    if not re.search(r'(?:const|let|=>|async|await|\.map\(|\.filter\(|\.reduce\()', code_content):
        score -= 5
    
    # Check for potential memory leaks in React
    if ".jsx" in code_content or "React" in code_content:
        if re.search(r'useEffect\([^,]+\)', code_content):
            score -= 3  # Missing dependency array
        
        if re.search(r'addEventListener\(', code_content) and not re.search(r'removeEventListener\(', code_content):
            score -= 3  # Event listener without cleanup
    
    # Check for error handling
    if not re.search(r'try\s*{', code_content) and re.search(r'(?:fetch|axios|\.then\()', code_content):
        score -= 4  # Missing error handling for async operations
    
    # Check for accessibility issues in React
    if ".jsx" in code_content or "React" in code_content:
        if re.search(r'<(?:img|input|button)', code_content) and not re.search(r'(?:alt|aria-|role)', code_content):
            score -= 3  # Missing accessibility attributes
    
    # Check for potential security issues
    if re.search(r'(?:innerHTML|dangerouslySetInnerHTML|eval\()', code_content):
        score -= 5  # Potential XSS vulnerabilities
    
    return max(0, score)

# Analysis functions for Python
def analyze_py_naming_conventions(code_content: str) -> int:
    """Analyze naming conventions in Python code. Max score: 10."""
    score = 10
    
    # Check for snake_case variables (PEP8)
    non_snake_case_vars = re.findall(r'(?:^|\s)([a-z][a-z0-9]*[A-Z][a-zA-Z0-9]*)\s*=', code_content)
    if non_snake_case_vars:
        score -= min(3, len(non_snake_case_vars))
    
    # Check for UPPER_CASE constants
    non_upper_constants = re.findall(r'(?:^|\s)([a-z][a-zA-Z0-9_]*)\s*=\s*(?:["\'0-9\[]|True|False|None)', code_content)
    if non_upper_constants and re.search(r'if\s+__name__\s*==\s*["\']__main__["\']', code_content):
        score -= min(2, len(non_upper_constants))
    
    # Check for CamelCase classes (PEP8)
    non_camel_case_classes = re.findall(r'class\s+([a-z][a-zA-Z0-9_]*)', code_content)
    if non_camel_case_classes:
        score -= min(3, len(non_camel_case_classes))
    
    # Check for consistent naming
    mixed_styles = re.findall(r'(?:^|\s)([a-z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*_[a-zA-Z0-9_]*)', code_content)
    if mixed_styles:
        score -= min(2, len(mixed_styles))
    
    return max(0, score)

def analyze_py_modularity(code_content: str) -> int:
    """Analyze function length and modularity in Python code. Max score: 20."""
    score = 20
    
    # Find all function and method definitions
    function_matches = re.finditer(r'(?:^|\s)def\s+[a-zA-Z0-9_]+\s*\(', code_content, re.MULTILINE)
    
    # Extract function bodies and count lines
    long_functions = 0
    very_long_functions = 0
    extremely_long_functions = 0
    
    for match in function_matches:
        start_line = code_content[:match.start()].count('\n')
        lines = code_content.split('\n')
        
        # Find the end of the function by indentation
        end_line = start_line + 1
        while end_line < len(lines):
            # Skip empty lines or comments
            if not lines[end_line].strip() or lines[end_line].strip().startswith('#'):
                end_line += 1
                continue
                
            # Check if this line has less indentation than the function definition
            if not re.match(r'\s+', lines[end_line]):
                break
                
            end_line += 1
        
        function_length = end_line - start_line
        
        if function_length > 50:
            extremely_long_functions += 1
        elif function_length > 30:
            very_long_functions += 1
        elif function_length > 15:
            long_functions += 1
    
    # Deduct points based on function length
    score -= min(10, long_functions * 2)
    score -= min(15, very_long_functions * 3)
    score -= min(20, extremely_long_functions * 5)
    
    # Check for nested loops and conditionals
    nested_depth = 0
    lines = code_content.split('\n')
    for line in lines:
        indent_level = len(line) - len(line.lstrip())
        if indent_level > nested_depth:
            nested_depth = indent_level
    
    if nested_depth > 16:  # More than 4 levels of nesting (assuming 4 spaces per level)
        score -= min(5, (nested_depth - 16) // 4)
    
    return max(0, score)

def analyze_py_reusability(code_content: str) -> int:
    """Analyze reusability and DRY principles in Python code. Max score: 15."""
    score = 15
    
    # Check for repeated code blocks
    lines = code_content.split('\n')
    code_blocks = {}
    
    for i in range(len(lines)):
        for j in range(i+3, min(i+20, len(lines))):
            block = '\n'.join(lines[i:j])
            if len(block) > 50:  # Only consider substantial blocks
                if block in code_blocks:
                    code_blocks[block] += 1
                else:
                    code_blocks[block] = 1
    
    repeated_blocks = sum(1 for count in code_blocks.values() if count > 1)
    score -= min(10, repeated_blocks * 2)
    
    # Check for utility functions (positive)
    utility_functions = len(re.findall(r'def\s+(?:format|convert|transform|calculate|get|is|has|validate)', code_content))
    if utility_functions < 2:
        score -= 3
    
    # Check for hardcoded values that should be constants
    hardcoded_values = len(re.findall(r'[^A-Za-z0-9_](?:\d{3,}|"[^"]{10,}"|\'[^\']{10,}\')', code_content))
    score -= min(5, hardcoded_values)
    
    return max(0, score)

def analyze_py_best_practices(code_content: str) -> int:
    """Analyze web development best practices in Python code. Max score: 20."""
    score = 20
    
    # Check for FastAPI best practices
    if "fastapi" in code_content:
        # Check for type hints
        if not re.search(r'def\s+\w+\([^)]*:\s*\w+', code_content) and not re.search(r'def\s+\w+\([^)]*\)\s*->\s*\w+', code_content):
            score -= 4  # Missing type hints
        
        # Check for proper response models
        if not re.search(r'(?:response_model|BaseModel)', code_content):
            score -= 3  # Missing response models
        
        # Check for proper error handling
        if not re.search(r'(?:HTTPException|status\.)', code_content):
            score -= 3  # Missing error handling
    
    # Check for error handling
    if not re.search(r'try\s*:', code_content) and re.search(r'(?:requests\.|open\(|json\.)', code_content):
        score -= 4  # Missing error handling for I/O operations
    
    # Check for docstrings
    if not re.search(r'"""', code_content):
        score -= 3  # Missing docstrings
    
    # Check for potential security issues
    if re.search(r'(?:eval\(|exec\(|subprocess\.)', code_content):
        score -= 5  # Potential security vulnerabilities
    
    # Check for use of context managers
    if re.search(r'open\(', code_content) and not re.search(r'with\s+open\(', code_content):
        score -= 3  # Not using context managers for file operations
    
    return max(0, score)

# Common analysis functions
def analyze_comments(code_content: str) -> int:
    """Analyze comments and documentation. Max score: 20."""
    score = 20
    lines = code_content.split('\n')
    total_lines = len(lines)
    
    # Count comment lines
    comment_lines = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('#') or stripped.startswith('/*') or stripped.startswith('*'):
            comment_lines += 1
    
    # Calculate comment ratio
    comment_ratio = comment_lines / total_lines if total_lines > 0 else 0
    
    # Ideal comment ratio is around 15-25%
    if comment_ratio < 0.05:
        score -= 15  # Almost no comments
    elif comment_ratio < 0.1:
        score -= 10  # Very few comments
    elif comment_ratio < 0.15:
        score -= 5   # Few comments
    elif comment_ratio > 0.4:
        score -= 5   # Too many comments
    
    # Check for function/class documentation
    if '.py' in code_content:
        # Check for docstrings in Python
        docstring_count = code_content.count('"""') // 2  # Each docstring has opening and closing quotes
        function_count = len(re.findall(r'def\s+', code_content))
        class_count = len(re.findall(r'class\s+', code_content))
        
        if function_count + class_count > 0:
            docstring_ratio = docstring_count / (function_count + class_count)
            if docstring_ratio < 0.5:
                score -= 10  # Less than half of functions/classes have docstrings
            elif docstring_ratio < 0.8:
                score -= 5   # Most but not all functions/classes have docstrings
    else:
        # Check for JSDoc in JavaScript
        jsdoc_count = len(re.findall(r'/\*\*[\s\S]*?\*/', code_content))
        function_count = len(re.findall(r'function\s+|const\s+\w+\s*=\s*(?:function|\(.*?\)\s*=>)', code_content))
        
        if function_count > 0:
            jsdoc_ratio = jsdoc_count / function_count
            if jsdoc_ratio < 0.3:
                score -= 10  # Less than 30% of functions have JSDoc
            elif jsdoc_ratio < 0.6:
                score -= 5   # Less than 60% of functions have JSDoc
    
    return max(0, score)

def analyze_formatting(code_content: str) -> int:
    """Analyze code formatting and indentation. Max score: 15."""
    score = 15
    lines = code_content.split('\n')
    
    # Check for consistent indentation
    indentation_types = set()
    for line in lines:
        if line.strip() and line[0].isspace():
            # Check if indentation uses spaces or tabs
            if line[0] == '\t':
                indentation_types.add('tab')
            else:
                # Count leading spaces
                spaces = len(line) - len(line.lstrip(' '))
                if spaces % 2 == 0 and spaces % 4 != 0:
                    indentation_types.add('2spaces')
                elif spaces % 4 == 0:
                    indentation_types.add('4spaces')
                else:
                    indentation_types.add('other')
    
    # Deduct points for mixed indentation
    if len(indentation_types) > 1:
        score -= 8  # Mixed indentation styles
    
    # Check for lines that are too long (>100 characters)
    long_lines = sum(1 for line in lines if len(line) > 100)
    score -= min(5, long_lines // 3)
    
    # Check for consistent spacing around operators
    inconsistent_spacing = 0
    for pattern in [r'=', r'\+', r'-', r'\*', r'/', r'==', r'!=', r'>=', r'<=']:
        no_space_count = len(re.findall(r'[a-zA-Z0-9]' + pattern + r'[a-zA-Z0-9]', code_content))
        one_side_space_count = len(re.findall(r'[a-zA-Z0-9]\s+' + pattern + r'[a-zA-Z0-9]|[a-zA-Z0-9]' + pattern + r'\s+[a-zA-Z0-9]', code_content))
        if no_space_count > 0 and one_side_space_count > 0:
            inconsistent_spacing += 1
    
    score -= min(5, inconsistent_spacing)
    
    # Check for trailing whitespace
    trailing_whitespace = sum(1 for line in lines if line.rstrip() != line)
    score -= min(3, trailing_whitespace // 5)
    
    return max(0, score)

# Recommendation generators
def generate_js_recommendations(code_content: str, naming_score: int, modularity_score: int, 
                               comments_score: int, formatting_score: int, reusability_score: int, 
                               best_practices_score: int) -> List[str]:
    """Generate recommendations for JavaScript/JSX code."""
    recommendations = []
    
    # Naming conventions recommendations
    if naming_score < 8:
        if re.search(r'(?:let|const|var)\s+([A-Z][a-zA-Z0-9]*|[a-z]+_[a-zA-Z0-9_]*)\s*=', code_content):
            recommendations.append("Use camelCase for variable names (e.g., 'totalAmount' instead of 'Total_Amount' or 'TotalAmount').")
        
        if ".jsx" in code_content or "React" in code_content:
            if re.search(r'function\s+([a-z][a-zA-Z0-9]*)\s*\(\s*(?:props|{)', code_content):
                recommendations.append("Use PascalCase for React component names (e.g., 'UserProfile' instead of 'userProfile').")
    
    # Modularity recommendations
    if modularity_score < 15:
        function_matches = re.finditer(r'(?:function\s+\w+\s*\(.*?\)\s*{|const\s+\w+\s*=\s*(?:\(.*?\)|.*?)\s*=>\s*{|\(\s*\)\s*=>\s*{)', code_content)
        for match in function_matches:
            start_pos = match.end()
            # Find matching closing brace
            brace_count = 1
            end_pos = start_pos
            
            for i in range(start_pos, len(code_content)):
                if code_content[i] == '{':
                    brace_count += 1
                elif code_content[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_pos = i
                        break
            
            if end_pos > start_pos:
                function_body = code_content[start_pos:end_pos]
                line_count = function_body.count('\n') + 1
                
                if line_count > 30:
                    function_name = re.search(r'(?:function\s+(\w+)|const\s+(\w+)\s*=)', code_content[match.start():match.end()])
                    if function_name:
                        name = function_name.group(1) or function_name.group(2)
                        recommendations.append(f"Function '{name}' is too long ({line_count} lines). Consider breaking it into smaller functions.")
                        break
    
    # Comments recommendations
    if comments_score < 15:
        recommendations.append("Add more descriptive comments to explain complex logic and the purpose of functions.")
    
    # Formatting recommendations
    if formatting_score < 10:
        recommendations.append("Ensure consistent indentation and spacing throughout the code.")
    
    # Reusability recommendations
    if reusability_score < 10:
        if len(re.findall(r'[^A-Za-z0-9_](?:\d{3,}|"[^"]{10,}"|\'[^\']{10,}\')', code_content)) > 2:
            recommendations.append("Extract magic numbers and strings into named constants for better maintainability.")
    
    # Best practices recommendations
    if best_practices_score < 15:
        if ".jsx" in code_content or "React" in code_content:
            if re.search(r'useEffect\([^,]+\)', code_content):
                recommendations.append("Add dependency arrays to useEffect hooks to prevent unnecessary re-renders.")
            
            if re.search(r'<(?:img|input|button)', code_content) and not re.search(r'(?:alt|aria-|role)', code_content):
                recommendations.append("Add accessibility attributes (alt, aria-* attributes, role) to improve accessibility.")
        
        if re.search(r'(?:innerHTML|dangerouslySetInnerHTML|eval\()', code_content):
            recommendations.append("Avoid using innerHTML, dangerouslySetInnerHTML, or eval() to prevent security vulnerabilities.")
    
    # Limit to 3-5 recommendations
    if len(recommendations) < 3:
        # Add general recommendations if we don't have enough specific ones
        general_recommendations = [
            "Consider using ESLint to enforce code style and catch potential issues.",
            "Implement unit tests to ensure code reliability.",
            "Use TypeScript for better type safety and developer experience."
        ]
        recommendations.extend(general_recommendations[:3 - len(recommendations)])
    
    return recommendations[:5]

def generate_py_recommendations(code_content: str, naming_score: int, modularity_score: int, 
                               comments_score: int, formatting_score: int, reusability_score: int, 
                               best_practices_score: int) -> List[str]:
    """Generate recommendations for Python code."""
    recommendations = []
    
    # Naming conventions recommendations
    if naming_score < 8:
        if re.search(r'(?:^|\s)([a-z][a-z0-9]*[A-Z][a-zA-Z0-9]*)\s*=', code_content):
            recommendations.append("Use snake_case for variable and function names (e.g., 'total_amount' instead of 'totalAmount').")
        
        if re.search(r'class\s+([a-z][a-zA-Z0-9_]*)', code_content):
            recommendations.append("Use PascalCase for class names (e.g., 'UserProfile' instead of 'user_profile').")
    
    # Modularity recommendations
    if modularity_score < 15:
        function_matches = re.finditer(r'(?:^|\s)def\s+([a-zA-Z0-9_]+)\s*\(', code_content, re.MULTILINE)
        for match in function_matches:
            function_name = match.group(1)
            start_line = code_content[:match.start()].count('\n')
            lines = code_content.split('\n')
            
            # Find the end of the function by indentation
            end_line = start_line + 1
            while end_line < len(lines):
                # Skip empty lines or comments
                if not lines[end_line].strip() or lines[end_line].strip().startswith('#'):
                    end_line += 1
                    continue
                    
                # Check if this line has less indentation than the function definition
                if not re.match(r'\s+', lines[end_line]):
                    break
                    
                end_line += 1
            
            function_length = end_line - start_line
            
            if function_length > 30:
                recommendations.append(f"Function '{function_name}' is too long ({function_length} lines). Consider breaking it into smaller functions.")
                break
    
    # Comments recommendations
    if comments_score < 15:
        if not re.search(r'"""', code_content):
            recommendations.append("Add docstrings to functions and classes to document their purpose and parameters.")
        else:
            recommendations.append("Add more inline comments to explain complex logic and implementation details.")
    
    # Formatting recommendations
    if formatting_score < 10:
        indentation_types = set()
        lines = code_content.split('\n')
        for line in lines:
            if line.strip() and line[0].isspace():
                if line[0] == '\t':
                    indentation_types.add('tab')
                else:
                    spaces = len(line) - len(line.lstrip(' '))
                    if spaces % 2 == 0 and spaces % 4 != 0:
                        indentation_types.add('2spaces')
                    elif spaces % 4 == 0:
                        indentation_types.add('4spaces')
                    else:
                        indentation_types.add('other')
        
        if len(indentation_types) > 1:
            recommendations.append("Use consistent indentation (PEP 8 recommends 4 spaces per indentation level).")
    
    # Reusability recommendations
    if reusability_score < 10:
        if len(re.findall(r'[^A-Za-z0-9_](?:\d{3,}|"[^"]{10,}"|\'[^\']{10,}\')', code_content)) > 2:
            recommendations.append("Extract magic numbers and strings into named constants for better maintainability.")
    
    # Best practices recommendations
    if best_practices_score < 15:
        if "fastapi" in code_content:
            if not re.search(r'def\s+\w+\([^)]*:\s*\w+', code_content) and not re.search(r'def\s+\w+\([^)]*\)\s*->\s*\w+', code_content):
                recommendations.append("Add type hints to function parameters and return values for better code clarity.")
            
            if not re.search(r'(?:HTTPException|status\.)', code_content):
                recommendations.append("Implement proper error handling with HTTPException and status codes.")
        
        if re.search(r'open\(', code_content) and not re.search(r'with\s+open\(', code_content):
            recommendations.append("Use context managers (with statement) for file operations to ensure proper resource cleanup.")
    
    # Limit to 3-5 recommendations
    if len(recommendations) < 3:
        # Add general recommendations if we don't have enough specific ones
        general_recommendations = [
            "Consider using a linter like flake8 or pylint to enforce code style and catch potential issues.",
            "Implement unit tests to ensure code reliability.",
            "Use virtual environments to manage dependencies."
        ]
        recommendations.extend(general_recommendations[:3 - len(recommendations)])
    
    return recommendations[:5]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
