import http.client
import json
import time
import timeit
import sys
import collections
from pygexf.gexf import *

# implement your data retrieval code here
h = http.client.HTTPSConnection("rebrickable.com")
KEY = sys.argv[1]
request_url="/api/v3/lego/sets/?key="+KEY+"&page_size=1000&ordering=-num_parts"
h.request("GET", request_url)
result = h.getresponse()
resData = result.read()
resDataStr = resData.decode('utf-8')
resultsDict = json.loads(resDataStr)["results"]
#print("oK")
name = []
set_num = []
Parts = []

# complete auto grader functions for Q1.1.b,d


def min_parts():
    """
    Returns an integer value
    """
    # min_parts = 270
    # you must replace this with your own value
    # return -1

    return 270


def lego_sets():
    """
    return a list of lego sets.
    this may be a list of any type of values
    but each value should represent one set

    e.g.,
    biggest_lego_sets = lego_sets()
    print(len(biggest_lego_sets))
    > 280
    e.g., len(my_sets)
    """
    # you must replace this line and return your own list

    for i in range(min_parts()):
        name.append(resultsDict[i]["name"])
        set_num.append(resultsDict[i]["set_num"])

    for i in range(min_parts()):
        set_id = set_num[i]
        url = "/api/v3/lego/sets/" + set_id + "/parts/?key="+KEY+"&page_size=1000"
        h.request("GET", url)
        res = h.getresponse().read()
        res_dict = json.loads(res)["results"]
        res_dict.sort(key=lambda k: k["quantity"], reverse=True)
        part_dict = {}
        part_set = []
        for j in range(min(20, len(res_dict))):
            temp = {}
            temp["color"] = res_dict[j]["color"]
            temp["quantity"] = res_dict[j]["quantity"]
            temp["name"] = res_dict[j]["part"]["name"]
            temp["number"] = res_dict[j]["part"]["part_num"]
            part_set.append(temp)

        part_dict["set_num"] = set_num[i]
        part_dict["Parts"] = part_set
        Parts.append(part_dict)
        


lego_sets()


def gexf_graph():
    """
    return the completed Gexf graph object
    """
    # you must replace these lines and supply your own graph
    gexf = Gexf("author", "title")
    mygraph = gexf.addGraph("undirected", "static", "A web network")
    atr_type = mygraph.addNodeAttribute('Type', type='string')
    atr_id = mygraph.addNodeAttribute('id', type='string')
    atr_label = mygraph.addNodeAttribute('label', type='string')
    atr_color_r = mygraph.addNodeAttribute('color_r', type='string', defaultValue='0')
    atr_color_g = mygraph.addNodeAttribute('color_g', type='string', defaultValue='0')
    atr_color_b = mygraph.addNodeAttribute('color_b', type='string', defaultValue='0')
    k = 0
    for i in range(min_parts()):
        tmp = mygraph.addNode(set_num[i], name[i], r="0", g="0", b="0")
        tmp.addAttribute(atr_type, "set")
        tmp.addAttribute(atr_id, set_num[i])
        tmp.addAttribute(atr_label, name[i])
        for j in range(len(Parts[i]["Parts"])):
            if mygraph.nodeExists(Parts[i]["Parts"][j]["number"]+"_"+Parts[i]["Parts"][j]["color"]["rgb"])==0:
                temp = mygraph.addNode((Parts[i]["Parts"][j]["number"]+"_"+Parts[i]["Parts"][j]["color"]["rgb"]), Parts[i]["Parts"][j]["name"], r=str(int(Parts[i]["Parts"][j]["color"]["rgb"][0:2], 16)), g=str(int(Parts[i]["Parts"][j]["color"]["rgb"][2:4], 16)), b=str(int(Parts[i]["Parts"][j]["color"]["rgb"][4:6], 16)))
                temp.addAttribute(atr_type, "part")
                temp.addAttribute(atr_id, (Parts[i]["Parts"][j]["number"]+"_"+Parts[i]["Parts"][j]["color"]["rgb"]))
                temp.addAttribute(atr_label, Parts[i]["Parts"][j]["name"])
                temp.addAttribute(atr_color_r, Parts[i]["Parts"][j]["color"]["rgb"][0:2])
                temp.addAttribute(atr_color_g, Parts[i]["Parts"][j]["color"]["rgb"][2:4])
                temp.addAttribute(atr_color_b, Parts[i]["Parts"][j]["color"]["rgb"][4:6])
            mygraph.addEdge(str(k), set_num[i], (Parts[i]["Parts"][j]["number"]+"_"+Parts[i]["Parts"][j]["color"]["rgb"]), weight=Parts[i]["Parts"][j]["quantity"])
            k = k+1
    output_file = open("bricks_graph.gexf", "wb")
    gexf.write(output_file)
    return -1


gexf_graph()


# complete auto-grader functions for Q1.2.d

def avg_node_degree():
    """
    hardcode and return the average node degree
    (run the function called “Average Degree”) within Gephi
    """
    # you must replace this value with the avg node degree
    return 5.325


def graph_diameter():
    """
    hardcode and return the diameter of the graph
    (run the function called “Network Diameter”) within Gephi
    """
    # you must replace this value with the graph diameter
    return 8


def avg_path_length():
    """
    hardcode and return the average path length
    (run the function called “Avg. Path Length”) within Gephi
    :return:
    """
    # you must replace this value with the avg path length
    return 4.429

