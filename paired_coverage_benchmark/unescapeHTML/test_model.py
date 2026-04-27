import subject

def test_unescape_html_functionality():
    assert subject.unescapeHTML(None) is None
    assert subject.unescapeHTML("Hello &amp; World!") == "Hello & World!"
    assert subject.unescapeHTML("&lt;tag&gt;") == "<tag>"
    assert subject.unescapeHTML('A &quot;quote&quot;') == 'A "quote"'
    assert subject.unescapeHTML("Multi &amp; &lt;entities&gt; here with &nbsp; space.") == "Multi & <entities> here with \u00A0 space."
    assert subject.unescapeHTML("Plain text with no entities.") == "Plain text with no entities."
    assert subject.unescapeHTML("") == ""
    assert subject.unescapeHTML("This &amp is not an entity according to regex.") == "This &amp is not an entity according to regex."
    assert subject.unescapeHTML("It&#39;s a test.") == "It's a test."
    assert subject.unescapeHTML("Hex double quote: &#x22;") == 'Hex double quote: "'
    assert subject.unescapeHTML("Unknown &foobar; entity.") == "Unknown &foobar; entity."
