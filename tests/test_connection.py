def test_connection(page):
    page.goto("https://www.aircanada.com/home/ca/en/aco/flights")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    assert "Air" in page.title()