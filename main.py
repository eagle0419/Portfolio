import requests
import json
import time
import random
import smtplib
import ssl
import string

import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

apiKey = "1234567890!@#$%^&*()"
propKeys = [
    "201631_b58aa6d0420c4bb6588446ea6040238750b114b20484e07a",
    "202052_4c9955f2362ef50635d29d0cc2a6022da747dc7f7006e9fc",
    "201633_93f3701e049a3755ab1eedaa498e3e598ec5f7fa5344b16a",
    "202054_d1e4036174e65215046870823a98552b0a8a85c9ffed705e",
    "201632_139cae682c8788eb3d2a7aea1756b65bce102d216b745966",
    "202050_a7a4b4af41ad4f84fd892e1eec377e19d67d973e8dbdca50",
    "201648_333f33644af4da7d388ba29d5d47557898e2c1376e0fce3c"
]

booking_history = []


def get_history():
    print("Getting History...")
    for propKey in propKeys:
        data = {
            "authentication": {
                "apiKey": apiKey,
                "propKey": propKey
            }
        }
        json_data = json.dumps(data)
        headers = {"Content-Type": "application/json"}

        response = requests.get(
            "https://api.beds24.com/json/getBookings", data=json_data, headers=headers)
        if response.status_code != 200:
            print("Failed to get history")
            return
        books = response.json()
        for book in books:
            print(book)
            booking_history.append(book)

    print("\nAll Done.\n")


def main():
    for propKey in propKeys:
        data = {
            "authentication": {
                "apiKey": apiKey,
                "propKey": propKey
            }
        }
        json_data = json.dumps(data)

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.get(
            "https://api.beds24.com/json/getBookings", data=json_data, headers=headers)
        if response.status_code != 200:
            print("Request failed with status code:", response.status_code)

        books = response.json()
        for book in books:
            if book not in booking_history:
                try:
                    pincode = random.randint(1000, 9999).__str__()
                    print(
                        f"\nNew Booking Detected\n   Book Details:\n\tReservationTime: {book['bookingTime']}\n\tReservationID: {book['bookId']}\n\tDateFrom: {book['firstNight']}\n\tDateTo: {book['lastNight']}\n\tEmail: {book['guestEmail']}")
                    json_data = json.dumps({
                        "reservationDate": book["bookingTime"].split(' ')[0],
                        "eventCode": "Test",
                        "companyCode": "Test1",
                        "reservationID": book["bookId"],
                        "entertainments": [{
                            "entertainmentCode": "Test",
                            "dateFrom": book["firstNight"],
                            "dateTo": book["lastNight"],
                            "auths": [{
                                "authType": 1,
                                "authValue": pincode
                            }]
                        }]
                    })
                    print(
                        "   Sending Request to https://mano.acoris.lt/rezervation/api/UserApi/EntertainmentReservation ...")
                    response = requests.post(
                        "https://mano.acoris.lt/rezervation/api/UserApi/EntertainmentReservation", data=json_data, headers=headers)

                    if response.status_code != 200:
                        print("Request failed with status code:",
                              response.status_code)
                    print("   Response:")
                    print("\t", response.json(), "\n")
                    booking_history.append(book)

                    # Email details
                    sender_email = 'rezervations@rezerv.lt'
                    receiver_email = 'recipient_email@example.com'
                    password = 'y7y&nF38'
                    subject = 'pincode'
                    message = f"{pincode}"

                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = receiver_email
                    msg['Subject'] = subject

                    msg.attach(MIMEText(message, 'plain'))

                    smtp_server = 'plesk01.on-cloud.pro'
                    smtp_port = 465

                    try:
                        # Create a secure SSL connection with the SMTP server
                        server = smtplib.SMTP_SSL(smtp_server, smtp_port)

                        # Login to the email account
                        server.login(sender_email, password)

                        # Send the email
                        server.sendmail(
                            sender_email, receiver_email, msg.as_string())
                        print('Email sent successfully!')
                    except Exception as e:
                        print('An error occurred while sending the email:', str(e))
                    finally:
                        # Close the SMTP server connection
                        server.quit()

                except:
                    pass


if __name__ == "__main__":
    get_history()
    # print(booking_history)
    print("Real Time Scanning...")
    while True:
        main()
        time.sleep(30)
