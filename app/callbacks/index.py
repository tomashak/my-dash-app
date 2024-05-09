import json
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import codecs


def flatten_skills_tree(node):
    """Flatten the skills tree into a list of skills."""
    skills = []
    if 'name' in node:
        skills.append(node['name'])
    if 'children' in node:
        for child in node['children']:
            skills.extend(flatten_skills_tree(child))
    return skills

# Load skills tree data from JSON file
with codecs.open('app/data/skills_tree.json', 'r', encoding='cp1250', errors='ignore') as f:
    skills_tree = json.load(f)
skills = flatten_skills_tree(skills_tree)

# Define Dash app
app = dash.Dash(__name__)
def register_callbacks(app):
    # Define your callbacks here
    pass

# Define callback functions
@app.callback(
    Output('skills-tree', 'children'),
    [Input('dropdown', 'value')]
)


def update_skills_tree(selected_skill):
    # Logic to update the skills tree based on the selected skill
    # You can use the skills_tree data to render the updated skills tree
    # Return the updated skills tree component
    pass

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