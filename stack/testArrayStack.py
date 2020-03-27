from arraystack import ArrayStack

def test_stack():
    S = ArrayStack()
    S.push(5)
    print(S.top())
    S.push(6)
    print(len(S))
    print(S.pop())
    print(S.is_empty())
    print(S.data)

# test_stack()

def is_matched(expression):
    """Return True if all delimiters are properly match.
     False otherwise"""
    lefty = '({['
    righty = ')}]'
    S = ArrayStack()
    for char in expression:
        if char in lefty:
            S.push(char)
        elif char in righty:
            if S.is_empty():
                return False
            if righty.index(char) != lefty.index(S.pop()):
                return False
    return S.is_empty()

print(is_matched('{(a+(b+c))}'))

def is_matched_html(raw):
    """Return True if all HTML tags are properly matched;
    False Otherwise."""
    S = ArrayStack()
    # find first '<' character
    start = raw.find('<')
    while start != -1:
        # find next '>' character
        end = raw.find('>', start+1)
        if end == -1:
            return False
        # strip away < >
        tag = raw[start+1:end]
        # this is opening tag
        if not tag.startswith('/'):
            S.push(tag)
        # this is closing tag
        else:
            if S.is_empty():
                return False
            if tag[1:] != S.pop():
                return False
        start = raw.find('<', end+1)
    # all tags matched
    return S.is_empty()

raw_html = """<body>
<center>
<h1> The Little Boat </h1>
</center>
<p> The storm tossed the little
boat like a cheap sneaker in an
old washing machine. The three
drunken fishermen were used to
such treatment, of course, but
not the tree salesman, who even as
a stowaway now felt that he
had overpaid for the voyage. </p>
<ol>
<li> Will the salesman die? </li>
<li> What color is the boat? </li>
<li> And what about Naomi? </li>
</ol>
</body>"""

print(is_matched_html(raw_html))