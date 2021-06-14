from utils import db_get_many, db_get, db_create, db_del, db_update, timems, db_del_many, db_scan, db_describe

class Users:
    def programs_for_user(self, username):
        """List programs for the given user.

        Returns: [{ code, name, program, level, adventure_name, date }]
        """
        raise NotImplementedError

    def program_by_id(self, id):
        """Get program by ID.

        Returns: { code, name, program, level, adventure_name, date }
        """
        raise NotImplementedError

    def store_program(self, program):
        """Store a program."""
        raise NotImplementedError

    def set_program_public_by_id(self, id, public):
        """Store a program."""
        raise NotImplementedError

    def delete_program_by_id(self, id):
        """Delete a program by id."""
        raise NotImplementedError

    def increase_user_program_count(self, username, delta=1):
        """Increase the program count of a user by the given delta."""
        raise NotImplementedError

    def user_by_username(self, username):
        """Return a user object from the username."""
        raise NotImplementedError

    def user_by_email(self, email):
        """Return a user object from the email address."""
        raise NotImplementedError

    def get_token(self, token):
        """Load a token from the database."""
        raise NotImplementedError

    def store_token(self, token):
        """Store a token in the database."""
        raise NotImplementedError

    def forget_token(self, token_id):
        """Forget a Token.

        Returns the Token that was deleted.
        """
        pass

    def store_user(self, user):
        """Store a user in the database."""
        raise NotImplementedError

    def record_login(self, username, new_password_hash=None):
        """Record the fact that the user logged in, potentially updating their password hash."""
        if new_password_hash:
            self.update_user({'username': username, 'password': new_password_hash, 'last_login': timems ()})
        else:
            self.update_user({'username': username, 'last_login': timems ()})

    def update_user(self, userdata):
        """Update the user data with the given fields.

        This method is a bit of a failing of the API, but there are too many
        slight variants of tweaking some fields on the user in the code to
        turn each of them into a separate method here.
        """
        raise NotImplementedError

    def forget_user(self, username):
        """Forget the given user."""
        raise NotImplementedError

    def all_users(self):
        """Return all users."""
        raise NotImplementedError

    def all_programs_count(self):
        """Return the total number of all programs."""
        raise NotImplementedError

    def all_users_count(self):
        """Return the total number of all users."""
        raise NotImplementedError


class DynamoUsers(Users):
    def programs_for_user(self, username):
        return db_get_many('programs', {'username': username}, True)

    def program_by_id(self, id):
        return db_get('programs', {'id': id})

    def store_program(self, program):
        db_create('programs', program)

    def delete_program_by_id(self, id):
        db_del ('programs', {'id': id})

    def increase_user_program_count(self, username, delta=1):
        db_update('users', {'username': username}, {
            # Use raw updates to do an atomic increment in DDB
            # https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_AttributeValueUpdate.html#DDB-Type-AttributeValueUpdate-Action
            'program_count': {
                'Action': 'ADD',
                'Value': { 'N': delta },
            }})

    def set_program_public_by_id(self, id, public):
        db_update ('programs', {'id': id, 'public': 1 if public else None})

    def user_by_username(self, username):
        return db_get ('users',  {'username': username})

    def user_by_email(self, email):
        """Return a user object from the email address."""
        return db_get ('users', {'email': email}, True)

    def get_token(self, token_id):
        """Load a token from the database."""
        return db_get ('tokens', {'id': token_id})

    def store_token(self, token):
        """Store a token in the database."""
        db_create('tokens', token)

    def forget_token(self, token_id):
        """Forget a token"""
        return db_del('tokens', {'id': token_id})

    def store_user(self, user):
        db_create ('users', user)

    def update_user(self, userdata):
        """Update the user data with the given fields."""
        db_update('users', userdata)

    def forget_user(self, username):
        db_del ('users', {'username': username})
        # The recover password token may exist, so we delete it
        db_del ('tokens', {'id': username})
        db_del_many ('programs', {'username': username}, True)

    def all_users(self):
        return db_scan ('users')

    def all_programs_count(self):
        """Return the total number of all programs."""
        return db_describe ('programs') ['Table'] ['ItemCount']

    def all_users_count(self):
        """Return the total number of all users."""
        return db_describe ('users') ['Table'] ['ItemCount']


class InMemoryUsers(Users):
    def __init__(self):
        self.programs = {}
        self.users = {}
        self.tokens = {}

    def programs_for_user(self, username):
        return [x for x in self.users.values() if x['username'] == username]

    def program_by_id(self, id):
        return self.programs.get(id, None)

    def store_program(self, program):
        self.programs[program['id']] = program

    def delete_program_by_id(self, id):
        del self.programs[id]

    def increase_user_program_count(self, username, delta=1):
        user = self.users.get(username)
        user['program_count'] = user.get('program_count', 0) + delta

    def set_program_public_by_id(self, id, public):
        self.programs[id]['public'] = 1 if public else None

    def user_by_username(self, username):
        return self.users.get(username)

    def user_by_email(self, email):
        """Return a user object from the email address."""
        found = [x for x in self.users.values() if x['email'] == email]
        return found[0] if found else None

    def get_token(self, token_id):
        """Load a token from the database."""
        return self.tokens.get(token_id)

    def store_token(self, token):
        """Store a token in the database."""
        self.tokens[token['id']] = token

    def forget_token(self, token_id):
        """Forget a token"""
        del self.tokens[token_id]

    def store_user(self, user):
        self.users[user['username']] = user

    def update_user(self, userdata):
        """Update the user data with the given fields."""
        self.users.get(userdata['username']).update(userdata)

    def forget_user(self, username):
        del self.users[username]
        self.tokens = {k: v for k, v in self.tokens.items() if v['id'] != username}
        self.program = {k: v for k, v in self.program.items() if v['username'] != username}

    def all_users(self):
        return list(self.users.values())

    def all_programs_count(self):
        """Return the total number of all programs."""
        return len(self.programs)

    def all_users_count(self):
        """Return the total number of all users."""
        return len(self.users)