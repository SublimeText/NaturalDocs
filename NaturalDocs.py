"""
NaturalDocs
by: Nathan Levin-Greenhaw (njlg)
site: https://github.com/SublimeText/NaturalDocs

Based on DocBlockr by Nick Fisher (https://github.com/spadgos/sublime-jsdocs)
"""
import sublime_plugin
import re
import os
import sys

path = os.path.abspath(os.path.dirname(__file__))
if path not in sys.path:
    sys.path.insert(0, path)


def read_line(view, point):
    if (point >= view.size()):
        return

    next_line = view.line(point)
    return view.substr(next_line)


def write(view, str):
    view.run_command('insert_snippet', {'contents': str})


def counter():
    count = 0
    while True:
        count += 1
        yield(count)


def get_parser(view):
    scope = view.scope_name(view.sel()[0].end())
    preferences = view.settings()

    res = re.search('source\\.(?P<source>\w+)', scope)
    if not res:
        module = __import__('parsers.javascript', fromlist=['parsers'])
        return module.Parser(preferences)

    source = res.group('source')
    if source == 'js':
        source = 'javascript'

    try:
        module = __import__('parsers.%s' % source, fromlist=['parsers'])
    except ImportError:
        module = __import__('parsers.javascript', fromlist=['parsers'])

    return module.Parser(preferences)


class NaturalDocsCommand(sublime_plugin.TextCommand):

    def run(self, edit, definition='', inline=False):
        v = self.view

        settings = v.settings()
        point = v.sel()[0].end()

        parser = get_parser(v)
        parser.inline = inline

        indentSpaces = max(0, settings.get('natural_docs_indentation_spaces', 1))
        first = "\n" + parser.block_middle + (" " * (1 - indentSpaces))
        prefix = "\n" + parser.block_middle.lstrip() + (" " * (1 - indentSpaces))

        # read the current line if it did not get passed in
        line = ''
        if definition:
            line = definition
        else:
            line = read_line(v, point)

            if line is None:
                # there is no line beneath the cursor (e.g. EOF)
                v.run_command("insert", {"characters": "\n"})
                v.run_command("move", {"by": "lines", "forward": False})
                line = read_line(v, point)

            if parser.insert_after_def:
                # move cursor below current line
                v.run_command("move", {"by": "lines", "forward": True})
                v.run_command("move_to", {"to": "bol", "extend": False})
                v.run_command("insert", {"characters": "\n"})
                v.run_command("move", {"by": "lines", "forward": False})

        if re.search(re.escape(parser.block_start), line) is None:
            start = parser.block_start
            if parser.space_after_start:
                start += first
                first = prefix
            write(v, start)

        elif parser.space_after_start:
            write(v, first)
            first = prefix

        if not definition:
            # read the line after we inserted the doc block
            point = v.sel()[0].end()
            line = read_line(v, point + 1)

        out = None

        # if there is a line following this
        if line:
            if parser.is_existing_comment(line):
                write(v, "\n" + parser.block_middle + (" " * (1 - indentSpaces)))
                return
            # match against a function declaration.
            out = parser.parse(line)

        # fix all the tab stops so they're consecutive
        if out:
            tabIndex = counter()

            def swapTabs(m):
                return "%s%d%s" % (m.group(1), tabIndex.next(), m.group(2))

            for index, outputLine in enumerate(out):
                out[index] = re.sub("(\\$\\{)\\d+(:[^}]+\\})", swapTabs, outputLine)

        # prepare the end block tag
        end = '\n' + parser.block_end
        if parser.space_before_end:
            end = prefix + end

        if inline:
            if out:
                write(v, out[0] + end)
            else:
                write(v, "$0" + end)
        else:
            # write the first linebreak and star. this sets the indentation for the following snippets
            write(v, first)

            if out:
                if settings.get('natural_docs_spacer_between_sections'):

                    newOut = []
                    for idx, line in enumerate(out):
                        newOut.append(line)
                        res = re.match("^\S", line)

                        # add space after this section, only if it is not the last
                        # thing in this section
                        if res and len(out) - 1 != idx:
                            newOut.append("")

                    write(v, prefix.join(newOut) + end)

                else:
                    write(v, prefix.join(out) + end)

            else:
                write(v, "$0" + end)


