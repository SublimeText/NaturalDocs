
import re
from base_parser import BaseParser


class Parser(BaseParser):

    def setup_settings(self):
        self.settings = {
            # technically, they can contain all sorts of unicode, but w/e
            'varIdentifier': '[a-zA-Z_$][a-zA-Z_$0-9]*',
            'fnIdentifier': '[a-zA-Z_$][a-zA-Z_$0-9]*',
            'classIdentifier': '[a-zA-Z_$][a-zA-Z_$0-9]*',
            'bool': 'Boolean',
            'block_start': '#',
            'block_middle': '# ',
            'block_end': '#'
        }

    def parse_class(self, line):
        res = re.search(
            # declartions
            'class\\s+'
            # identifer
            + '(?P<name>{0})'.format(self.settings['classIdentifier'])
            # optional. extends identifer
            + '(\\s+extends\\s+(?P<extends>{0}))?'.format(self.settings['classIdentifier']),
            line
        )

        if res:
            return (res.group('name'), res.group('extends'))

        return None

    def parse_function(self, line):
        """
        Function: parse_function

          Parses CoffeeScript funtions
          Not sure if we should break methods/functions to seperate parsers.

        Examples:

          square = (x) -> x * x
          race = (winner, runners...) ->
          fill = (container, liquid = "coffee") ->
          Account = (customer, cart) ->
          $('.shopping_cart').bind 'click', (event) =>
          @method: ->
          @betterMethod: =>

        Parameters:

          self - Class instance
          line - The line containing the function

        Returns:

          Array containing all the important parts
        """

        res = re.search(
            # identifier
            '(?P<name>{0})\s*'.format(self.settings['varIdentifier'])
            # assignment / property
            + '[:=]\s*'
            # arguments
            + '(\((?P<args>.*)\))?\s*'
            # declaration
            + '[\-=]>',
            line
        )

        if not res:
            # this might be an closure
            res = re.search(
                # arguments
                '(\((?P<args>.*)\))?\s*'
                # declaration
                + '[\-=]>',
                line
            )

            if not res:
                return None

            return ('Anonymous', res.group('args'))

        name = self.escape(res.group('name') or '')
        args = res.group('args')

        return (name, args)

    def get_arg_name(self, arg):
        name = re.search("([^=]+)", arg).group(0)
        name = name.replace('...', '')
        return name

    def get_arg_type(self, arg):
        #  function add($x, $y = 1)
        res = re.search(
            '(?P<name>{0})\\s*=\\s*(?P<val>.*)'.format(self.settings['varIdentifier']),
            arg
        )

        if not res:
            # check for a splat
            res = re.search(
                '(?P<name>{0})(?P<val>\.\.\.)'.format(self.settings['varIdentifier']),
                arg
            )

        if not res:
            return None

        return self.guess_type_from_value(res.group('val'))

    def parse_var(self, line):
        res = re.search(
            # foo = blah
            '(?P<name>{0})\s*[=:]\s*'.format(self.settings['varIdentifier']),
            line
        )

        if not res:
            return None

        return (res.group('name'), res.group('val').strip())

    def guess_type_from_value(self, val):
        type = None

        if val == '...':
            return 'Splat. '
        if self.is_numeric(val):
            type = 'Number'
        if val[0] == '"' or val[0] == "'":
            type = 'String'
        if val[0] == '[':
            type = 'Array'
        if val[0] == '{':
            type = 'Object'
        if val == 'true' or val == 'false' or val == 'on' or val == 'off':
            type = 'Boolean'
        if re.match('RegExp\\b|\\/[^\\/]', val):
            type = 'RegExp'
        if val[:4] == 'new ':
            res = re.search('new (' + self.settings['fnIdentifier'] + ')', val)
            type = res and res.group(1) or None

        if type:
            return '{0}. Defaults to {1}'.format(type, val)

        return None
