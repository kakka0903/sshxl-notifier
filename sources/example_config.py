# APPLICATION
test_mode = False

# IFTTT
IFTTT_enabled = False
IFTTT_webhook_link = ''

# EMAIL
email_enabled = False
gmail_address = ''
gmail_password = ''
receiver_email = ''

# REQUEST
url = 'https://booking.sshxl.nl/usercontrols/kim/aanbod/ikwilhuren.asmx/GetAanbodData'
request_json = {
    "aanbodtypes": [],
    "filters": [
        {
            "Soort": "Begindatum",
            "Waarde": "9 Aug 2021"
        },
        {
            "Soort": "Einddatum",
            "Waarde": "29 Jul 2022"
        },
        {
            "Soort": "Regios",
            "Waarde": "Groningen"
        },
        {
            "Soort": "Contingenthouders",
            "Waarde": "University of Groningen (RUG)"
        },
        {
            "Soort": "ContingentDoelgroepen",
            "Waarde": "RUG Bachelor/Master"
        },
        {
            "Soort": "ContingentPeriodes",
            "Waarde": "RUG Bachelor/Master Full Year - 9 Aug 2021/29 Jul 2022"
        }
    ],
    "filtersoorten": [
        "Complex",
        "Type"
    ]
}
