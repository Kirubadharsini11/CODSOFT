from flask import Flask, render_template, request, jsonify
from calculator import Calculator
import os

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), '../frontend/templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '../frontend/static'))

calc = Calculator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    try:
        num1 = float(data['num1'])
        num2 = float(data['num2'])
        operation = data['operation']

        if operation == '+':
            result = calc.add(num1, num2)
        elif operation == '-':
            result = calc.subtract(num1, num2)
        elif operation == '*':
            result = calc.multiply(num1, num2)
        elif operation == '/':
            result = calc.divide(num1, num2)
        else:
            return jsonify({"error": "Invalid operation!"}), 400

        return jsonify({"result": result})

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)