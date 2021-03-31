import requests
import re
import wikipedia
from bs4 import BeautifulSoup
import pydot
def get_influenced(infobox):
  academic_was_influenced_section= infobox.find("div", string=re.compile("Influenced"))
  science_was_influenced_section = infobox.find("th", string=re.compile("Influenced"))
  notable_students_section = infobox.find("th", string="Notable Students")

  influenced = []
  influenced_nodes = []
  if academic_was_influenced_section != None:
    influenced = academic_was_influenced_section.find_parent("td").find_all("a", title=True)
  elif science_was_influenced_section != None:
    influenced = science_was_influenced_section.next_sibling.find_all("a", title=True)
  if notable_students_section != None:
    notable_students = notable_students_section.find_parent("td").find_all("a", title=True)
    influenced += notable_students
  if influenced:
    for i in influenced:
      cur_influenced = i.string
      if cur_influenced[:7] == "List of":
        influenced_nodes.append((f'Literally all{cur_influenced[7:]}', i.get("href")))
      else:
        influenced_nodes.append((i.get("title"), i.get("href")))
  return influenced_nodes
  
def get_influences(infobox):
  academic_did_influence_section = infobox.find("div", string=re.compile("Influences"))
  science_did_influence_section = infobox.find("th", string=re.compile("Influences"))
  influences = []
  influences_hrefs = []
  if academic_did_influence_section != None:
    influences = academic_did_influence_section.find_parent("td").find_all("a", title=True)
  elif science_did_influence_section != None:
    influences = science_did_influence_section.next_sibling.find_all("a", title=True)
  if influences:
    for i in influences:
      influences_hrefs.append((i.get("title"), i.get("href"))) 
  return influences_hrefs

def get_beautiful_soup(input_name):
  try: 
    suggested_input = wikipedia.suggest(input_name)
    if suggested_input != None:
      search_name = suggested_input
    else:
      search_name = input_name
    response = wikipedia.WikipediaPage(search_name)
    soup = BeautifulSoup(response.html(), features="lxml")
    return soup
  except wikipedia.DisambiguationError as e:
    return e.options

def get_title_from_soup(soup):
  infobox = soup.find("table", "infobox")
  text = infobox.find("div").get_text()
  return ' '.join(text.split())

 
def create_graph(soup):
  graph = pydot.Dot(graph_type="digraph", rankdir="LR")
  infobox = soup.find("table", "infobox")
  title = get_title_from_soup(soup)
  root = title
  link_name = title.replace(" ", "_")
  influences_nodes = get_influences(infobox)    
  influenced_nodes = get_influenced(infobox)
  if not influences_nodes and not influenced_nodes:
    raise Exception("No influences or influenced section found.")

  for i in influences_nodes:
    graph.add_node(pydot.Node(i[0], URL="https://en.wikipedia.org" + i[1]))
    graph.add_edge(pydot.Edge(i[0], root))

  for i in influenced_nodes:
    graph.add_node(pydot.Node(i[0], URL="https://en.wikipedia.org" + i[1]))
    graph.add_edge(pydot.Edge(root, i[0]))
  return (title, graph)
if __name__ == '__main__':
    create_graph("Michel Foucault")