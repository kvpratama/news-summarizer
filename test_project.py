from project import *


def test_inference():
    payload = {"inputs": "This is a test."}
    assert inference(payload)


def test_scraping():
    assert scraping("https://www.google.com")


def test_find_news():
    assert find_news("covid")


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
