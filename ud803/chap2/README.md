# Chapter 2 - Data and Datatypes

## Introduction
- Explains the simple data and datatypes available in JavaScript
- String datatype
- Variables
- Booleans
- NaN
- null
- undefined

## Strings
- String can be concanatenated with '+'
- strings can also be concanatenated with .concat function

## Variables
- Variable declarations follow the camelCase syntax
- Variable declarations start with a 'var' keyword

## Booleans
- true and false are boolean operators

## null
- has no value
- ex, var x = null

## undefined
- has no value not even nothing

## NaN
- indicates that it is an invalid arithmetic operation
- Ex, math.sqrt(-10)

## Equality
- JavaScript is a loosely typed language. Hence it becomes much more difficult to 
  debug problems
- For instance in a strongly typed language,
  ```
  string variable = "madhu"
  int num = 10
  ```
  whereas in a loosely typed language like JavaScript
  ```
  var str = "string"
  var boo = 1
  ```
- So, in cases of comparison operations JavaScript implicitly converts the operands
  on either side of the equality operator to 1 and then performs the comparison.
  Hence the name type coercion
- To retain the type on either side of the operator you should use "strict equality"
  operator ('===')
