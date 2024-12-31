import os
import json
import hashlib
import requests
from config import config
from hedy_content import COUNTRIES
from website.auth import send_email


MAILCHIMP_API_URL = None
MAILCHIMP_API_HEADERS = {}
if os.getenv("MAILCHIMP_API_KEY") and os.getenv("MAILCHIMP_AUDIENCE_ID"):
    # The domain in the path is the server name, which is contained in the Mailchimp API key
    MAILCHIMP_API_URL = (
        "https://"
        + os.getenv("MAILCHIMP_API_KEY").split("-")[1]
        + ".api.mailchimp.com/3.0/lists/"
        + os.getenv("MAILCHIMP_AUDIENCE_ID")
    )
    MAILCHIMP_API_HEADERS = {
        "Content-Type": "application/json",
        "Authorization": "apikey " + os.getenv("MAILCHIMP_API_KEY"),
    }


def create_subscription(email, country):
    """ Subscribes the user to the newsletter. Currently, users can subscribe to the newsletter only on signup and
    only if they are creating a teacher account. """
    # If there is a Mailchimp API key, use it to add the subscriber through the API
    if MAILCHIMP_API_URL:
        create_mailchimp_subscriber(email, [country, MailchimpTag.TEACHER])
    # Otherwise, email to notify about the subscription to the main email address
    else:
        recipient = config["email"]["sender"]
        send_email(recipient, "Subscription to Hedy newsletter on signup", email, f"<p>{email}</p>")


def update_subscription(current_email, new_email, new_country):
    """ Updates the newsletter subscription when the user changes their email or/and their country """
    if not MAILCHIMP_API_URL:
        # TODO: Why do we send an email to hello@hedy.org if a user subscribes and there is no mailchimp api key
        #  but if the user changes their email and we do not have a key, we do nothing?
        return
    r = get_mailchimp_subscriber(current_email)
    if r.status_code == 200:
        current_tags = r.json().get('tags', [])
        if new_email != current_email:
            # If user is subscribed, we remove the old email from the list and add the new one
            new_tags = [t.get('name') for t in current_tags if t.get('name') not in COUNTRIES] + [new_country]
            create_mailchimp_subscriber(new_email, new_tags)
            delete_mailchimp_subscriber(current_email)
        else:
            # If the user did not change their email, check if the country needs to be updated
            tags_to_update = get_country_tag_changes(current_tags, new_country)
            if tags_to_update:
                update_mailchimp_tags(current_email, tags_to_update)


def add_class_created_to_subscription(email):
    create_subscription_event(email, MailchimpTag.CREATED_CLASS)


def add_class_customized_to_subscription(email):
    create_subscription_event(email, MailchimpTag.CUSTOMIZED_CLASS)


def create_subscription_event(email, tag):
    """ When certain events occur, e.g. a newsletter subscriber creates or customizes a class, these events
    should be reflected in their subscription, so that we can send them relevant content """
    if not MAILCHIMP_API_URL:
        return
    r = get_mailchimp_subscriber(email)
    if r.status_code == 200:
        current_tags = r.json().get('tags', [])
        if not any([t for t in current_tags if t.get('name') == tag]):
            new_tags = current_tags + [to_mailchimp_tag(tag)]
            update_mailchimp_tags(email, new_tags)


def get_country_tag_changes(current_tags, country):
    """ Returns the necessary alterations to the tags of the newsletter subscriber when they change their country.
     The old country tag, if existing, should be removed, and the new country, if existing, should be added. """
    current_country_tags = [t.get('name') for t in current_tags if t.get('name') in COUNTRIES]

    if country in current_country_tags:
        return []

    changes = [to_mailchimp_tag(t, active=False) for t in current_country_tags]
    if country:
        changes.append(to_mailchimp_tag(country))
    return changes


def to_mailchimp_tag(tag, active=True):
    # https://mailchimp.com/developer/marketing/api/list-member-tags/
    status = 'active' if active else 'inactive'
    return {'name': tag, 'status': status}


class MailchimpTag:
    TEACHER = 'teacher'
    CREATED_CLASS = "created_class"
    CUSTOMIZED_CLASS = "customized_class"


def create_mailchimp_subscriber(email, tag_names):
    tag_names = [t for t in tag_names if t]  # the country can be None, so filter it
    request_body = {"email_address": email, "status": "subscribed", "tags": tag_names}
    request_path = MAILCHIMP_API_URL + "/members/"
    r = requests.post(request_path, headers=MAILCHIMP_API_HEADERS, data=json.dumps(request_body))

    subscription_error = None
    if r.status_code != 200 and r.status_code != 400:
        subscription_error = True
    # We can get a 400 if the email is already subscribed to the list. We should ignore this error.
    if r.status_code == 400 and "already a list member" not in r.text:
        subscription_error = True
    # If there's an error in subscription through the API, we report it to the main email address
    if subscription_error:
        send_email(
            config["email"]["sender"],
            "ERROR - Subscription to Hedy newsletter",
            f"email: {email} status: {r.status_code} body: {r.text}",
            f"<p>{email}</p><pre>Status:{r.status_code}    Body:{r.text}</pre>")


def get_mailchimp_subscriber(email):
    request_path = f'{MAILCHIMP_API_URL}/members/{get_subscriber_hash(email)}'
    return requests.get(request_path, headers=MAILCHIMP_API_HEADERS)


def update_mailchimp_tags(email, tags):
    request_path = f'{MAILCHIMP_API_URL}/members/{get_subscriber_hash(email)}/tags'
    return requests.post(request_path, headers=MAILCHIMP_API_HEADERS, data=json.dumps({'tags': tags}))


def delete_mailchimp_subscriber(email):
    request_path = f'{MAILCHIMP_API_URL}/members/{get_subscriber_hash(email)}'
    requests.delete(request_path, headers=MAILCHIMP_API_HEADERS)


def get_subscriber_hash(email):
    """ We hash the email with md5 to avoid emails with unescaped characters triggering errors """
    return hashlib.md5(email.encode("utf-8")).hexdigest()
