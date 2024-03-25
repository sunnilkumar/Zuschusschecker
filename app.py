from flask import Flask, render_template
from flask import Flask, request, jsonify
import json
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USERNAME'] = 'colin@thinkvoltaic.de' 
app.config['MAIL_PASSWORD'] = 'stotxdvjnjvgegor' 
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'colin@thinkvoltaic.de'

mail = Mail(app)


@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/formular')
def formular():
    return render_template('form.html')

@app.route('/preise')
def price():
    return render_template('price.html')

@app.route('/leistungen')
def feauture():
    return render_template('features.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.data
    final_data = json.loads(data.decode('utf-8'))
    firstName = final_data['firstName']
    lastName = final_data['lastName']
    street = final_data['street']
    postalcode = final_data['postalCode']
    city = final_data['city']
    email = final_data['email']
    phone = final_data['phone']
    userquestionanswer = final_data['useranswers']

    self_subject = 'New Submission: User Details'
    self_body = f"Dear Team,\n\nA new submission has been received from a user. Here are the details:\n\nName: {firstName} {lastName}\nEmail: {email}\nPostal Code: {postalcode}\nCity: {city}\nTelefon: {phone}\nAddress: {street}\n\nUser's Answers:\n"
    
    for question_answer in userquestionanswer:
        self_body += f"\nQuestion: {question_answer['question']}\nAnswer: {question_answer['answer']}\n"

    self_body += "\nPlease review the information and take necessary action.\n\nBest regards,\nZuschusschecker"

    msg = Message(self_subject, recipients=["colin@thinkvoltaic.de"], body=self_body)
    mail.send(msg)

    user_subject = 'Anfrage Bestätigung Zuschusschecker'
    user_body = f"Sehr geehrte/r {firstName} {lastName},\n\nVielen Dank für Ihre Anfrage. Wir haben all Ihrer Informationen erhalten. Wir melden uns zeitnah mit einer Förderberatung.\n\nMit freundlichen Grüßen,\nZuschusschecker"
    msg = Message(user_subject,recipients=[email],body= user_body)
    mail.send(msg)
    
    return jsonify({'message': 'Form submitted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
