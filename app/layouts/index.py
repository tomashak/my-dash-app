from dash import html
from dash import dcc
import json
import codecs

def convert_to_sunburst_format(node, parent=""):
    labels = [node['name']]
    descriptions = [node.get('description', '')]
    info1s = [node.get('info1', '')]
    info2s = [node.get('info2', '')]
    info3s = [node.get('info3', '')]
    urls = [node.get('url', '')]
    parents = [parent]
    values = [1]
    if 'children' in node:
        for child in node['children']:
            child_labels, child_descriptions, child_info1s, child_info2s, child_info3s, child_urls, child_parents, child_values = convert_to_sunburst_format(child, node['name'])
            labels.extend(child_labels)
            descriptions.extend(child_descriptions)
            info1s.extend(child_info1s)
            info2s.extend(child_info2s)
            info3s.extend(child_info3s)
            urls.extend(child_urls)
            parents.extend(child_parents)
            values.extend(child_values)
    return labels, descriptions, info1s, info2s, info3s, urls, parents, values

def get_layout():
    # Load the skills tree data from the JSON file
    with codecs.open('app/data/skills_tree.json', 'r', encoding='cp1250', errors='ignore') as file:
        skills_tree = json.load(file)

    labels, descriptions, info1s, info2s, info3s, urls, parents, values = convert_to_sunburst_format(skills_tree)

    # Create the layout for the Dash application
    layout = html.Div(
        children=[                        
            dcc.Graph(
                id="skills-tree",
                figure={
                    "data": [
                        {
                            "type": "sunburst",
                            "labels": labels,
                            "parents": parents,
                            "values": values,
                            "hovertext": [f'{desc}<br>{info1}<br>{info2}<br>{info3}<br><a href="{url}">Source</a>' for desc, info1, info2, info3, url in zip(descriptions, info1s, info2s, info3s, urls)],
                            "hoverinfo": "label+text"
                        }
                    ],
                    "layout": {
                        "margin": {"l": 0, "r": 0, "t": 30, "b": 0},
                        "height": 900,
                    },
                },
            ),          
            
        ],
        style={
                "display": "flex",
                "align-items": "center",
                "justify-content": "center"
            }
    )

    return layout