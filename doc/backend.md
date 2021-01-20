# Backend documentation

## Routes

### Auth

- `POST /auth/login`
    - This route creates a new session for an existing user.
    - Requires a body of the form `{username: STRING, password: STRING}`. Otherwise, the route returns 400.
    - If `username` contains an `@`, it is considered an email.
    - `username` is stripped of any whitespace at the beginning or the end; it is also lowercased.
    - If successful, the route returns 200 and a `cookie` header containing the session. Otherwise, the route returns 403.

- `POST /auth/signup`
    - This route creates a new user.
    - Requires a body of the form `{username: STRING, password: STRING, email: STRING, country: STRING|UNDEFINED, birth_year: INTEGER|UNDEFINED, gender: m|f|o|UNDEFINED, subscribe: true|false|UNDEFINED}`. Otherwise, the route returns 400.
    - If present, `country` must be a valid [ISO 3166 Alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements).
    - If present, `birth_year` must be an integer between 1900 and the current calendar year.
    - If present, `gender` must be either `m`, `f` or `o`.
    - If present, `subscribe` must be either boolean or undefined and if `true`, indicates that the user wants to subscribe to the Hedy newsletter.
    - `email` must be a valid email.
    - `password` must be at least six characters long.
    - If `username` contains an `@`, it is considered an email.
    - Both `username` and `email` are stripped of any whitespace at the beginning or the end; they are also lowercased.
    - Both `username` and `email` should not be in use by an existing user. Otherwise, the route returns 403.
    - The trimmed `username` must be at least three characters long.
    - If successful, the route returns 200. It will also send a verification email to the provided `email`.

- `GET /auth/verify?username=USERNAME&token=TOKEN`
    - This route verifies ownership of the email address of a new user.
    - If the query parameters `username` or `token` are missing, the route returns 400.
    - If the `token` doesn't correspond to `username`, the route returns 403.
    - If successful, the route returns a 302 redirecting to `/`.

- `POST /auth/logout`
    - This route destroys the current session.
    - This route is always successful and returns 200. It will only destroy a session only if a valid cookie is set.

- `POST /auth/destroy`
    - This route destroys the user's account.
    - This route requires a session, otherwise it returns 403.
    - If successful, the route returns 200.

- `POST /auth/change_password`
    - This route changes the user's password.
    - Requires a body of the form `{old_password: STRING, new_password: STRING}`. Otherwise, the route returns 400.
    - `newPassword` must be at least six characters long.
    - If successful, the route returns 200.

- `POST /auth/recover`
    - This route sends a password recovery email to the user.
    - Requires a body of the form `{username: STRING}`. Otherwise, the route returns 400.
    - If `username` contains an `@`, it is considered an email.
    - `username` or `email` must belong to an existing user. Otherwise, the route returns 403.
    - `username` is stripped of any whitespace at the beginning or the end; it is also lowercased.
    - If successful, the route returns 200 and sends a recovery password email to the user.

- `POST /auth/reset`
    - This route allows an user to set a new password using a password recovery token.
    - Requires a body of the form `{username: STRING, token: STRING, password: STRING}`. Otherwise, the route returns 400.
    - If `username` contains an `@`, it is considered an email.
    - `username` is stripped of any whitespace at the beginning or the end; it is also lowercased.
    - `password` must be at least six characters long.
    - If the `username`/`token` combination is not correct, the route returns 403.
    - If successful, the route returns 200 and sends an email to notify the user that their password has been changed.

### Profile

- `GET /profile`
    - This route allows the user to retrieve their profile.
    - This route requires a session, otherwise it returns 403.
    - If successful, this route returns 200 with a body of the shape `{username: STRING, email: STRING, birth_year: INTEGER|UNDEFINED, country: STRING|UNDEFINED, gender: m|f|o|UNDEFINED, verification_pending: UNDEFINED|true}`.

- `POST /profile`
    - This route allows the user to change its `email`, `birth_year`, `gender` and/or `country`.
    - This route requires a session, otherwise it returns 403.
    - Requires a body of the form `{email: STRING|UNDEFINED, country: STRING|UNDEFINED, birth_year: INTEGER|UNDEFINED, gender: m|f|oUNDEFINED}`. Otherwise, the route returns 400.
    - If present, `country` must be a valid [ISO 3166 Alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements).
    - If present, `birth_year` must be an integer between 1900 and the current calendar year.
    - If present, `gender` must be either `m`, `f` or `o`.
    - If present, `email` must be a valid email.
    - `email` should not be in use by an existing user. Otherwise, the route returns 403.
    - If `email` is present and different from the existing email, the route will also send a verification email to the provided `email`.
    - If successful, the route returns 200.

- `GET /users`
    - This route allows the admin user to retrieve a list of all the users in the system.
    - If there's no session or the logged in user is not the admin user, it returns 403.
    - If successful, the route will return a template containing a table with all the users in the system. The users will be sorted by creation date, last first.

## DynamoDB

```
table users:
    username:    STRING (main index)
    password:    STRING (not the original password, but a bcrypt hash of it)
    email:       STRING (secondary index)
    birth_year:  INTEGER|UNDEFINED
    country:     STRING|UNDEFINED
    gender:      m|f|UNDEFINED
    created:     INTEGER (epoch milliseconds)
    last_login:  INTEGER|UNDEFINED (epoch milliseconds)

table tokens:
    id:       STRING (main index; for password reset tokens, id is the username)
    username: STRING|UNDEFINED (only set for session tokens)
    token:    STRING|UNDEFINED (only set for password reset tokens)
    ttl:      INTEGER (epoch seconds)
```
