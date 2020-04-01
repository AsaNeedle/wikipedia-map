
import requests
import wikipedia
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import pydot

input_name = "Michel Foucault"

graph = pydot.Dot(graph_type="digraph")
root = input_name
influence_nodes = []

response = wikipedia.WikipediaPage(input_name).html()
html = BeautifulSoup(response, 'html.parser')

infobox = html.find("table", "infobox")
academic_did_influence_section = infobox.find("div", string="Influences")
academic_was_influenced_section= infobox.find("div", string="Influenced")

science_did_influence_section = infobox.find("th", string="Influences")
science_was_influenced_section = infobox.find("th", string="Influenced")
 
if academic_did_influence_section != None:
  influences = academic_did_influence_section.parent.find("ul", "NavContent").find_all("a")
  influenced = academic_was_influenced_section.parent.find("ul", "NavContent").find_all("a")
else:
  influences = science_did_influence_section.next_sibling.find_all("a")
  influenced = science_was_influenced_section.next_sibling.find_all("a")

# print("INFLUENCES")
# for i in influences:
#   cur_influence = i.string
#   if cur_influence[0] != '[':
#     print(cur_influence)


print("INFLUENCED")
for i in influenced:
  cur_influenced = i.string
  if cur_influenced[0] != '[':
    if cur_influenced[:7] == "List of":
      influence_nodes.append(f'Literally all{cur_influenced[7:]}')
    else:
      influence_nodes.append(cur_influenced)

# with open("foucault.txt") as f:
#   f.write(foucault_body)



graph.write_png("foucault.png")