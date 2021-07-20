from utils import timems
from . import dynamo

storage = dynamo.AwsDynamoStorage.from_env() or dynamo.MemoryStorage('dev_database.json')

USERS = dynamo.Table(storage, 'users', 'username', indexed_fields=['email'])
TOKENS = dynamo.Table(storage, 'tokens', 'id')
PROGRAMS = dynamo.Table(storage, 'programs', 'id', indexed_fields=['username'])

class Database:
    def programs_for_user(self, username):
        """List programs for the given user, newest first.

        Returns: [{ code, name, program, level, adventure_name, date }]
        """
        return PROGRAMS.get_many({'username': username}, reverse=True)

    def program_by_id(self, id):
        """Get program by ID.

        Returns: { code, name, program, level, adventure_name, date }
        """
        return PROGRAMS.get({'id': id})

    def store_program(self, program):
        """Store a program."""
        PROGRAMS.create(program)

    def set_program_public_by_id(self, id, public):
        """Store a program."""
        PROGRAMS.update({'id': id}, {'public': 1 if public else None})

    def delete_program_by_id(self, id):
        """Delete a program by id."""
        PROGRAMS.delete({'id': id})

    def increase_user_program_count(self, username, delta=1):
        """Increase the program count of a user by the given delta."""
        return USERS.update({ 'username': username }, {
            'program_count': dynamo.DynamoIncrement(delta)
        })

    def user_by_username(self, username):
        """Return a user object from the username."""
        return USERS.get({'username': username})

    def user_by_email(self, email):
        """Return a user object from the email address."""
        return USERS.get({'email': email})

    def get_token(self, token_id):
        """Load a token from the database."""
        return TOKENS.get({'id': token_id})

    def store_token(self, token):
        """Store a token in the database."""
        TOKENS.create(token)

    def forget_token(self, token_id):
        """Forget a Token.

        Returns the Token that was deleted.
        """
        return TOKENS.delete({'id': token_id})

    def store_user(self, user):
        """Store a user in the database."""
        USERS.create(user)

    def record_login(self, username, new_password_hash=None):
        """Record the fact that the user logged in, potentially updating their password hash."""
        if new_password_hash:
            self.update_user(username, {'password': new_password_hash, 'last_login': timems ()})
        else:
            self.update_user(username, {'last_login': timems ()})

    def update_user(self, username, userdata):
        """Update the user data with the given fields.

        This method is a bit of a failing of the API, but there are too many
        slight variants of tweaking some fields on the user in the code to
        turn each of them into a separate method here.
        """
        USERS.update({'username': username}, userdata)

    def forget_user(self, username):
        """Forget the given user."""
        USERS.delete({'username': username})
        # The recover password token may exist, so we delete it
        TOKENS.delete({'id': username})
        PROGRAMS.del_many({'username': username})

    def all_users(self):
        """Return all users."""
        return USERS.scan()

    def all_programs_count(self):
        """Return the total number of all programs."""
        return PROGRAMS.item_count()

    def all_users_count(self):
        """Return the total number of all users."""
        return USERS.item_count()