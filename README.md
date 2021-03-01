Greatly eases manual Blind SQL injection by automating the loop for data extraction.

This is basically a word-for-word implementation of the script in [this video](https://www.youtube.com/watch?v=d3fUh0QeoZI) by cwinfosec (Thanks!!)

Priority improvements
* Binary search for ascii values
* Sort characters in order of likelihood. (lowercase -> symbols -> numbers -> uppercase)

Possible improvements
* Command line input for QUERY parameter
* Expose some variables on the command line
    - TRUE_RESPONSE
    - COOKIES (?)
    - HEADERS (?)
    - etc.
