NaturalDocs is a [Sublime Text 2](http://www.sublimetext.com/) package which makes writing [NaturalDocs](http://www.naturaldocs.org) easy. Based on [DocBlockr](https://github.com/spadgos/sublime-jsdocs) by [Nick Fisher](https://github.com/spadgos), influenced by [Germán M. Bravo](https://github.com/Kronuz)'s [SublimeLinter](https://github.com/Kronuz/SublimeLinter).

# Languages

Currently supported languages: CoffeeScript, Java, JavaScript, Perl, PHP, and Python.

# Usage

The easiest way to use this plugin is to put the cursor near what you want to document and press `Super+N` (or `Super+Alt+N` for OSX).

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
```

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

### CoffeeScript Examples

#### Class Examples

Example:

```coffeescript
class Animal
```

Result:

```coffeescript
#
# Class: Animal
#
# [Animal description]
#
class Animal
```

Example:

```coffeescript
class Snake extends Animal
```

Result:

```coffeescript
#
# Class: Snake
#
# [Snake description]
#
# Extends: Animal
#
class Snake extends Animal
```

#### Function Examples

Example:

```coffeescript
square = (x) -> x * x
```

Result:

```coffeescript
#
# Function: square
#
# description
#
# Parameters:
#
#   x - [type/description]
#
# Returns:
#
#   return description
#
square = (x) -> x * x
```

Example:

```coffeescript
race = (winner, runners...) ->
```

Result:

```coffeescript
#
# Function: race
#
# description
#
# Parameters:
#
#   winner  - [type/description]
#   runners - Splat.
#
# Returns:
#
#   return description
#
race = (winner, runners...) ->
```

Example:

```coffeescript
fill = (container, liquid = "coffee") ->
```

Result:

```coffeescript
#
# Function: fill
#
# description
#
# Parameters:
#
#   container - [type/description]
#   liquid    - String. Defaults to "coffee"
#
# Returns:
#
#   return description
#
fill = (container, liquid = "coffee") ->
```

### Java Example

Class:

```java
public class MyClass extends BaseClass implements ClassA, ClassB { ... }
```

Put cursor on or before the line and pressing `Super+N` will result in:

```java
/**
 * Class: MyClass
 *
 * [MyClass description]
 *
 * Extends: BaseClass
 *
 * Implements: ClassA, ClassB
 */
public class MyClass extends BaseClass implements ClassA, ClassB { ... }
```

Constructor:

```java
  public MyClass() { ... }
```

Results in:

```java
  /**
   * Constructor: MyClass
   *
   * description
   */
  public MyClass() { ... }
```

Method:

```java
  public Map<String, String> methodOne(Map<String, String> one, List<Map<String, String>> two, char[] three, int four)  { ... }
```

Results in:

```java
  /**
   * Method: methodOne
   *
   * description
   *
   * Parameters:
   *
   *   one   - Map<String,String>
   *   two   - List<Map<String,String>>
   *   three - char[]
   *   four  - int
   *
   * Returns:
   *
   *   Map<String, String> - return description
   */
  public Map<String, String> methodOne(Map<String, String> one, List<Map<String, String>> two, char[] three, int four) { ... }
```

### JavaScript Example

Code:

```javascript
function testThis($one, $two, $three) {}
```

Put cursor on or before the line and pressing `Super+N` will result in:

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

### Perl Example

Package Code:

```perl
package A::B::C;
```

Put cursor on or before the line and pressing `Super+N` will result in:

```perl
=begin ND

Package: A::B::C

[A::B::C description]

=cut
package A::B::C;
```

Function Code:

```perl
sub index { ... }
```

Results in:

```perl
=begin ND

Function: index

description

Returns:

   return description

=cut
sub index { ... }
```

### PHP Example

Class:

```php
<?php
class ClassD extends ClassA implements ClassB, ClassC { ... }
```

Put cursor on or before the line and pressing `Super+N` will result in:

```php
<?php
/**
 * Class: ClassD
 *
 * [ClassD description]
 *
 * Extends: ClassA
 *
 * Implements: ClassB, ClassC
 */
class ClassD extends ClassA implements ClassB, ClassC { ... }
```

Function:

```php
<?php
function testThis($one='', $two=true, $three=array()) {}
```

Results in:

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

Class Code:

```python
class ClassB(ClassA):
```

Put cursor on or /after/ the line and pressing `Super+N` will result in:

```python
class ClassB(ClassA):
  """
  Class: ClassB

  [ClassB description]

  Extends: ClassA
  """
```

Function Code:

```python
def test_test(one, two=12, three=[]):
    return 'yes'
```

Results in:

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

This setting controls whether to align lines inside documentation blocks based on the previous line.

When using `Enter` inside a documentation block, NaturalDocs will try to align the start of the next line either (1) after the parameter dash (space-hyphen-space) or (2) at the first actual start of last line. See examples.

Example:

```javascript
  /**
   * ...
   * Parameters:
   *
   *   one     - this parameter does something |
   *   twoLong - string
   */
```

If the current line that contains ' - ', then pressing `Enter` will insert enough spaces to align the cursor under the description of the previous line. Result:

```javascript
  /**
   * ...
   * Parameters:
   *
   *   one     - this parameter does something
   *             |
   *   twoLong - string
   */
```

Similarly, if the current line does not contain ' - ', then pressing `Enter` will insert enough spaces to start the line under the first non-Whitespace character inside the documentation. Starting at:

```javascript
  /**
   * ...
   * Parameters:
   *
   *   one     - this parameter does something
   *             this is another line |
   *   twoLong - string
   */
```

Results in:

```javascript
  /**
   * ...
   * Parameters:
   *
   *   one     - this parameter does something
   *             this is another line
   *             |
   *   twoLong - string
   */
```

If this setting is enabled, and there are no snippet fields available in the documentation block, you can also use `Tab` to insert as many spaces as necessary to put the cursor below the description of the previous line.

```javascript
  /**
   * ...
   * Parameters:
   *
   *   one   - this parameter does something
   * |
   */
```

Pressing `Tab` results in:

```javascript
  /**
   * ...
   * Parameters:
   *
   *   one   - this parameter does something
   *           |
   */
```

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

## natural_docs_language_map

This setting maps the current syntax source to a NaturalDocs parser. To determine the name of a source file press `Ctrl+Alt+Shift+P`, and the scope tree will appear in the status line. NaturalDocs parses that string to find "source.(\w+)" and uses the part in parentheses to put in the map.

Additionally, there is a fallback placeholder in the map that is "_". This is a way to get NaturalDocs to default to a particular parser if either (1) the source language of the current file cannot be determined or (2) there is no other mapping for the source language. Example: if you like the way the Python NaturalDocs parser works and want to use that in all languages.


# Todo

* Add more languages (C/C++, Ruby, Scala)
* Something special for PHP5.4 (maybe parse traits like a class?)
* Make awesomer

# Changelog

## July 2, 2013

* Updated the plugin to work with Python3
* Changed OSX shortcuts to actually work (now that I have a Macbook)

## May 14, 2013

* Added a new setting that maps source languages to NaturalDocs parsers
* NaturalDocs will only work on source files that are map in the new setting

## December 7, 2012

* Added a CoffeeScript parser

## July 9, 2012

* Fixed bug with documenting the wrong line if language likes commends below the thing to be documented (e.g. Python)
* Added a custom EventListener to check NaturalDocs settings from keymap contexts
* Resolved [Issue #4](https://github.com/SublimeText/NaturalDocs/issues/4): `Tab` was overriding `next_field` actions.

## June 29, 2012

* Resolved [Issue #6](https://github.com/SublimeText/NaturalDocs/issues/6): inserting doc-blocks does not work when directly above EOF
* Fixed bug with new preferences file not getting used correctly all the time (especially for non-Javascript like languages)

## June 11, 2012

* Resolved [Issue #5](https://github.com/SublimeText/NaturalDocs/issues/5): Move settings file to `NaturalDocs.sublime-settings` / `User/NaturalDocs.sublime-settings`

## May 15, 2012

* Fixed [Issue #3](https://github.com/SublimeText/NaturalDocs/issues/3): inserting doc-blocks does not work when directly above EOF
* Fix bug with inserting a Group block when parser uses
* Changed default keymappings for OSX

## April 11, 2012

* Snakecase all the Pasrers' function names
* Added `__getattr__` to `BaseParser` for external classes to access language settings

## April 9, 2012

* Added Java parser (updated BaseParser to be more robust)
* Fixed an indent bug with decorate command
* Fixing bug in PHP parser. Class parser would not add `implements` to docblock
* Fixing keymaps, `natural_docs_deep_indent`, and `NaturalDocsIndentCommand` to work

## March 21, 2012

* Add Decorations for Perl & Python
* Added the ability to add Class/Package doc-blocks
* Changed setting `natural_docs_extend_double_slash` to `natural_docs_continue_comments`
* Added keymappings to continue number-sign comments if `natural_docs_continue_comments` is `True`
