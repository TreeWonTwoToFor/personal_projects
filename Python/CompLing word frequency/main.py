import os
import math
import plotly.express as px

# getting the text from the input file
f = open("input.txt", "r")
input_text = f.read().lower()

# removes all of the punctuation in the input sentence
def format(text_to_format):
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for ele in text_to_format:
        if ele in punc:
            text_to_format = text_to_format.replace(ele, "")
    return text_to_format

def countOccurrence(a):
  k = {}
  for j in a:
    if j in k:
      k[j] +=1
    else:
      k[j] =1
  return k


def e_func():
    e_xlist = []
    e_ylist = []
    for i in range(1,500):
      e_xlist.append(i/5)
      e_ylist.append(1/(math.exp(i/5)))
    return(e_xlist, e_ylist)

input_list = format(input_text).split()
sorted_input_list = dict(reversed(sorted(countOccurrence(input_list).items(), key=lambda x:x[1])))

# prints out the sentence
os.system('cls')
print(sorted_input_list)

fig = px.line(x=sorted_input_list.keys(), y=sorted_input_list.values())
#fig = px.line(x=e_func()[0], y=e_func()[1])
#fig.write_html('graphs/output_graph.html', auto_open=True)
fig.write_image("graphs/output_graph_words.png")
fig = px.line(x=e_func()[0], y=e_func()[1])
fig.write_image("graphs/output_graph_e.png")