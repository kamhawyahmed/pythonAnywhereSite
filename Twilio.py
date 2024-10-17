#NEED TO VERIFY P# BEFORE CAN SEND BUT CAN STILL RECEIVE TEXTS
from twilio.rest import Client
from twilio.rest.api.v2010.account import message
# import OpenAI

# Twilio account credentials
import os
from dotenv import load_dotenv

load_dotenv(".env") #loads environ vars from .venv file (hidden on mac bc start with .)

account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")

# Twilio phone number to monitor for incoming messages
twilio_phone_number = os.environ.get("twilio_phone_number")
twilio_virtual_phone_number = "+18777804236"

# File path to log incoming messages
log_file_path = 'incoming_messages.log'


# Function to fetch and log incoming messages
def fetch_and_log_messages(twilio_phone_number=twilio_phone_number, log_file_path=log_file_path):
    client = Client(account_sid, auth_token)

    # Fetch all messages received by the Twilio phone number
    messages = client.messages.list(to=twilio_phone_number)

    # Log each message to a text file
    with open(log_file_path, 'a') as log_file:
        for message in messages:
            log_file.write(f"From: {message.from_}\n")
            log_file.write(f"To: {message.to}\n")
            log_file.write(f"Body: {message.body}\n")
            log_file.write(f"Date: {message.date_created}\n")
            log_file.write("-----------------------------\n")

    print(f"Messages logged to {log_file_path}")
    return

def fetch_messages_to_list(twilio_phone_number=twilio_phone_number):
    client = Client(account_sid, auth_token)
    messages = client.messages.list(to=twilio_phone_number, limit=50)
    messages_list = []
    auto_reply_message = "Thanks for the message. Configure your number's SMS URL to change this message.Reply HELP for help.Reply STOP to unsubscribe.Msg&Data rates may apply."
    for message in messages:
        if message.body != auto_reply_message:
            messages_list.append(message.body)
    return messages_list  

if __name__ == "__main__":
    print(fetch_messages_to_list())  


def send_message(message_content="This is the ship that made the Kessel Run in fourteen parsecs?", 
                 target_phone_number=twilio_virtual_phone_number):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message_content,
        from_=twilio_phone_number,
        to= target_phone_number,
    )
    return message.sid, message.body

prompt_start_old = """Given the following database schema and patient case, format the patient information into a structured text form based on the schema in under 1200 characters:

Database Schema:

sql
Copy code
CREATE DATABASE Hospital;
USE Hospital;

DROP TABLE IF EXISTS patients;

CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    firstName VARCHAR(255) NOT NULL,
    lastName VARCHAR(255) NOT NULL,
    phoneNumber VARCHAR(255) NOT NULL,
    secondaryPhoneNumber VARCHAR(255),
    email VARCHAR(255) NOT NULL,
    admissionDate DATETIME NOT NULL,
    dischargeDate DATETIME NOT NULL,
    contactDate DATE NOT NULL,
    admissionReason VARCHAR(1024) NOT NULL,
    proceduresPerformed VARCHAR(1024) NOT NULL,
    diagnosis VARCHAR(1024) NOT NULL,
    medicationsGiven VARCHAR(1024) NOT NULL,
    followupInstructions VARCHAR(1024) NOT NULL,
    authCode VARCHAR(255) NOT NULL,
    needsFollowUp BOOLEAN NOT NULL
);

Patient Case: 
"""

prompt_start = """You are a neurosurgeon at one of the top universities in the United States. Please summarize the following information as you would present it in an electronic medical record: 
"""
index = 0 

# if __name__ == "__main__":
#     sms_received = fetch_messages_to_list()[0]
#     fetch_and_log_messages()
#     # if not db:
#     #     send_message(message_content="Please submit patient information now:")
#     message = OpenAI.process(f'{prompt_start} {sms_received}')
#     print(sms_received)
#     if sms_received == "Thanks for the message. Configure your number's SMS URL to change this message.Reply HELP for help.Reply STOP to unsubscribe.Msg&Data rates may apply.":
#         sms_received = ""
#     send_message(message_content= f"- \n\n\n\nPatient Follow-up Services:\n\nIncoming Text: {sms_received}\n\nResponse: Hi, and welcome to Patient Follow-up Services! Please enter your 2FA code:")

