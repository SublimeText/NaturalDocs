NaturalDocs is a [Sublime Text 2](http://www.sublimetext.com/) package which makes writing [NaturalDocs](http://www.naturaldocs.org) easy. Based on [DocBlockr](https://github.com/spadgos/sublime-jsdocs) by [Nick Fisher](https://github.com/spadgos), influenced by [Germán M. Bravo](https://github.com/Kronuz)'s [SublimeLinter](https://github.com/Kronuz/SublimeLinter).

# Languages

Currently supported languages: Perl, JavaScript, PHP, and Python.

# Usage

The easiest way to use this plugin is to put the cursor near what you want to document and press `Super-N`.

## Autocomplete Comments

If you start a comment block (e.g. `/*`, `/**`, `/*!`) and press enter, it will complete the block and put your cursor in the middle. Subsequently, pressing enter inside a block will create a new line continuing the comment block.

`/**|` -> `Enter`

Results in

```
/**
 * |
 */
```

The above pipe represents the cursor. Pressing `Enter` again will result in this:

```
/**
 *
 * |
 */
```

If you happened to start a block before a function, it would populate the block with the function information.

```
/** |
function testThis($one, $two) {}
```

Results in:

```
/**
 * Function: testThis
 *
 * |description
 *
 * Parameters:
 *
 *   $one - [type/description]
 *   $two - [type/description]
 *
 * Returns:
 *
 *    return description
 */
function testThis($one, $two) {}
```

**Single-line Comments**

Additionally, if you start a single-line comment (e.g. `//` or `#`), pressing `Enter` will continue the comment block on the next line. You can press `Shift-Enter` to just go to a blank line.


## Decorations

You can add decoration blocks by pressing `Ctrl-Enter`.

Examples in JavaScript:

```javascript
// this is a pretty item |
```

Results in:

```javascript
///////////////////////////
// this is a pretty item //
///////////////////////////

Examples in Perl:

```perl
# this is a pretty item |
```

Results in:

```perl
#########################
# this is a pretty item #
#########################
```

## Language Specific Examples

### Perl Example

Code:

```perl
sub index {
```

Put cursor on or before the line and pressing `Super-N` will result in:

```perl
=begin ND

Function: index

description

Returns:

   return description

=cut
sub index {
```

### JavaScript Example

Code:

```javascript
function testThis($one, $two, $three) {}
```

Put cursor on or before the line and pressing `Super-N` will result in:

```javascript
/**
 * Function: testThis
 *
 * description
 *
 * Parameters:
 *
 *   $one   - [type/description]
 *   $two   - [type/description]
 *   $three - [type/description]
 *
 * Returns:
 *
 *    return description
 */
function testThis($one, $two, $three) {}
```

### PHP Example

Code:

```php
<?php
function testThis($one='', $two=true, $three=array()) {}
```

Put cursor on or before the line and pressing `Super-N` will result in:

```php
<?php
/**
 * Function: testThis
 *
 * description
 *
 * Parameters:
 *
 *   $one   - string
 *   $two   - boolean
 *   $three - array
 *
 * Returns:
 *
 *    return description
 */
function testThis($one='', $two=true, $three=array()) {}
```

### Python Example

Code:

```python
def test_test(one, two=12, three=[]):
    return 'yes'
```

Put cursor on or /after/ the line and pressing `Super-N` will result in:

```python
def test_test(one, two=12, three='something'):
    """
    Function: test_test

    description

    Parameters:

      one   - [type/description]
      two   - integer
      three - string

    Returns:

       return description
    """
    return 'yes'
```


# Commands

* NaturalDocsCommand
* NaturalDocsInsertBlock
* NaturalDocsIndentCommand
* NaturalDocsJoinCommand
* NaturalDocsDecorateCommand

# Settings

## natural_docs_deep_indent

*To Be Done & Documented*

## natural_docs_continue_comments

If this setting is set to `True`, then pressing `Enter` on a line with a double-slash or number-sign comment will place that comment punctuation at the beginning of the next line.

Example:
```javascript
// hello |
```

Translates to

```javascript
// hello
// |
```

## natural_docs_indentation_spaces

The number of spaces to insert after the comment punctuation. Example if set to one:

```
/**
 * Function: <functionName>
```

Example if set to five:

```
/**
 *     Function: <functionName>
```

Defaults to one.

## natural_docs_spacer_between_sections

If set to `true` will added extra lines between sections in docblock. For example:

```
/**
 * Function: <functionName>
 *
 * [description]
 *
 * Parameters:
 *
 *    foo - [description]
 *    bar - [description]
 *
 * Returns:
 *
 *    [description]
 */
```

If set to `false` will make the docblock more compact. Example:

```
/**
 * Function: <functionName>
 * [description]
 * Parameters:
 *    foo - [description]
 *    bar - [description]
 * Returns:
 *    [description]
 */
```


## natural_docs_perl_use_pod

If set to `true` will use POD-style comments instead of using Perl number-sign comments. Example:

```perl
=begin ND

Function: <functionName>

[description]

Parameters:

   foo - [description]
   bar - [description]

 Returns:

   [description]

=cut
```

If set to `false`, the normal comment tag will be used. Example:

```perl
#
# Function: <functionName>
#
# [description]
#
# Parameters:
#
#    foo - [description]
#    bar - [description]
#
#  Returns:
#
#    [description]
#
```

# Todo

* Add shortcuts for inserting [NaturalDoc Group](http://www.naturaldocs.org/documenting/reference.html#Summaries) blocks
* Add more languages (C/C++, Ruby)
* Make awesomer

# Changelog

## March 21, 2012

* Add Decorations for Perl & Python
* Added the ability to add Class/Package doc-blocks
* Changed setting `natural_docs_extend_double_slash` to `natural_docs_continue_comments`
* Added keymappings to continue number-sign comments if `natural_docs_continue_comments` is `True`