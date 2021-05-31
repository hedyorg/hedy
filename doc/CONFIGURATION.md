# Server configuration

A place to start recording all the special config that needs to be set to make this
server work.

## Config via environment variables

AWS credentials and setup:

```
AWS_DYNAMODB_ACCESS_KEY
AWS_DYNAMODB_SECRET_KEY
AWS_DYNAMODB_TABLE_PREFIX

AWS_SES_ACCESS_KEY
AWS_SES_SECRET_KEY
```

JSONbin credentials and setup:

```
JSONBIN_COLLECTION_ID
JSONBIN_SECRET_KEY
```

HTTP redirect:

```
REDIRECT_HTTP_TO_HTTPS
```

Email:

```
MAILCHIMP_AUDIENCE_ID
MAILCHIMP_API_KEY
BASE_URL
```

A/B testing:

```
PROXY_TO_TEST_HOST
PROXY_TO_TEST_PROPORTION
IS_TEST_ENV
```

App secret (for cookies):

```
SECRET_KEY
```

To determine if this is the production environment (to avoid requests from e2e tests being considered as such, to avoid any sort of security loopholes):

```
IS_PRODUCTION
```

To set up the port of the app through an env variable (helpful to start multiple instances of the app locally

```
PORT
```

## Heroku Metadata

This app depends on some environment variables that require Heroku dyno metadata.

Enable using the Heroku CLI:

```
$ heroku labs:enable runtime-dyno-metadata -a <app name>
```
