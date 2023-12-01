from project import *


def test_is_paragraph():
    assert is_paragraph(
        "This is a paragraph with more than 15 words. This is a paragraph with more than 15 words.")
    assert not is_paragraph("this is not a paragraph")
    assert is_paragraph("This is a? with more! than words. Right?")
    assert is_paragraph("H.e.l.l.o?")
    assert is_paragraph("H!e!l?l?o?")
    assert is_paragraph("H!e!l!l!o!")
    assert is_paragraph("H.e.l.l.o.")
    assert not is_paragraph("This is not a paragraph.")
