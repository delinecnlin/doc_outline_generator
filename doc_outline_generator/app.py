## app.py
from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
from utils.file_processor import FileProcessor
from utils.ai_model import AIModel
from utils.doc_generator import DocGenerator
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['ALLOWED_EXTENSIONS'] = {'docx', 'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return file_path, 200

@app.route('/generate', methods=['POST'])
def generate_outline():
    file_path = request.json.get('file_path')
    project_info = request.json.get('project_info')
    if not file_path or not project_info:
        return 'Missing file_path or project_info', 400
    file_processor = FileProcessor(file_path)
    template_text = file_processor.process_file()
    ai_model = AIModel(template_text)
    outline = ai_model.generate_outline()
    doc_generator = DocGenerator(outline, project_info)
    doc_path = doc_generator.generate_doc()
    return doc_path, 200

@app.route('/preview', methods=['GET'])
def preview_doc():
    doc_path = request.args.get('doc_path')
    if not doc_path:
        return 'Missing doc_path', 400
    return send_file(doc_path)

if __name__ == '__main__':
    app.run(debug=True)
