import json
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import codecs
import logging

urls = []
logging.basicConfig(level=logging.DEBUG)

def flatten_skills_tree(node):
    """Flatten the skills tree into a list of skills."""
    skills = []
    if 'name' in node:
        skills.append(node['name'])
    if 'children' in node:
        for child in node['children']:
            skills.extend(flatten_skills_tree(child))
    return skills

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

# Load skills tree data from JSON file
with codecs.open('app/data/skills_tree.json', 'r', encoding='cp1250', errors='ignore') as f:
    skills_tree = json.load(f)
skills = flatten_skills_tree(skills_tree)

# Define Dash app
app = dash.Dash(__name__)
def register_callbacks(app):
    # Define your callbacks here
    # Define callback functions
    @app.callback(
        Output('skills-tree', 'figure'),
        Input('dropdown', 'value')
    )
    @app.callback(
        Output('markdown-container', 'children'),
        Input('skills-tree', 'hoverData')
    )
    def update_markdown_callback(hoverData):
        return update_markdown(hoverData)
    pass




def update_skills_tree(selected_skill):
    # Logic to update the skills tree based on the selected skill
    # You can use the skills_tree data to render the updated skills tree
    # Return the updated skills tree component
    pass



def update_markdown(hoverData):
    logging.debug("Update markdown=" + json.dumps(hoverData))
    # Load the skills tree data from the JSON file
    with codecs.open('app/data/skills_tree.json', 'r', encoding='cp1250', errors='ignore') as file:
        skills_tree = json.load(file)

    _, _, _, _, _, urls, _, _ = convert_to_sunburst_format(skills_tree)

    if hoverData is not None:
        point_index = hoverData['points'][0]['pointNumber']
        md_file_path = urls[point_index]
        try:
            with open('app/data/obsidian/'+md_file_path, 'r', encoding='utf-8', errors='ignore') as file:
                md_content = file.read()
            return dcc.Markdown(md_content)
        except FileNotFoundError:
            return [dcc.Markdown(f"File not found: {md_file_path}")]
        
    return [dcc.Markdown("Not defined in JSON, hoverData is None")]

def get_layout():
    # Load the skills tree data from the JSON file
    with codecs.open('app/data/skills_tree.json', 'r', encoding='cp1250', errors='ignore') as file:
        skills_tree = json.load(file)

    labels, descriptions, info1s, info2s, info3s, urls, parents, values = convert_to_sunburst_format(skills_tree)

    # Create the layout for the Dash application
    layout = html.Div(
        children=[
            html.Div(
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
                    "width": "65%",
                }
            ),
            html.Div(
                id="markdown-container",
                children=[],
                style={
                    "width": "35%",
                    "overflow-y": "auto",
                }
            ),
        ],
        style={
            "display": "flex",
            "align-items": "stretch",
            "justify-content": "center"
        }
    )

    return layout

# Define app layout
app.layout = html.Div(
    children=[
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': skill, 'value': skill} for skill in skills
            ],
            placeholder='Select a skill'
        ),
        html.Div(id='skills-tree')
    ]
)



if __name__ == '__main__':
    app.run_server(debug=True)