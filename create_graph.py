import requests
import wikipedia
from bs4 import BeautifulSoup
import pydot

def create_graph(input_name):
  link_name = input_name.replace(" ", "_")
  graph = pydot.Dot(graph_type="digraph")
  root = input_name
  influences_nodes = []
  influenced_nodes = []
  try:
    response = wikipedia.WikipediaPage(input_name)
  except:
    print("No such article")
    return

  html = BeautifulSoup(response.html(), 'html.parser')
  infobox = html.find("table", "infobox")

  academic_did_influence_section = infobox.find("div", string="Influences")
  academic_was_influenced_section= infobox.find("div", string="Influenced")

  science_did_influence_section = infobox.find("th", string="Influences")
  science_was_influenced_section = infobox.find("th", string="Influenced")
  
  influences = []
  if academic_did_influence_section != None:
    influences = academic_did_influence_section.parent.find("ul", "NavContent").find_all("a")

  elif science_did_influence_section != None:
    influences = science_did_influence_section.next_sibling.find_all("a")

  influenced = []
  if academic_was_influenced_section != None:
    influenced = academic_was_influenced_section.parent.find("ul", "NavContent").find_all("a")
  elif science_was_influenced_section != None:
    influenced = science_was_influenced_section.next_sibling.find_all("a")

  if influences:
    for i in influences:
      cur_influence = i.string
      if cur_influence[0] != '[':
        influences_nodes.append(cur_influence)
  if influenced:
    for i in influenced:
      cur_influenced = i.string
      if cur_influenced[0] != '[':
        if cur_influenced[:7] == "List of":
          influenced_nodes.append(f'Literally all{cur_influenced[7:]}')
        else:
          influenced_nodes.append(cur_influenced)
  if not influences and not influenced:
    print("No influences or influenced section found.")
    return

  for i in influences_nodes:
    graph.add_edge(pydot.Edge(i, root))

  for i in influenced_nodes:
    graph.add_edge(pydot.Edge(root, i))

  graph.write_png(f"./static/img/{link_name}.png")

