
import re
from base_parser import BaseParser


class Parser(BaseParser):

    def setupSettings(self):
        nameToken = '[a-zA-Z_\\x7f-\\xff][a-zA-Z0-9_\\x7f-\\xff]*'
        self.settings = {
            # curly brackets around the type information
            'curlyTypes': False,
            "typeTag": "my",
            'varIdentifier': nameToken + '(?:\.' + nameToken + ')*',
            'fnIdentifier': nameToken,
            "bool": "boolean",
            "function": "def",
            'block_start': '"""',
            'block_middle': '',
            'block_end': '"""',
            'space_after_start': False,
            'space_before_end': False,
            'insert_after_def': True
        }

    def getBlockStart(self):
        start = self.settings['blockStart']
        if self.preferences.get("natural_docs_perl_use_pod"):
            start += '\n'

        return start

    def getBlockEnd(self):
        end = self.settings['blockEnd']
        if self.preferences.get("natural_docs_perl_use_pod"):
            end = '\n' + end

        return end

    def parseFunction(self, line):
        # sub [name] [($@%&+)] {
        res = re.search(
            'def\\s+'
            + '(?P<name>' + self.settings['fnIdentifier'] + ')'
            # sub fnName
            + '\\s*\\((?P<args>.*)\):',
            # (arg1, arg2)
            line
        )

        if not res:
            return None

        return (res.group('name'), res.group('args'))
        # return (res.group('name'), ())

    def getArgType(self, arg):
        #  function add($x, $y = 1)
        res = re.search(
            '(?P<name>' + self.settings['varIdentifier'] + ")\\s*=\\s*(?P<val>.*)",
            arg
        )
        if res:
            return self.guessTypeFromValue(res.group('val'))

        #  function sum(Array $x)
        if re.search('\\S\\s', arg):
            return re.search("^(\\S+)", arg).group(1)
        else:
            return None

    def getArgName(self, arg):
        return re.search("([^=]+)", arg).group(0)

    def parseVar(self, line):
        res = re.search(
            #   var $foo = blah,
            #       $foo = blah;
            #   $baz->foo = blah;
            #   $baz = array(
            #        'foo' => blah
            #   )

            '(?P<name>' + self.settings['varIdentifier'] + ')\\s*=>?\\s*(?P<val>.*?)(?:[;,]|$)',
            line
        )
        if res:
            return (res.group('name'), res.group('val').strip())

        res = re.search(
            '\\b(?:var|public|private|protected|static)\\s+(?P<name>' + self.settings['varIdentifier'] + ')',
            line
        )
        if res:
            return (res.group('name'), None)

        return None

    def guessTypeFromValue(self, val):
        if self.is_numeric(val):
            return "float" if '.' in val else "integer"
        if val[0] == '"' or val[0] == "'":
            return "string"
        if val[:5] == 'array':
            return "array"
        if val.lower() in ('true', 'false', 'filenotfound'):
            return 'boolean'
        if val[:4] == 'new ':
            res = re.search('new (' + self.settings['fnIdentifier'] + ')', val)
            return res and res.group(1) or None
        return None

    def getFunctionReturnType(self, name):
        if (name[:2] == '__'):
            if name in ('__construct', '__set', '__unset', '__wakeup'):
                return None
            if name == '__sleep':
                return 'array'
            if name == '__toString':
                return 'string'
            if name == '__isset':
                return 'boolean'
        return super(Parser, self).getFunctionReturnType(name)
