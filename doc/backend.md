# Backend documentation

## Routes

### Auth

- `POST /auth/login`
    - This route creates a new session for an existing user.
    - Requires a body of the form `{username: STRING, password: STRING}`. Otherwise, the route returns 400.
    - If `username` contains an `@`, it is considered an email.
    - `username` is stripped of any whitespace at the beginning or the end; it is also lowercased.
    - If successful, the route returns 200 and a `cookie` header containing the session. Otherwise, the route returns 403.
    - For the route to be successful, the user should have already verified their account through `GET /auth/verify`.

- `POST /auth/signup`
    - This route creates a new user.
    - Requires a body of the form `{username: STRING, password: STRING, email: STRING, country: STRING|UNDEFINED, age: INTEGER|UNDEFINED, gender: m|f|UNDEFINED}`. Otherwise, the route returns 400.
    - If present, `country` must be a valid [ISO 3166 Alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements).
    - If present, `age` must be an integer larger than 0.
    - If present, `gender` must be either `m` or `f`.
    - `email` must be a valid email.
    - `password` must be at least six characters long.
    - If `username` contains an `@`, it is considered an email.
    - Both `username` and `email` are stripped of any whitespace at the beginning or the end; they are also lowercased.
    - Both `username` and `email` should not be in use by an existing user. Otherwise, the route returns 403.
    - If successful, the route returns 200. It also will send a verification email to the provided `email`.

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

- `POST /auth/changePassword`
    - This route changes the user's password.
    - Requires a body of the form `{oldPassword: STRING, newPassword: STRING}`. Otherwise, the route returns 400.
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
    - If successful, this route returns 200 with a body of the shape `{username: STRING, email: STRING, age: INTEGER|UNDEFINED, country: STRING|UNDEFINED, gender: m|f|UNDEFINED}`.

- `POST /profile`
    - This route allows the user to change its `email`, `age`, `gender` and/or `country`.
    - This route requires a session, otherwise it returns 403.
    - Requires a body of the form `{email: STRING|UNDEFINED, country: STRING|UNDEFINED, age: INTEGER|UNDEFINED, gender: m|f|UNDEFINED}`. Otherwise, the route returns 400.
    - If present, `country` must be a valid [ISO 3166 Alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements).
    - If present, `age` must be an integer larger than 0.
    - If present, `gender` must be either `m` or `f`.
    - If present, `email` must be a valid email.
    - `email` should not be in use by an existing user. Otherwise, the route returns 403.
    - If successful, the route returns 200.

## Redis

```
email (hash): keys are emails, values are corresponding usernames.

user:USERNAME (hash):
    username:    STRING
    password:    STRING (not the original password, but a bcrypt hash of it)
    email:       STRING
    age:         INTEGER|UNDEFINED
    country:     STRING|UNDEFINED
    gender:      m|f|UNDEFINED
    created:     INTEGER
    last_access: INTEGER|UNDEFINED
    verification_pending: STRING|UNDEFINED (if present, contains the a hash of the email verification token)

sess:ID (string): ID is session, value is corresponding username.

token:USERNAME (string): value is hash of recover password token.
```
