
import re
import string


class BaseParser(object):

    NO_RETURN_TYPE = 1  # e.g. void
    UNKNOWN_RETURN_TYPE = 2  # e.g. add Returns section with no type

    def __init__(self, preferences={}):
        self.preferences = preferences
        self.setupSettings()

    def setupSettings(self):
        self.settings = {}
        return self.settings

    def getSettings(self):
        return self.settings

    def isExistingComment(self, line):
        return re.search('^\\s*\\*', line)

    def parse(self, line):
        out = self.parseClass(line)  # (name, extends)
        if out:
            return self.formatClass(*out)

        out = self.parseFunction(line)  # (name, args)
        if out:
            return self.formatFunction(*out)

        out = self.parseVar(line)
        if out:
            return self.formatVar(*out)

        return None

    def parseClass(self, line):
        return None

    def parseFunction(self, line):
        return None

    def parseVar(self, line):
        return None

    def escape(self, str):
        return string.replace(str, '$', '\$')

    def formatClass(self, name, base=None, interface=None):
        out = []

        classname = 'Class'
        if 'classname' in self.settings:
            classname = self.settings['classname']

        out.append("%s: %s" % (classname, name))
        out.append("${1:[%s description]}" % (self.escape(name)))

        if base:
            out.append("Extends: %s" % base)

        if interface:
            out.append("Implements: %s" % interface)

        return out

    def formatVar(self, name, val):
        out = []

        out.append("Variable: %s" % name)
        if self.inline == False:
            out.append("${1:[%s description]}" % (self.escape(name)))

        return out

    def formatFunction(self, name, args, return_type=None):
        out = []

        function_name = 'Function'
        if 'function_name' in self.settings:
            function_name = self.settings['function_name']

        out.append("%s: %s" % (function_name, name))
        out.append("${1:description}")

        self.addExtraTags(out)

        # if there are arguments, add a Parameter section for each
        if args:
            # remove comments inside the argument list.
            # args = re.sub("/\*.*?\*/", '', args)
            out.append("Parameters:")
            params = []

            for arg in self.parseArgs(args):
                description = '[type/description]'
                if arg[0]:
                    description = arg[0]

                params.append("  %s - ${1:%s}" % (self.escape(arg[1]), description))

            out.extend(self.alignParameters(params))

            # add extra line after parameters?
            if self.preferences.get("natural_docs_spacer_between_sections"):
                out.append("")

        if return_type is None:
            return_type = self.getFunctionReturnType(name)

        if return_type is not None and return_type is not self.NO_RETURN_TYPE:
            out.append("Returns:")

            if return_type is not self.UNKNOWN_RETURN_TYPE:
                out.append("  %s - ${1:return description}" % (return_type))
            else:
                out.append("  ${1:return description}")

        return out

    def alignParameters(self, params):
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

    def getFunctionReturnType(self, name):
        """ returns None for no return type. False meaning unknown, or a string """
        return self.UNKNOWN_RETURN_TYPE

    def parseArgs(self, args):
        """ an array of tuples, the first being the best guess at the type, the second being the name """
        out = []
        for arg in re.split('\s*,\s*', args):
            arg = arg.strip()
            out.append((self.getArgType(arg), self.getArgName(arg)))
        return out

    def getArgType(self, arg):
        return None

    def getArgName(self, arg):
        return arg

    def addExtraTags(self, out):
        extraTags = self.preferences.get('natural_docs_extra_tags', [])
        if (len(extraTags) > 0):
            out.extend(extraTags)

    def guessTypeFromName(self, name):
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
