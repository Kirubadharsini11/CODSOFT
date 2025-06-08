from flask import Flask, render_template, request, jsonify
from password_generator import PasswordGenerator
import os

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), '../frontend/templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '../frontend/static'))
generator = PasswordGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    try:
        length = int(data.get('length', 12))
        if length < 8 or length > 64:
            return jsonify({"error": "Password length should be between 8 and 64"}), 400
        
        password = generator.generate_password(
            length=length,
            use_uppercase=data.get('uppercase', True),
            use_digits=data.get('digits', True),
            use_special=data.get('special', True)
        )
        
        return jsonify({
            "password": password,
            "strength": evaluate_strength(password)
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

def evaluate_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    score = 0
    # Length score
    if length >= 12: score += 3
    elif length >= 8: score += 2
    else: score += 1
    
    # Complexity score
    complexity = sum([has_upper, has_lower, has_digit, has_special])
    score += complexity
    
    # Evaluate strength
    if score >= 6: return "Very Strong"
    if score >= 4: return "Strong"
    if score >= 3: return "Moderate"
    return "Weak"

if __name__ == '__main__':
    app.run(debug=True, port=5001)