from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
from werkzeug.utils import secure_filename
from hashlib import sha256
import os
import secrets # For generating a strong secret key

app = Flask(__name__)

# --- Cấu hình quan trọng ---
app.secret_key = secrets.token_hex(24) # Sử dụng 24 bytes cho độ an toàn cao hơn

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

users = {
    'alicu': '1234',
    'bob': '5678'
}

# --- Routes của ứng dụng Flask ---

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password are required'}), 400

    if username in users and users[username] == password:
        session['user'] = username # Lưu tên người dùng vào session
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None) # Xóa 'user' khỏi session
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/upload', methods=['POST'])
def upload():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    recipient = request.form.get('recipient')
    if not recipient:
        return jsonify({'error': 'Recipient username is required'}), 400

    if recipient not in users:
        return jsonify({'error': 'Recipient does not exist'}), 400

    if file:
        filename = secure_filename(file.filename)
        user_folder = os.path.join(UPLOAD_FOLDER, recipient)
        os.makedirs(user_folder, exist_ok=True)
        filepath = os.path.join(user_folder, filename)
        file.save(filepath)

        with open(filepath, 'rb') as f:
            file_data = f.read()
        file_hash = sha256(file_data).hexdigest()
        
        return jsonify({'status': f'Upload OK. SHA-256: {file_hash}'})
    
    return jsonify({'error': 'File upload failed unexpectedly'}), 500

@app.route('/files')
def list_files():
    if 'user' not in session:
        return jsonify([])
    
    current_user_folder = os.path.join(UPLOAD_FOLDER, session['user'])
    
    if not os.path.exists(current_user_folder):
        return jsonify([])
    
    try:
        files = [f for f in os.listdir(current_user_folder) if os.path.isfile(os.path.join(current_user_folder, f))]
        return jsonify(files)
    except Exception as e:
        app.logger.error(f"Error listing files for user {session['user']}: {e}")
        return jsonify([]), 500

@app.route('/download/<filename>')
def download_file(filename):
    if 'user' not in session:
        return redirect(url_for('index'))

    current_user_folder = os.path.join(UPLOAD_FOLDER, session['user'])
    
    safe_filename = secure_filename(filename)
    filepath = os.path.join(current_user_folder, safe_filename)

    if not os.path.exists(filepath) or not os.path.isfile(filepath):
        return "File not found or access denied.", 404
    
    return send_from_directory(current_user_folder, safe_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)