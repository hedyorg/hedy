import inspect
"""
    Any exception added in this file must be also added to error-messages.txt
    So we can translate the error message. The exception must also be assigned
    an Exception Type in the exception_types dictionary in statistics.py
"""


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
        Otherwise, if 'line_number' is part of the keyword arguments, return that instead
        wrapped in a list so we are sure the return type is always a list.

        """
        if 'location' in self.arguments:
            return self.arguments['location']
        if 'line_number' in self.arguments:
            return [self.arguments['line_number']]
        return None


class WarningException(HedyException):
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


class InvalidSpaceException(WarningException):
    def __init__(self, level, line_number, fixed_code, fixed_result):
        super().__init__('Invalid Space',
                         level=level,
                         line_number=line_number,
                         fixed_code=fixed_code,
                         fixed_result=fixed_result)  # what is the difference??


class UnusedVariableException(WarningException):
    def __init__(self, level, line_number, variable_name, fixed_code, fixed_result):
        super().__init__('Unused Variable',
                         level=level,
                         line_number=line_number,
                         variable_name=variable_name,
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

        # TODO (FH, 8 dec 21) many exceptions now support fixed code maybe we
        # should move it to hedyexception?
        self.fixed_code = fixed_code


class UnquotedEqualityCheckException(HedyException):
    def __init__(self, line_number):
        super().__init__('Unquoted Equality Check',
                         line_number=line_number)
        self.location = [line_number]


class AccessBeforeAssignException(HedyException):
    def __init__(self, name, access_line_number, definition_line_number):
        super().__init__('Access Before Assign',
                         name=name,
                         access_line_number=access_line_number,
                         line_number=access_line_number,
                         definition_line_number=definition_line_number)


class UndefinedVarException(HedyException):
    def __init__(self, name, line_number):
        super().__init__('Var Undefined',
                         name=name,
                         line_number=line_number)


class UndefinedFunctionException(HedyException):
    def __init__(self, name, line_number):
        super().__init__('Function Undefined',
                         name=name,
                         line_number=line_number)


class CyclicVariableDefinitionException(HedyException):
    def __init__(self, variable, line_number):
        super().__init__('Cyclic Var Definition',
                         variable=variable,
                         line_number=line_number)


class InvalidArgumentTypeException(HedyException):
    def __init__(self, command, invalid_type, allowed_types, invalid_argument, line_number):
        super().__init__('Invalid Argument Type',
                         command=command,
                         invalid_type=invalid_type,
                         allowed_types=allowed_types,
                         invalid_argument=invalid_argument,
                         line_number=line_number)


class InvalidTypeCombinationException(HedyException):
    def __init__(self, command, arg1, arg2, type1, type2, line_number):
        super().__init__('Invalid Type Combination',
                         command=command,
                         invalid_argument=arg1,
                         invalid_argument_2=arg2,
                         invalid_type=type1,
                         invalid_type_2=type2,
                         line_number=line_number)


class InvalidArgumentException(HedyException):
    def __init__(self, command, allowed_types, invalid_argument, line_number):
        super().__init__('Invalid Argument',
                         command=command,
                         allowed_types=allowed_types,
                         invalid_argument=invalid_argument,
                         line_number=line_number)


class WrongLevelException(HedyException):
    def __init__(self, working_level, offending_keyword, tip, line_number):
        super().__init__('Wrong Level',
                         working_level=working_level,
                         offending_keyword=offending_keyword,
                         tip=tip,
                         line_number=line_number)


class InputTooBigException(HedyException):
    def __init__(self, lines_of_code, max_lines):
        super().__init__('Too Big',
                         lines_of_code=lines_of_code,
                         max_lines=max_lines)


class InvalidCommandException(WarningException):
    def __init__(
            self,
            level,
            invalid_command,
            guessed_command,
            line_number,
            fixed_code,
            fixed_result):
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


class MissingVariableException(HedyException):
    def __init__(self, command, level, line_number):
        super().__init__('Missing Variable',
                         command=command,
                         level=level,
                         line_number=line_number)


class InvalidAtCommandException(HedyException):
    def __init__(self, command, level, line_number):
        super().__init__('Invalid At Command',
                         command=command,
                         level=level,
                         line_number=line_number)


class IncompleteRepeatException(HedyException):
    def __init__(self, command, level, line_number):
        super().__init__('Incomplete Repeat',
                         command=command,
                         level=level,
                         line_number=line_number)


class LonelyTextException(HedyException):
    def __init__(self, level, line_number):
        super().__init__('Lonely Text',
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
    def __init__(self, level, line_number, unquotedtext=None):
        super().__init__('Unquoted Text',
                         level=level,
                         unquotedtext=unquotedtext,
                         line_number=line_number)


class MissingAdditionalCommand(HedyException):
    def __init__(self, command, missing_command, line_number):
        super().__init__('Missing Additional Command',
                         command=command,
                         missing_command=missing_command,
                         line_number=line_number)


class MisspelledAtCommand(HedyException):
    def __init__(self, command, arg1, line_number):
        super().__init__('Misspelled At Command',
                         command=command,
                         invalid_argument=arg1,
                         line_number=line_number)


class NonDecimalVariable(HedyException):
    def __init__(self, line_number):
        super().__init__('Non Decimal Variable',
                         line_number=line_number)


class UnquotedAssignTextException(HedyException):
    def __init__(self, text, line_number):
        super().__init__('Unquoted Assignment', text=text, line_number=line_number)


class MissingBracketsException(HedyException):
    def __init__(self, level, line_number):
        super().__init__('Missing Square Brackets',
                         line_number=line_number)


class LonelyEchoException(HedyException):
    def __init__(self):
        super().__init__('Lonely Echo')


class CodePlaceholdersPresentException(HedyException):
    def __init__(self, line_number):
        super().__init__('Has Blanks', line_number=line_number)


class TooManyIndentsStartLevelException(HedyException):
    def __init__(self, line_number, leading_spaces, fixed_code=None):
        super().__init__('Too Many Indents', line_number=line_number, leading_spaces=leading_spaces)
        self.fixed_code = fixed_code


class TooFewIndentsStartLevelException(HedyException):
    def __init__(self, line_number, leading_spaces, fixed_code=None):
        super().__init__('Too Few Indents', line_number=line_number, leading_spaces=leading_spaces)
        self.fixed_code = fixed_code


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


class UnsupportedStringValue(HedyException):
    def __init__(self, invalid_value):
        super().__init__('Unsupported String Value', invalid_value=invalid_value)


class MissingElseForPressitException(HedyException):
    def __init__(self, command, level, line_number):
        super().__init__('Pressit Missing Else',
                         command=command,
                         level=level,
                         line_number=line_number)


class NestedFunctionException(HedyException):
    def __init__(self):
        super().__init__('Nested Function')


class WrongNumberofArguments(HedyException):
    def __init__(self, name, defined_number, used_number, line_number):
        super().__init__('Wrong Number of Arguments',
                         name=name,
                         defined_number=defined_number,
                         used_number=used_number,
                         line_number=line_number)


class InvalidErrorSkippedException(HedyException):
    def __init__(self):
        super().__init__('Invalid Error Skipped')


class RuntimeValueException(HedyException):
    def __init__(self, command, value, tip):
        super().__init__('Runtime Value Error', command=command, value=value, tip=tip)


class RuntimeValuesException(HedyException):
    def __init__(self, command, value, tip):
        super().__init__('Runtime Values Error', command=command, value=value, tip=tip)


class RuntimeIndexException(HedyException):
    def __init__(self, name):
        super().__init__('Runtime Index Error', name=name)


class ElseWithoutIfException(HedyException):
    def __init__(self, line_number):
        super().__init__('Else Without If Error', line_number=line_number)


class MissingColonException(HedyException):
    def __init__(self, command, line_number):
        super().__init__('Missing Colon Error', command=command, line_number=line_number)


HEDY_EXCEPTIONS = {name: cls for name, cls in globals().items() if inspect.isclass(cls)}
