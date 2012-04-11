
import re
from base_parser import BaseParser


class Parser(BaseParser):

    def setup_settings(self):
        nameToken = '[a-zA-Z_\\x7f-\\xff][a-zA-Z0-9_\\x7f-\\xff]*'
        self.settings = {
            'typeTag': 'my',
            'varIdentifier': '[$]' + nameToken + '(?:->' + nameToken + ')*',
            'fnIdentifier': nameToken,
            'classIdentifier': nameToken + '(::' + nameToken + ')*',
            'class_name': 'Package',
            'bool': 'boolean',
            'function': 'sub',
            'block_start': '#',
            'block_middle': '# ',
            'block_end': '#',
        }

        if self.preferences.get('natural_docs_perl_use_pod'):
            self.settings['block_start'] = '=begin ND'
            self.settings['block_middle'] = ''
            self.settings['block_end'] = '=cut'
            self.settings['space_after_start'] = True
            self.settings['space_before_end'] = True

    def parse_class(self, line):
        res = re.search(
            'package\\s+(?P<name>' + self.settings['classIdentifier'] + ');',
            line
        )

        if res:
            return (res.group('name'), ())

        return None

    def parse_function(self, line):
        # sub [name] [($@%&+)] {
        res = re.search(
            # Declaration
            'sub\\s+'
            # Identifier
            + '(?P<name>' + self.settings['fnIdentifier'] + ')'
            # Parameter list
            + '\\s*\(?(?P<args>[$@%&]+)?\)?'
            # Block Starter
            + '\\s*{',
            line
        )

        if not res:
            return None

        return (res.group('name'), res.group('args'))

    def parse_args(self, args):
        """ an array of tuples, the first being the best guess at the type, the second being the name """
        out = []
        for arg in list(args):
            arg = arg.strip()
            out.append((self.get_arg_type(arg), self.get_arg_name(arg)))
        return out

    def get_arg_type(self, arg):
        types = {
            '$': 'scalar',
            '@': 'array',
            '%': 'hash',
            '&': 'reference'
        }

        return types[arg]

    def get_arg_name(self, arg):
        # return re.search("(\\S+)(?:\\s*=.*)?$", arg).group(1)
        return self.get_arg_type(arg)

    def parse_var(self, line):
        res = re.search(
            #   var $foo = blah,
            #       $foo = blah;
            #   $baz->foo = blah;
            #   $baz = [\{\[]
            #        'foo' => blah
            #   [\}\]]

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
