import json
import config
import requests
import smtplib
import ssl
import time
from datetime import datetime


def get_listings():
    """ get listings from sshxl website api """
    try:
        response = requests.post(config.url, json=config.request_json)
        listings = response.json()['d']['Advertenties']
        return listings
    except Exception:
        return None


def get_fake_listings():
    """ return fake listings for test purposes """
    return [{"Naam": "Upsilon", "HuurObjecten": [{}, {}]}, {"Naam": "Windeip", "HuurObjecten": [{}, {}]}]


def parse_listings(listings):
    """ returns name and roomsavailable in tuples in a list """
    results = []
    for listing in listings:
        name = listing['Naam'].split(' ')[0]
        rooms_available = len(listing["HuurObjecten"])
        results.append((name, rooms_available))

    return results


def get_listings_string(listings):
    """ get listings string for sending in notifications """
    # get listings names and available number
    parsed_listings = parse_listings(listings)
    listings_string = ", ".join([f"{tup[0]} ({tup[1]})" for tup in parsed_listings])
    if not listings_string:
        listings_string = 'No listings'

    return listings_string


def send_IFTTT_notification(title, text, link):
    """ send IFTTT notification if enabled in config """
    if config.IFTTT_enabled:
        requests.post(
            config.IFTTT_webhook_link,
            headers={'Content-Type': 'application/json'},
            data=json.dumps({"value1": title, "value2": text, "value3": link}),
        )
        print('IFTTT notification sent')


def send_email_notification(subject, text, link):
    """ send email notification if enabled in config """
    if config.email_enabled:
        # build message
        message = f'subject: {subject}\n\n {text}. {link}.'

        # Create a secure SSL context
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            # login to gmail and send
            server.login(config.gmail_address, config.gmail_password)
            server.sendmail(config.gmail_address, config.receiver_email, message)
            print('email sent')


def main():
    last_listings = None
    listings = None
    count = 0

    while True:
        if config.test_mode and count == 5:
            # get fake listings for test
            listings = get_fake_listings()
            count = 0
        else:
            listings = get_listings()

        timestamp = datetime.now().strftime("%H:%M:%S")

        if listings is not None:
            # get parsed listings and build listings string
            listings_string = get_listings_string(listings)
            listings_link = 'https://booking.sshxl.nl/accommodations'

            if last_listings is not None and listings != last_listings:
                send_IFTTT_notification('SSHXL Updated!', listings_string, listings_link)
                send_email_notification('(!!!) SSHXL LISTINGS UPDATED (!!!)', listings_string, listings_link)

            print(f'{timestamp}: {listings_string}')
            last_listings = listings
        else:
            print(f'{timestamp}: could not get listings')

        time.sleep(1)
        count += 1


if __name__ == '__main__':
    main()
