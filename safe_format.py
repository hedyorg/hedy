from string import Formatter


def safe_format(s: str, /, **kwargs):
    """A replacement for str.format() that does NOT explode if values are missing from kwargs."""
    return FORMATTER.format(s, **kwargs)


class SafeFormatter(Formatter):
    def get_value(self, field_name, args, kwargs):
        if field_name not in kwargs:
            return '{' + field_name + '}'
        return super().get_value(field_name, args, kwargs)


FORMATTER = SafeFormatter()
