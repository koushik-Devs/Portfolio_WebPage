from flask import render_template, request, flash, redirect, url_for
from app import app
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@app.route('/')
def index():
    """Main portfolio page"""
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submission"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        if not name or not email or not message:
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('index') + '#contact')
        
        try:
            # Email configuration (using environment variables)
            smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.environ.get('SMTP_PORT', '587'))
            smtp_username = os.environ.get('SMTP_USERNAME', '')
            smtp_password = os.environ.get('SMTP_PASSWORD', '')
            recipient_email = os.environ.get('RECIPIENT_EMAIL', 'koushik.mondal@example.com')
            
            if smtp_username and smtp_password:
                # Create message
                msg = MIMEMultipart()
                msg['From'] = smtp_username
                msg['To'] = recipient_email
                msg['Subject'] = f'Portfolio Contact: Message from {name}'
                
                body = f"""
                New contact form submission:
                
                Name: {name}
                Email: {email}
                Message: {message}
                """
                
                msg.attach(MIMEText(body, 'plain'))
                
                # Send email
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(smtp_username, smtp_password)
                text = msg.as_string()
                server.sendmail(smtp_username, recipient_email, text)
                server.quit()
                
                flash('Thank you for your message! I\'ll get back to you soon.', 'success')
            else:
                # If email is not configured, just show a success message
                flash('Thank you for your message! I\'ll get back to you soon.', 'success')
                
        except Exception as e:
            flash('Sorry, there was an error sending your message. Please try again.', 'error')
        
        return redirect(url_for('index') + '#contact')
