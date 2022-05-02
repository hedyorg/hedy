class HedyException(Exception):
    def __init__(self, error_code, **arguments):
        """Create a new HedyException.

        You should not create a HedyException directly. Instead, use any of
        the subclasses of HedyException below.

        The keyword arguments passed into this constructor become available
        in exception translation strings. In those arguments, the keywords
        'location' and 'line_number' are special: they will be used to indicate
        the error location in the client.
        """
        super().__init__(error_code)

        self.error_code = error_code
        self.arguments = arguments

    @property
    def error_location(self):
        """Return the location where the error was found.

        Returns either an array of [row, col] or just [row].

        If 'location' is part of the keyword arguments, return that.
        Otherwise, if 'line_number' is part of the keyword arguments, return that instead.
        """
        if 'location' in self.arguments:
            return self.arguments['location']
        if 'line_number' in self.arguments:
            return [self.arguments['line_number']]
        return None

class FtfyException(HedyException):
    """Fixed That For You warning/exception.

    Not really a failure case: instead it represents a warning to
    the user that they made a mistake we recovered for them.

    'fixed_code' and 'fixed_result' will contain the repaired
    code, and the result of compiling that repaired code.
    """
    def __init__(self, error_code, fixed_code, fixed_result, **arguments):
        super().__init__(error_code, **arguments)
        self.fixed_code = fixed_code
        self.fixed_result = fixed_result

class InvalidSpaceException(FtfyException):
    def __init__(self, level, line_number, fixed_code, fixed_result):
        super().__init__('Invalid Space',
            level=level,
            line_number=line_number,
            fixed_code=fixed_code,
            fixed_result=fixed_result)

class ParseException(HedyException):
    def __init__(self, level, location, found, fixed_code=None):
        super().__init__('Parse',
            level=level,
            location=location,
            found=found,
            # 'character_found' for backwards compatibility
            character_found=found)

        #TODO (FH, 8 dec 21) many exceptions now support fixed code maybe we should move it to hedyexception?
        self.fixed_code = fixed_code

class UnquotedEqualityCheck(HedyException):
    def __init__(self, line_number):
        super().__init__('Unquoted Equality Check',
             line_number=line_number)
        self.location = [line_number]

class UndefinedVarException(HedyException):
    def __init__(self, name):
        super().__init__('Var Undefined',
            name=name)

class CyclicVariableDefinitionException(HedyException):
    def __init__(self, variable):
        super().__init__('Cyclic Var Definition',
                         variable=variable)

class InvalidArgumentTypeException(HedyException):
    def __init__(self, command, invalid_type, allowed_types, invalid_argument):
        super().__init__('Invalid Argument Type',
            command=command,
            invalid_type=invalid_type,
            allowed_types=allowed_types,
            invalid_argument=invalid_argument)

class InvalidTypeCombinationException(HedyException):
    def __init__(self, command, arg1, arg2, type1, type2):
        super().__init__('Invalid Type Combination',
            command=command,
            invalid_argument=arg1,
            invalid_argument_2=arg2,
            invalid_type=type1,
            invalid_type_2=type2)

class InvalidArgumentException(HedyException):
    def __init__(self, command, allowed_types, invalid_argument):
        super().__init__('Invalid Argument',
            command=command,
            allowed_types=allowed_types,
            invalid_argument=invalid_argument)

class WrongLevelException(HedyException):
    def __init__(self, working_level, offending_keyword, tip):
        super().__init__('Wrong Level',
            working_level=working_level,
            offending_keyword=offending_keyword,
            tip=tip)

class InputTooBigException(HedyException):
    def __init__(self, lines_of_code, max_lines):
        super().__init__('Too Big',
            lines_of_code=lines_of_code,
            max_lines=max_lines)

class InvalidCommandException(FtfyException):
    def __init__(self, level, invalid_command, guessed_command, line_number, fixed_code, fixed_result):
        super().__init__('Invalid',
            invalid_command=invalid_command,
            level=level,
            guessed_command=guessed_command,
            line_number=line_number,
            fixed_code=fixed_code,
            fixed_result=fixed_result)
        self.location = [line_number]

class MissingCommandException(HedyException):
    def __init__(self, level, line_number):
        super().__init__('Missing Command',
            level=level,
            line_number=line_number)

class MissingInnerCommandException(HedyException):
    def __init__(self, command, level, line_number):
        super().__init__('Missing Inner Command',
            command=command,
            level=level,
            line_number=line_number)

class IncompleteCommandException(HedyException):
    def __init__(self, incomplete_command, level, line_number):
        super().__init__('Incomplete',
            incomplete_command=incomplete_command,
            level=level,
            line_number=line_number)

        # Location is copied here so that 'hedy_error_to_response' will find it
        # Location can be either [row, col] or just [row]
        self.location = [line_number]

class UnquotedTextException(HedyException):
    def __init__(self, level):
        super().__init__('Unquoted Text', level=level)

class UnquotedAssignTextException(HedyException):
    def __init__(self, text):
        super().__init__('Unquoted Assignment', text=text)

class LonelyEchoException(HedyException):
    def __init__(self):
        super().__init__('Lonely Echo')

class CodePlaceholdersPresentException(HedyException):
    def __init__(self):
        super().__init__('Has Blanks')

class NoIndentationException(HedyException):
    def __init__(self, line_number, leading_spaces, indent_size, fixed_code=None):
        super().__init__('No Indentation',
            line_number=line_number,
            leading_spaces=leading_spaces,
            indent_size=indent_size)
        self.fixed_code = fixed_code

class IndentationException(HedyException):
    def __init__(self, line_number, leading_spaces, indent_size, fixed_code=None):
        super().__init__('Unexpected Indentation',
            line_number=line_number,
            leading_spaces=leading_spaces,
            indent_size=indent_size)
        self.fixed_code = fixed_code

class UnsupportedFloatException(HedyException):
    def __init__(self, value):
        super().__init__('Unsupported Float', value=value)

class LockedLanguageFeatureException(HedyException):
    def __init__(self, concept):
        super().__init__('Locked Language Feature', concept=concept)

class UnsupportedStringValue(HedyException):
    def __init__(self, invalid_value):
        super().__init__('Unsupported String Value', invalid_value=invalid_value)
