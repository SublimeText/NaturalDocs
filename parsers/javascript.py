
import re
from base_parser import BaseParser


class Parser(BaseParser):
    def setupSettings(self):
        self.settings = {
            "typeTag": "type",
            # technically, they can contain all sorts of unicode, but w/e
            "varIdentifier": '[a-zA-Z_$][a-zA-Z_$0-9]*',
            "fnIdentifier": '[a-zA-Z_$][a-zA-Z_$0-9]*',
            "bool": "Boolean",
            "function": "Function",
            'block_start': '/**',
            'block_middle': ' * ',
            'block_end': '*/'
        }

    def parseFunction(self, line):
        res = re.search(
            #   fnName = function,  fnName : function
            '(?:(?P<name1>' + self.settings['varIdentifier'] + ')\s*[:=]\s*)?'
            + 'function'
            # function fnName
            + '(?:\s+(?P<name2>' + self.settings['fnIdentifier'] + '))?'
            # (arg1, arg2)
            + '\s*\((?P<args>.*)\)',
            line
        )
        if not res:
            return None

        # grab the name out of "name1 = function name2(foo)" preferring name1
        name = self.escape(res.group('name1') or res.group('name2') or '')
        args = res.group('args')

        return (name, args)

    def parseVar(self, line):
        res = re.search(
            #   var foo = blah,
            #       foo = blah;
            #   baz.foo = blah;
            #   baz = {
            #        foo : blah
            #   }

            '(?P<name>' + self.settings['varIdentifier'] + ')\s*[=:]\s*(?P<val>.*?)(?:[;,]|$)',
            line
        )
        if not res:
            return None

        return (res.group('name'), res.group('val').strip())

    def guessTypeFromValue(self, val):
        if self.is_numeric(val):
            return "Number"
        if val[0] == '"' or val[0] == "'":
            return "String"
        if val[0] == '[':
            return "Array"
        if val[0] == '{':
            return "Object"
        if val == 'true' or val == 'false':
            return 'Boolean'
        if re.match('RegExp\\b|\\/[^\\/]', val):
            return 'RegExp'
        if val[:4] == 'new ':
            res = re.search('new (' + self.settings['fnIdentifier'] + ')', val)
            return res and res.group(1) or None
        return None
