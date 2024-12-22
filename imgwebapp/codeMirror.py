from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-code', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get('code', '')

    try:
        # Write code to a temporary file
        with open("temp.php", "w") as f:
            f.write(code)
        
        # Execute the PHP code
        result = subprocess.run(['php', 'temp.php'], capture_output=True, text=True, timeout=5)
        output = result.stdout or result.stderr
        
        
        
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
