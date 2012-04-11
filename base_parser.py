
import re
import string


class BaseParser(object):

    NO_RETURN_TYPE = 1  # e.g. void
    UNKNOWN_RETURN_TYPE = 2  # e.g. add Returns section with no type

    def __init__(self, preferences={}):
        self.preferences = preferences
        self.default_settings = {
            'class_name': 'Class',
            'function_name': 'Function',
            'block_start': '',
            'block_middle': '',
            'block_end': ''
        }
        self.setup_settings()

    def setup_settings(self):
        self.settings = {}
        return self.settings

    def get_settings(self):
        return self.settings

    def __getattr__(self, name):
        if name in self.settings:
            return self.settings[name]

        if name in self.default_settings:
            return self.default_settings[name]

        return None

    def is_existing_comment(self, line):
        return re.search('^\\s*\\*', line)

    def parse(self, line):
        out = self.parse_class(line)  # (name, extends)
        if out:
            return self.format_class(*out)

        out = self.parse_function(line)  # (name, args)
        if out:
            return self.format_function(*out)

        out = self.parse_var(line)
        if out:
            return self.format_var(*out)

        return None

    def parse_class(self, line):
        return None

    def parse_function(self, line):
        return None

    def parse_var(self, line):
        return None

    def escape(self, str):
        return string.replace(str, '$', '\$')

    def format_class(self, name, base=None, interface=None):
        out = []

        class_name = self.class_name

        out.append("%s: %s" % (class_name, name))
        out.append("${1:[%s description]}" % (self.escape(name)))

        if base:
            out.append("Extends: %s" % base)

        if interface:
            out.append("Implements: %s" % interface)

        return out

    def format_var(self, name, val):
        out = []

        out.append("Variable: %s" % name)
        if self.inline == False:
            out.append("${1:[%s description]}" % (self.escape(name)))

        return out

    def format_function(self, name, args, return_type=None):
        out = []
        function_name = self.function_name

        out.append("%s: %s" % (function_name, name))
        out.append("${1:description}")

        self.add_extra_tags(out)

        # if there are arguments, add a Parameter section for each
        if args:
            # remove comments inside the argument list.
            # args = re.sub("/\*.*?\*/", '', args)
            out.append("Parameters:")
            params = []

            for arg in self.parse_args(args):
                description = '[type/description]'
                if arg[0]:
                    description = arg[0]

                params.append("  %s - ${1:%s}" % (self.escape(arg[1]), description))

            out.extend(self.align_parameters(params))

            # add extra line after parameters?
            if self.preferences.get("natural_docs_spacer_between_sections"):
                out.append("")

        if return_type is None:
            return_type = self.get_function_return_type(name)

        if return_type is not None and return_type is not self.NO_RETURN_TYPE:
            out.append("Returns:")

            if return_type is not self.UNKNOWN_RETURN_TYPE:
                out.append("  %s - ${1:return description}" % (return_type))
            else:
                out.append("  ${1:return description}")

        return out

    def align_parameters(self, params):
        columnWidth = 0

        # discover the first column width
        for param in params:
            first = param.split(" - ")[0]
            if len(first) > columnWidth:
                columnWidth = len(first)

        # adjust each parameter line with the new column width
        newParams = []
        for param in params:
            (first, second) = param.split(" - ")
            extra = columnWidth - len(first)
            newParams.append(first + (" " * extra) + " - " + second)

        return newParams

    def get_function_return_type(self, name):
        """ returns None for no return type. False meaning unknown, or a string """
        return self.UNKNOWN_RETURN_TYPE

    def parse_args(self, args):
        """ an array of tuples, the first being the best guess at the type, the second being the name """
        out = []
        for arg in re.split('\s*,\s*', args):
            arg = arg.strip()
            out.append((self.get_arg_type(arg), self.get_arg_name(arg)))
        return out

    def get_arg_type(self, arg):
        return None

    def get_arg_name(self, arg):
        return arg

    def add_extra_tags(self, out):
        extraTags = self.preferences.get('natural_docs_extra_tags', [])
        if (len(extraTags) > 0):
            out.extend(extraTags)

    def guess_type_from_name(self, name):
        name = re.sub("^[$_]", "", name)
        hungarian_map = self.preferences.get('natural_docs_notation_map', [])
        if len(hungarian_map):
            for rule in hungarian_map:
                matched = False
                if 'prefix' in rule:
                    matched = re.match(rule['prefix'] + "[A-Z_]", name)
                elif 'regex' in rule:
                    matched = re.search(rule['regex'], name)

                if matched:

                    return self.settings[rule['type']] if rule['type'] in self.settings else rule['type']

        if (re.match("(?:is|has)[A-Z_]", name)):
            return self.settings['bool']

        if (re.match("^(?:cb|callback|done|next|fn)$", name)):
            return self.settings['function']

        return False

    def is_numeric(self, val):
        try:
            float(val)
            return True
        except ValueError:
            return False