####     send_message(message_content= f"- \n\n\n\nPatient Follow-up Services:\n\nIncoming Text: {sms_received}\n\nResponse: {message}")





def patient_view():
    health_questions = [
        "Are you experiencing any pain related to your previous visit? (yes/no): ",
        "Do you have any difficulty breathing? (yes/no): ",
        "Are you feeling dizzy? (yes/no): ",
        "Do you have any swelling? (yes/no): ",
        "Are you experiencing any nausea? (yes/no): "
    ]

    responses = {}
    for question in health_questions:
        response = input(question)
        responses[question] = response
    return responses

def doctor_view():
    patient_data = {}

    while True:
        mode = input("Enter mode (send/retrieve/exit): ").strip().lower()

        if mode == "send":
            patient_id = input("Enter patient ID: ").strip()
            firstName = input("Enter first name: ").strip()
            lastName = input("Enter last name: ").strip()
            phoneNumber = input("Enter phone number: ").strip()
            secondaryPhoneNumber = input("Enter secondary phone number (optional): ").strip()
            email = input("Enter email: ").strip()
            admissionDate = input("Enter admission date (YYYY-MM-DD): ").strip()
            dischargeDate = input("Enter discharge date (YYYY-MM-DD): ").strip()
            contactDate = input("Enter contact date (YYYY-MM-DD): ").strip()
            admissionReason = input("Enter admission reason: ").strip()
            proceduresPerformed = input("Enter procedures performed: ").strip()
            diagnosis = input("Enter diagnosis: ").strip()
            medicationsGiven = input("Enter medications given: ").strip()
            followupInstructions = input("Enter follow-up instructions: ").strip()
            authCode = input("Enter authorization code: ").strip()
            needsFollowUp = input("Needs follow-up? (yes/no): ").strip().lower() == "yes"

            patient_info = (
                firstName,
                lastName,
                phoneNumber,
                secondaryPhoneNumber,
                email,
                admissionDate,
                dischargeDate,
                contactDate,
                admissionReason,
                proceduresPerformed,
                diagnosis,
                medicationsGiven,
                followupInstructions,
                authCode,
                needsFollowUp
            )

            patient_data[patient_id] = patient_info
            print(f"Patient data for ID {patient_id} stored successfully.")

        elif mode == "retrieve":
            patient_id = input("Enter patient ID to retrieve: ").strip()
            if patient_id in patient_data:
                patient_info = patient_data[patient_id]
                print(f"Patient data for ID {patient_id}:")
                print(f"First Name: {patient_info[0]}")
                print(f"Last Name: {patient_info[1]}")
                print(f"Phone Number: {patient_info[2]}")
                print(f"Secondary Phone Number: {patient_info[3]}")
                print(f"Email: {patient_info[4]}")
                print(f"Admission Date: {patient_info[5]}")
                print(f"Discharge Date: {patient_info[6]}")
                print(f"Contact Date: {patient_info[7]}")
                print(f"Admission Reason: {patient_info[8]}")
                print(f"Procedures Performed: {patient_info[9]}")
                print(f"Diagnosis: {patient_info[10]}")
                print(f"Medications Given: {patient_info[11]}")
                print(f"Follow-up Instructions: {patient_info[12]}")
                print(f"Authorization Code: {patient_info[13]}")
                print(f"Needs Follow-up: {patient_info[14]}")
            else:
                print(f"No data found for patient ID {patient_id}.")

        elif mode == "exit":
            break
        else:
            print("Invalid mode. Please enter 'send', 'retrieve', or 'exit'.")

def main():
    while True:
        view = input("Enter view (patient/doctor/exit): ").strip().lower()

        if view == "patient":
            patient_responses = patient_view()
            print("Patient health check responses recorded.")
            for question, response in patient_responses.items():
                print(f"{question}: {response}")

        elif view == "doctor":
            doctor_view()


