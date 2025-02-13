from flask import Flask, request, jsonify, render_template, url_for
from flask_mail import Mail, Message
import re

app = Flask(__name__)

# Configure Mail Server (Use your SMTP details)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'subhash7483558714@gmail.com'
app.config['MAIL_PASSWORD'] = 'nqxo igkt tewp utvv'
app.config['MAIL_DEFAULT_SENDER'] = 'subhash7483558714@gmail.com'

mail = Mail(app)

# Store submitted data (temporary dictionary)
stored_data = {}

@app.route('/')
def home():
    return render_template('submit.html')

@app.route('/submit', methods=['POST'])
def submit_request():
    global stored_data
    data = request.json
    stored_data = data  

    email_body = "A new regression request has been submitted.\n\n"
    for key, value in stored_data.items():
        email_body += f"{key}: {value}\n"
    
    compare_url = url_for('compare_page', _external=True)
    email_body += f"\nClick the link below to compare input values:\n{compare_url}"
    
    recipient = "subhash7483558714@gmail.com"
    msg = Message("Regression Request Submitted", recipients=[recipient])
    msg.body = email_body
    mail.send(msg)
    
    return jsonify({"message": "Request submitted! Email sent with comparison link."})

@app.route('/compare', methods=['POST', 'GET'])
def compare_page():
    if request.method == 'POST':
        input_text = request.json.get('inputData', '')

        # Parse input in the format "--key=value"
        pattern = r'--([\w\d_-]+)=(?:(?:"([^"]+)")|(\S+))'
        matches = re.findall(pattern, input_text)
    
        input_dict = {key: (val1 if val1 else val2) for key, val1, val2 in matches}

        mismatches = []
        for key, stored_value in stored_data.items():
            if key in input_dict and input_dict[key] != stored_value:
                mismatches.append({"key": key, "stored_value": stored_value, "input_value": input_dict[key]})

        if mismatches:
            mismatch_table = '<table border="1" cellpadding="5" cellspacing="0">'
            mismatch_table += '<tr><th>Field</th><th>Stored Value</th><th>Input Value</th></tr>'

            for mismatch in mismatches:
                mismatch_table += f"""
                    <tr>
                        <td>{mismatch['key']}</td>
                        <td>{mismatch['stored_value']}</td>
                        <td>{mismatch['input_value']}</td>
                    </tr>
                """
            mismatch_table += '</table>'

            recipient = "subhash7483558714@gmail.com"
            msg = Message("Mismatch in Regression Data", recipients=[recipient])
            msg.html = f"<p>Mismatches found:</p>{mismatch_table}"
            mail.send(msg)

            return jsonify({"result": "Mismatches found and email sent!"})

        return jsonify({"result": "No mismatches found!"})

    return render_template('compare.html', stored_data=stored_data)

if __name__ == '__main__':
    app.run(debug=True)
