from utils import add_nums
from bs4 import BeautifulSoup
from create_graph import get_beautiful_soup, get_title_from_soup, get_influences, get_influenced, create_graph

class TestGetBeautifulSoup:
  def test_perfect_match(self):
    result = get_beautiful_soup("Michel Foucault")
    assert isinstance(result, BeautifulSoup)
  def test_disambiguation_error(self):
    result = get_beautiful_soup("Wendy Brown")
    assert isinstance(result, list)
class TestGetTitleFromSoup:
  def test_basic(self):
    f = open("wikipedia.txt", "r")
    soup = BeautifulSoup(f.read(), "html.parser")
    assert get_title_from_soup(soup) == "Michel Foucault"
class TestGetInfluences:
  def test_basic(self):
    f = open("wikipedia.txt", "r")
    soup = BeautifulSoup(f.read(), "html.parser")
    infobox = soup.find("table", "infobox")
    foucault_influences_hrefs = [
      ("Louis Althusser", "/wiki/Louis_Althusser"),
      ("Antonin Artaud", "/wiki/Antonin_Artaud"),
      ("Gaston Bachelard", "/wiki/Gaston_Bachelard"),
      ("Roland Barthes", "/wiki/Roland_Barthes"),
    ]
    assert get_influences(infobox) == foucault_influences_hrefs
class TestGetInfluenced:
  def test_basic(self):
    f = open("wikipedia.txt", "r")
    soup = BeautifulSoup(f.read(), "html.parser")
    infobox = soup.find("table", "infobox")
    foucault_influenced_hrefs = [
      ("Edward Said", "/wiki/Edward_Said"),
      ("Pierre Bourdieu", "/wiki/Pierre_Bourdieu"),
      ("Gilles Deleuze", "/wiki/Gilles_Deleuze"),
      ("Judith Butler", "/wiki/Judith_Butler")
    ]
    assert get_influenced(infobox) == foucault_influenced_hrefs
class TestCreateMap:
  def test_basic(self):
    soup = get_beautiful_soup("Michel Foucault")
    result = create_graph(soup)
    print(result)
    assert result[0] == "Michel Foucault" 