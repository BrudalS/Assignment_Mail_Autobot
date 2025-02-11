from flask import Flask, request, jsonify, render_template, url_for
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Configure Mail Server (Use your SMTP details)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Change to your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False  # Ensure this is False if using TLS
app.config['MAIL_USERNAME'] = 'subhash7483558714@gmail.com'  # Replace with sender email
app.config['MAIL_PASSWORD'] = 'nqxo igkt tewp utvv'  # Use App Password or real password
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
    stored_data = data  # Save data temporarily
    
    # Format the email body with variables and values
    email_body = "A new regression request has been submitted.\n\n"
    for key, value in stored_data.items():
        email_body += f"{key}: {value}\n"
    
    compare_url = url_for('compare_page', _external=True)  # Generate comparison page link
    email_body += f"\nClick the link below to compare input values:\n{compare_url}"
    
    # Send email
    recipient = "subhash7483558714@gmail.com"  # Replace with recipient email
    msg = Message("Regression Request Submitted", recipients=[recipient])
    msg.body = email_body
    mail.send(msg)
    
    return jsonify({"message": "Request submitted! Email sent with comparison link."})

@app.route('/compare', methods=['POST', 'GET'])
def compare_page():
    if request.method == 'POST':
        input_value = request.json.get('inputValue')
        
        # Store mismatches in a list
        mismatches = []
        for key, stored_value in stored_data.items():
            if stored_value != input_value:
                mismatches.append({"key": key, "stored_value": stored_value, "input_value": input_value})
        
        # If mismatches exist, format and send email
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

            recipient = "subhash7483558714@gmail.com"  # Replace with the desired recipient email
            msg = Message("Mismatch in Regression Data", recipients=[recipient])
            msg.html = f"""
            <p>A mismatch occurred in the comparison of regression data. Below are the mismatches:</p>
            {mismatch_table}
            """
            mail.send(msg)
        
        # Return the result to the frontend
        return jsonify({"result": "Mismatches found and email sent!"})
    
    return render_template('compare.html', stored_data=stored_data)

if __name__ == '__main__':
    app.run(debug=True)
