# Chapter 5

## Introduction
- Functions
- Local and global variables
- Hoisting

## Hoisting
- JavaScript hoists function and variable declaration to the top of the current scope
- assignments won't get hoisted

## Function variables
- Two different ways for using functions, function declarations and function expressions
- JavaScript allows you to store functions in variables - function expression, anonymous function
- Function expressions are not hoisted but function declarations are
- Function expression is when a function is assigned to a function

## Functions as parameters
- A function that is passed as an argument to another function is called as a
  callback

## Named function expressions
- can also have a name to an anonymous function but in that case you should use
 the name of the variable and not the name of the function
 ```
 var variable = function name() {


 }
 ```
## Inline function expressions
 ```
 // Function declaration that takes in two arguments: a function for displaying
 // a message, along with a name of a movie
 function movies(messageFunction, name) {
   messageFunction(name);
 }

 // Call the movies function, pass in the function and name of movie
 movies(function displayFavorite(movieName) {
   console.log("My favorite movie is " + movieName);
 }, "Finding Nemo");
 ```

