import os
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import pandas as pd
import pdfplumber
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'toni-secret-key'
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        filetype = request.form['filetype']
        location = request.form.get('location', '').strip()
        if not file:
            flash('No file selected!')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        result_file = None
        base_name, ext = os.path.splitext(filename)
        if filetype == 'pdf':
            # PDF extraction logic (Script 1)
            all_text = ""
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    all_text += page.extract_text() + "\n"
            def extract_year(text):
                m = re.search(r'(\d{4})(?:\s*-\s*\d{4})?', text)
                return m.group(1) if m else ""
            def extract_people(line):
                line = re.sub(r'\b[a-zA-Z]\.\s*', '', line)
                surnames = re.findall(r'\b([A-Z]{2,}(?: [A-Z]{2,})*)\b', line)
                people = []
                for surname in surnames:
                    parts = line.split(surname)
                    if len(parts) > 0:
                        before = parts[0].strip().split()
                        firstname = ""
                        for word in reversed(before):
                            if not word.isupper() and word.isalpha():
                                firstname = word
                                break
                        if not firstname:
                            after = parts[1].strip().split() if len(parts) > 1 else []
                            for word in after:
                                if word and not word.isupper() and word.isalpha():
                                    firstname = word
                                    break
                        firstname = firstname.replace('/', '').strip()
                        people.append((surname.strip(), firstname.strip()))
                return people
            records = []
            for line in all_text.splitlines():
                if not line.strip():
                    continue
                year = extract_year(line)
                people = extract_people(line)
                for surname, firstname in people:
                    records.append({
                        "Surname": surname,
                        "Firstname": firstname,
                        "Record Type": "t",
                        "Date": year,
                        "Location": location if location else "PDF Upload"
                    })
            df = pd.DataFrame(records)
            result_file = os.path.join(UPLOAD_FOLDER, f'{base_name}.xlsx')
            df.to_excel(result_file, index=False)
        elif filetype == 'excel':
            # Excel deduplication logic (Script 2)
            df = pd.read_excel(filepath)
            df_no_dupes = df.drop_duplicates()
            result_file = os.path.join(UPLOAD_FOLDER, f'{base_name}_deduped.xlsx')
            df_no_dupes.to_excel(result_file, index=False)
        return send_file(result_file, as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) 