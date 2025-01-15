import os
import json
import hashlib
import requests
import logging
import threading
from config import config
from functools import wraps
from hedy_content import COUNTRIES
from website.auth import send_email

logger = logging.getLogger(__name__)

MAILCHIMP_API_URL = None
MAILCHIMP_API_HEADERS = {}
MAILCHIMP_TIMEOUT_SECONDS = 15
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


def run_if_mailchimp_config_present(f):
    """ Decorator that runs a particular Mailchimp-dependent function only if there are credentials available. """
    @wraps(f)
    def inner(*args, **kws):
        if MAILCHIMP_API_URL:
            f(*args, **kws)

    return inner


def fire_and_forget(f):
    def run():
        try:
            f()
        except Exception as e:
            logger.exception(f'Exception in background thread: {e}')

    threading.Thread(target=run, daemon=True).start()


@run_if_mailchimp_config_present
def create_subscription(email, country):
    """ Subscribes the user to the newsletter. Currently, users can subscribe to the newsletter only on signup and
    only if they are creating a teacher account. """
    def create():
        tags = [country, MailchimpTag.TEACHER]
        create_mailchimp_subscriber(email, tags)
    fire_and_forget(create)


@run_if_mailchimp_config_present
def update_subscription(current_email, new_email, new_country):
    def update():
        """ Updates the newsletter subscription when the user changes their email or/and their country """
        response = get_mailchimp_subscriber(current_email)
        if response and response.status_code == 200:
            current_tags = response.json().get('tags', [])
            if new_email != current_email:
                # If user is subscribed, we remove the old email from the list and add the new one
                new_tags = [t.get('name') for t in current_tags if t.get('name') not in COUNTRIES] + [new_country]
                successfully_created = create_mailchimp_subscriber(new_email, new_tags)
                if successfully_created:
                    delete_mailchimp_subscriber(current_email)
            else:
                # If the user did not change their email, check if the country needs to be updated
                tags_to_update = get_country_tag_changes(current_tags, new_country)
                if tags_to_update:
                    update_mailchimp_tags(current_email, tags_to_update)

    fire_and_forget(update)


def add_class_created_to_subscription(email):
    create_subscription_event(email, MailchimpTag.CREATED_CLASS)


def add_class_customized_to_subscription(email):
    create_subscription_event(email, MailchimpTag.CUSTOMIZED_CLASS)


@run_if_mailchimp_config_present
def create_subscription_event(email, tag):
    """ When certain events occur, e.g. a newsletter subscriber creates or customizes a class, these events
    should be reflected in their subscription, so that we can send them relevant content """
    def create():
        r = get_mailchimp_subscriber(email)
        if r.status_code == 200:
            current_tags = r.json().get('tags', [])
            if not any([t for t in current_tags if t.get('name') == tag]):
                new_tags = current_tags + [to_mailchimp_tag(tag)]
                update_mailchimp_tags(email, new_tags)
    fire_and_forget(create)


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
    return not subscription_error


def get_mailchimp_subscriber(email):
    request_path = f'{MAILCHIMP_API_URL}/members/{get_subscriber_hash(email)}'
    return requests.get(request_path, headers=MAILCHIMP_API_HEADERS, timeout=MAILCHIMP_TIMEOUT_SECONDS)


def update_mailchimp_tags(email, tags):
    request_path = f'{MAILCHIMP_API_URL}/members/{get_subscriber_hash(email)}/tags'
    return requests.post(
        request_path,
        headers=MAILCHIMP_API_HEADERS,
        data=json.dumps({'tags': tags}),
        timeout=MAILCHIMP_TIMEOUT_SECONDS
    )


def delete_mailchimp_subscriber(email):
    request_path = f'{MAILCHIMP_API_URL}/members/{get_subscriber_hash(email)}'
    requests.delete(request_path, headers=MAILCHIMP_API_HEADERS, timeout=MAILCHIMP_TIMEOUT_SECONDS)


def get_subscriber_hash(email):
    """ Hashes the email with md5 to avoid emails with unescaped characters triggering errors """
    return hashlib.md5(email.encode("utf-8")).hexdigest()
