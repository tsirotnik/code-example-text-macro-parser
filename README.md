### Homework Programing Problem:

**__Link to solution documentation: [SOLUTION](README-solution.md)__**


Please implement a simple template formatting system in your favorite programming language. You may use idiomatic language constructs and standard library facilities for your language. You should be able to complete the problem in a couple of hours.

Here's some sample input, from which you may infer the desired behavior:

```
!name1=John Q.

!name2=Smith

!salutation=Dear @name1 @name2

1 Infinite Loop

!product=Horcrux Widget

Somewheresville, CA 98765




@salutation,




Thank you for your interest in @{product}s.

Unfortunately, we sold our last @product yesterday.




@name1, if you have any more questions about our products,

email us at support@@horcrux.com, tweet to @@horcrux_support,

or call us @@ 1-800-HORCRUX.
```



Your solution should generate the following output:
```



1 Infinite Loop

Somewheresville, CA 98765




Dear John Q. Smith,




Thank you for your interest in Horcrux Widgets.

Unfortunately, we sold our last Horcrux Widget yesterday.




John Q., if you have any more questions about our products,

email us at support@horcrux.com, tweet to @horcrux_support,

or call us @ 1-800-HORCRUX.
```



### Solution

Your solution should be a filter that reads from stdin and writes to stdout.

Note:

- You may assume that the input is 7-bit ASCII.
- Do not assume that the input will “compile” correctly.
- There may be an arbitrary number of !-assignment directives interspersed throughout the input.
- The color in the sample input and output is only to make the samples easier to read.