class NaturalDocsInsertBlock(sublime_plugin.TextCommand):
    """
    This tries to start a Doc Block where one does not already exist
    """

    def run(self, edit):
        v = self.view

        parser = get_parser(v)

        # are one on the line or above it?
        point = v.sel()[0].begin()
        line_point = v.full_line(point)
        current_line = v.substr(line_point)

        if len(current_line.strip()) > 0:
            # cursor is on the function definition
            if parser.insert_after_def:
                # position the cursor inside the function
                v.run_command("move", {"by": "lines", "forward": True})
                v.run_command("move_to", {"to": "bol", "extend": False})
                v.run_command("insert", {"characters": "\n"})
                v.run_command("move", {"by": "lines", "forward": False})
                # should we verify tabs are correct???
            else:
                # move the function down to begin our block
                v.run_command("move_to", {"to": "bol", "extend": False})
                v.run_command("insert", {"characters": "\n"})
                v.run_command("move", {"by": "lines", "forward": False})

        elif parser.insert_after_def:
            col = v.rowcol(v.sel()[0].begin())[1]
            point = v.sel()[0].end() - (col + 1)
            line_point = v.full_line(point)
            current_line = v.substr(line_point)
        else:
            point = v.sel()[0].end() + 1
            line_point = v.full_line(point)
            current_line = v.substr(line_point)

        v.run_command("natural_docs", {'definition': current_line})
        return


class NaturalDocsIndentCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        v = self.view
        current_position = v.sel()[0].begin()
        current_line_region = v.line(current_position)
        current_column = current_position - current_line_region.begin()  # which column we're currently in
        previous_line = v.substr(v.line(v.line(current_position).begin() - 1))

        if previous_line.find(' - ') > -1:
            column = previous_line.find(' - ') + 3
            spaces_to_insert = column - current_column

            if spaces_to_insert > 0:
                v.insert(edit, current_position, " " * spaces_to_insert)
                return

        # default to inserting an indent
        # TODO: make default docblock indent a preference? per source type?
        v.insert(edit, current_position, "  ")


class NaturalDocsJoinCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        v = self.view
        for sel in v.sel():
            for lineRegion in reversed(v.lines(sel)):
                v.replace(edit, v.find("[ \\t]*\\n[ \\t]*(\\*[ \\t]*)?", lineRegion.begin()), ' ')


class NaturalDocsDecorateCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        v = self.view

        punctuation = ''
        re_whitespace = ''
        punctuation_end = ''

        if v.scope_name(v.sel()[0].a).find('comment.line.number-sign') > 0:
            punctuation = '#'
            punctuation_end = '#'
            re_whitespace = re.compile("^(\\s*)#")
        elif v.scope_name(v.sel()[0].a).find('comment.line.double-slash') > 0:
            punctuation = '/'
            punctuation_end = '//'
            re_whitespace = re.compile("^(\\s*)//")
        else:
            print 'NaturalDocs: Cannot decorate this line.'
            return

        endLength = len(punctuation_end) + 1
        v.run_command('expand_selection', {'to': 'scope'})

        for sel in v.sel():
            maxLength = 0
            lines = v.lines(sel)

            for lineRegion in lines:
                leadingWS = re_whitespace.match(v.substr(lineRegion)).group(1)
                maxLength = max(maxLength, lineRegion.size())

            lineLength = maxLength - len(leadingWS)
            v.insert(edit, sel.end(), leadingWS + punctuation * (lineLength + endLength) + "\n")

            for lineRegion in reversed(lines):
                line = v.substr(lineRegion)
                rPadding = 1 + (maxLength - lineRegion.size())
                v.replace(edit, lineRegion, leadingWS + line + (" " * rPadding) + punctuation_end)
                # break

            v.insert(edit, sel.begin(), punctuation * (lineLength + endLength) + "\n")


class NaturalDocsGroupCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        v = self.view

        parser = get_parser(v)

        block_start = parser.block_start
        block_end = parser.block_end
        block_middle = parser.block_middle

        block = block_start + '\n'

        if parser.space_after_start:
            block += '\n'

        block += block_middle + 'Group: \n'

        if parser.space_before_end:
            block += '\n'

        block += block_end

        for sel in v.sel():
            lines = v.lines(sel)
            for line_region in lines:
                # step 1 - move anything on the line down
                current_line = v.substr(line_region)
                if current_line.strip():
                    v.run_command("move_to", {"to": "bol", "extend": False})
                    v.run_command("insert", {"characters": "\n"})
                    v.run_command("move", {"by": "lines", "forward": False})

                # keep whitespace
                whitespace = re.match('^\s+', current_line).group(0)
                doc_block = block.replace('\n', '\n' + whitespace)

                # step 2 - insert group block
                v.insert(edit, line_region.end(), doc_block)

        # step 3 - position cursor after group label
        v.run_command("move", {"by": "lines", "forward": False})

        if parser.space_before_end:
            v.run_command("move", {"by": "lines", "forward": False})

        v.run_command("move_to", {"to": "eol", "extend": False})
