
import re
from base_parser import BaseParser


class Parser(BaseParser):

    CONSTRUCTOR_TYPE = 3

    def setupSettings(self):
        self.settings = {
            'typeTag': 'type',
            # technically, they can contain all sorts of unicode, but whatever
            'varIdentifier': '[a-zA-Z][a-zA-Z_0-9]*',
            'fnIdentifier': '[a-zA-Z][a-zA-Z_0-9]*',
            'classIdentifier': '[a-zA-Z][a-zA-Z_0-9]*',
            # this will mess up if the generics have spaces:
            'type_specifier': '[\w\[\]\.]+(\<[\w\,\.\[\] ]+\>)?',
            'function_name': 'Method',
            'block_start': '/**',
            'block_middle': ' * ',
            'block_end': '*/',
        }

    def parseClass(self, line):
        # public class ArticlesDAO extends TableDAO {
        res = re.search(
            # Declaration
            'class'
            # Identifier
            + '\\s+(?P<name>' + self.settings['classIdentifier'] + ')'
            # Extends (optional)
            + '(\\s+extends\\s+)?(?P<extends>' + self.settings['classIdentifier'] + ')?'
            # Implements (optional)
            + '(\\s+implements\\s+)?(?P<implements>(' + self.settings['classIdentifier'] + ',?\s*)+)?',
            line
        )

        if res:
            return (res.group('name'), res.group('extends'), res.group('implements'))

        return None

    def parseFunction(self, line):
        res = re.search(
            # Modifier
            '(public|private|protected|static|final|native|synchronized|abstract|threadsafe|transient)+'
            # Type. Constructor has no type.
            + '\s+(?P<return>' + self.settings['type_specifier'] + ')?'
            # Identifier
            + '(?:\s+(?P<name>' + self.settings['fnIdentifier'] + '))?'
            # Parameter list
            + '\s*\((?P<args>.*)\)',
            line
        )

        if not res:
            return None

        # grab the name out of "name1 = function name2(foo)" preferring name1
        return_type = res.group('return')
        name = res.group('name')
        args = res.group('args')

        if return_type is not None and name is None:
            # Constructors do not have types, we need to flip these results
            name = return_type
            return_type = self.CONSTRUCTOR_TYPE

        if return_type == 'void':
            return_type = self.NO_RETURN_TYPE

        return (name, args, return_type)

    def parseVar(self, line):
        res = re.search(
            #   <Type> foo = blah;
            #   baz.foo = blah;
            '(?P<name>' + self.settings['varIdentifier'] + ')\s*[=]\s*(?P<val>.*?)(?:[;,]|$)',
            line
        )

        if not res:
            return None

        return (res.group('name'), res.group('val').strip())

    def parseArgs(self, args):
        """ an array of tuples, the first being the best guess at the type, the second being the name """
        out = []

        # fancy foot work to deal with generics
        # TODO: figure out a better way to do this
        for arg in re.split('\s*,\s*', args):
            arg = arg.strip()
            if arg.find('>') > -1 and arg.find('<') <= -1:
                previous_arg = out[-1]
                current_arg = re.split('\s+', arg)
                previous_arg[0] += ',' + current_arg[0]
                previous_arg.append(current_arg[1])
                out[-1] = previous_arg
            else:
                out.append(re.split('\s+', arg))

        return out

    def formatFunction(self, name, args, return_type=None):
        """
        Override BaseParser to change Method to Constructor where applicable
        """
        out = super(Parser, self).formatFunction(name, args, return_type)

        # all methods must have a return type specified, therefore if there
        # BaseParser did not find a return type this must be a constructor
        if return_type is self.CONSTRUCTOR_TYPE:
            out[0] = out[0].replace('Method: ', 'Constructor: ')
            out = out[:-2]

        return out
