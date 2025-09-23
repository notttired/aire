def test_example(page):
    page.goto("https://www.aircanada.com/home/ca/en/aco/flights")
    assert "Air Canada" in page.title()
