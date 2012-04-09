NaturalDocs is a [Sublime Text 2](http://www.sublimetext.com/) package which makes writing [NaturalDocs](http://www.naturaldocs.org) easy. Based on [DocBlockr](https://github.com/spadgos/sublime-jsdocs) by [Nick Fisher](https://github.com/spadgos), influenced by [Germán M. Bravo](https://github.com/Kronuz)'s [SublimeLinter](https://github.com/Kronuz/SublimeLinter).

# Languages

Currently supported languages: Java, JavaScript, Perl, PHP, and Python.

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

### Java Example

Class:

```java
public class MyClass extends BaseClass implements ClassA, ClassB { ... }
```

Put cursor on or before the line and pressing `Super-N` will result in:

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

### Perl Example

Package Code:

```perl
package A::B::C;
```

Put cursor on or before the line and pressing `Super-N` will result in:

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

Put cursor on or before the line and pressing `Super-N` will result in:

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

Put cursor on or /after/ the line and pressing `Super-N` will result in:

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

If this is set to `True` then pressing `Tab` inside a documentation block, will try to add enough spaces to align the cursor below the description section of the previous line (which only the Parameters section has), otherwise it will just insert two spaces.

Example:

```javascript
  /**
   * ...
   * Parameters:
   *
   *   one   - this parameter does something
   *   |
   */
```

If the cursor is below a line that contains ' - ', then pressing `Tab` will insert enough spaces to align the cursor under the description of the prvious line. Result:

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

# Todo

* Add shortcuts for inserting [NaturalDoc Group](http://www.naturaldocs.org/documenting/reference.html#Summaries) blocks
* Add more languages (C/C++, Ruby)
* Something special for PHP5.4 (maybe parse traits like a class?)
* Snakecase all the Pasrers' function names
* Make awesomer

# Changelog

## March 21, 2012

* Add Decorations for Perl & Python
* Added the ability to add Class/Package doc-blocks
* Changed setting `natural_docs_extend_double_slash` to `natural_docs_continue_comments`
* Added keymappings to continue number-sign comments if `natural_docs_continue_comments` is `True`

## April 9, 2012

* Added Java parser (updated BaseParser to be more robust)
* Fixed an indent bug with decorate command
* Fixing bug in PHP parser. Class parser would not add `implements` to docblock
* Fixing keymaps, `natural_docs_deep_indent`, and `NaturalDocsIndentCommand` to work
