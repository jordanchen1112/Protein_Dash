import dash_bio as dashbio
from dash import Dash, html, Input, Output, callback, dcc
from dash_bio.utils import PdbParser, create_mol3d_style

# Define regions based on residue numbers
def get_region(residue_num):
    residue_num = int(residue_num)
    if 0 <= residue_num <= 121:
        return "Repeat 1"
    elif 121 < residue_num <= 241:
        return "Repeat 2"
    elif 241 < residue_num <= 362:
        return "Repeat 3"
    elif 362 < residue_num <= 484:
        return "Repeat 4"
    elif 484 < residue_num <= 607:
        return "Repeat 5"
    elif 607 < residue_num <= 729:
        return "Repeat 6"
    elif 729 < residue_num <= 851:
        return "Repeat 7"
    elif 851 < residue_num <= 973:
        return "Repeat 8"
    elif 973 < residue_num <= 1093:
        return "Repeat 9"
    elif 1093 < residue_num <= 1211:
        return "Repeat 10"
    elif 1211 < residue_num <= 1335:
        return "Repeat 11"
    elif 1335 < residue_num <= 1457:
        return "Repeat 12"
    elif 1457 < residue_num <= 1579:
        return "Repeat 13"
    elif 1579 < residue_num <= 1696:
        return "Repeat 14"
    elif 1696 < residue_num <= 1818:
        return "Repeat 15"
    elif 1818 < residue_num <= 1935:
        return "Repeat 16"
    else:
        return "Outside defined regions"

def _is_ki67_domain(residue_num):
    if 92 <= residue_num <= 113:
        return 'Ki67-1'
    elif 214 <= residue_num <= 235:
        return 'Ki67-2'
    elif 336 <= residue_num <= 357:
        return 'Ki67-3'
    elif 458 <= residue_num <= 478:
        return 'Ki67-4'
    elif 578 <= residue_num <= 599:
        return 'Ki67-5'
    elif 700 <= residue_num <= 721:
        return 'Ki67-6'
    elif 822 <= residue_num <= 843:
        return 'Ki67-7'
    elif 944 <= residue_num <= 965:
        return 'Ki67-8'
    elif 1066 <= residue_num <= 1087:
        return 'Ki67-9'
    elif 1184 <= residue_num <= 1205:
        return 'Ki67-10'
    elif 1306 <= residue_num <= 1327:
        return 'Ki67-11'
    elif 1427 <= residue_num <= 1448:
        return 'Ki67-12'
    elif 1549 <= residue_num <= 1570:
        return 'Ki67-13'
    elif 1669 <= residue_num <= 1690:
        return 'Ki67-14'
    elif 1791 <= residue_num <= 1806:
        return 'Ki67-15'
    elif 1909 <= residue_num <= 1929:
        return 'Ki67-16'
    else:
        return False


app = Dash()
# server = app.server
parser = PdbParser('All.pdb')
data = parser.mol3d_data()
default_styles = []
for atom in data['atoms']:
    atom_style = {
        'visualization_type': 'cartoon',
        'color': 'grey'  # Default color for all atoms
    }
    atom_residue_num = atom.get('residue_index', 'N/A')
    if _is_ki67_domain(atom_residue_num):
        atom_style['color'] = 'yellow'
    default_styles.append(atom_style)

# default_styles = create_mol3d_style(
#     data['atoms'], visualization_type='cartoon', color_element='chain'
# )

app.layout = html.Div(
    [
        dashbio.Molecule3dViewer(
            id='dashbio-default-molecule3d',
            modelData=data,
            styles=default_styles,
            style={'width': '100%', 'height': '500px'},
        ),
        dcc.Checklist(
            id='highlight-checkbox',
            options=[{'label': 'Display Ki67 Domain', 'value': 'show_ki67'}],
            value=[],
        ),
        html.Br(),
        dcc.Dropdown(
            id='style-dropdown',
            options=[
                {'label': 'Stick', 'value': 'stick'},
                {'label': 'Cartoon', 'value': 'cartoon'},
                {'label': 'Sphere', 'value': 'sphere'},
            ],
            value='cartoon',  # Default value
            placeholder="Select Visualization Style",
        ),
        html.Br(),
        # html.Label("Highlight Region:"),
        html.Div(id='default-molecule3d-output'),
    ],
    style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'height': '100vh',
        'width': '100%',
        'textAlign': 'left',
    }
)

@callback(
    Output('dashbio-default-molecule3d', 'styles'),
    [Input('highlight-checkbox', 'value')],
    [Input('dashbio-default-molecule3d', 'selectedAtomIds')],
    [Input('style-dropdown', 'value')],
)
def highlight_region(checkbox_values, atom_ids, style):
    # Return default styles if no atoms are selected
    if atom_ids is None or len(atom_ids) == 0:
        return default_styles.copy()  # Ensure a new object is returned
    # Get the first selected atom's information
    atom_info = data['atoms'][atom_ids[-1]]
    residue_num = atom_info.get('residue_index', 'N/A')
    region = get_region(residue_num)


    # Create a new styles list to modify the appearance of the selected region
    new_styles = []
    for atom in data['atoms']:
        atom_style = {
            'visualization_type': style,
            'color': 'grey'  # Default color for all atoms
        }
        atom_residue_num = atom.get('residue_index', 'N/A')
        atom_region = get_region(atom_residue_num)
        if atom_region == region:
            atom_style['color'] = 'red'  # Highlight color for the selected region
        if checkbox_values:
            if checkbox_values[0] == 'show_ki67' and _is_ki67_domain(atom_residue_num):
                atom_style['color'] = 'yellow'

        new_styles.append(atom_style)

    return new_styles


@callback(
    Output('default-molecule3d-output', 'children'),
    Input('dashbio-default-molecule3d', 'selectedAtomIds')
)
def show_selected_atoms(atom_ids):
    if atom_ids is None or len(atom_ids) == 0:
        return 'No residue has been selected. Click somewhere on the protein structure to select a residue.'

    output = []
    atm = atom_ids[-1]
    atom_info = data['atoms'][atm]
    residue_num = atom_info.get('residue_index', 'N/A')
    region = get_region(residue_num)
    ki67_domain_number = 'No'
    if _is_ki67_domain(residue_num):
        ki67_domain_number = _is_ki67_domain(residue_num)

    output.append(html.Div([
        # html.Div(f'Element: {atom_info["elem"]}'),
        # html.Div(f'Chain: {atom_info["chain"]}'),
        html.Div(f'Residue name: {atom_info["residue_name"]}'),
        # html.Div(f'Residue number: {residue_num}'),
        html.Div(f'Region: {region}'),
        html.Div(f'Is Ki67 Domain: {ki67_domain_number}'),
        html.Br()
    ]))

    return output

if __name__ == '__main__':
    app.run(debug=True)