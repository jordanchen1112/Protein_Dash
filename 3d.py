import dash_bio as dashbio
from dash import Dash, html, Input, Output, callback
from dash_bio.utils import PdbParser, create_mol3d_style

app = Dash()
parser = PdbParser('All.pdb')
data = parser.mol3d_data()
default_styles = create_mol3d_style(
    data['atoms'], visualization_type='cartoon', color_element='residue'
)


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


app.layout = html.Div([
    dashbio.Molecule3dViewer(
        id='dashbio-default-molecule3d',
        modelData=data,
        styles=default_styles,

    ),
    "Select Residue: ",
    html.Div(id='default-molecule3d-output')
])


@callback(
    Output('dashbio-default-molecule3d', 'styles'),
    Input('dashbio-default-molecule3d', 'selectedAtomIds')
)
def highlight_region(atom_ids):
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
            'visualization_type': 'cartoon',
            'color': 'grey'  # Default color for all atoms
        }
        atom_residue_num = atom.get('residue_index', 'N/A')
        atom_region = get_region(atom_residue_num)
        if atom_region == region:
            atom_style['color'] = 'red'  # Highlight color for the selected region
        new_styles.append(atom_style)

    return new_styles


@callback(
    Output('default-molecule3d-output', 'children'),
    Input('dashbio-default-molecule3d', 'selectedAtomIds')
)
def show_selected_atoms(atom_ids):
    if atom_ids is None or len(atom_ids) == 0:
        return 'No atom has been selected. Click somewhere on the molecular structure to select an atom.'

    output = []
    atm = atom_ids[-1]
    atom_info = data['atoms'][atm]
    residue_num = atom_info.get('residue_index', 'N/A')
    region = get_region(residue_num)

    output.append(html.Div([
        # html.Div(f'Element: {atom_info["elem"]}'),
        # html.Div(f'Chain: {atom_info["chain"]}'),
        html.Div(f'Residue name: {atom_info["residue_name"]}'),
        # html.Div(f'Residue number: {residue_num}'),
        html.Div(f'Region: {region}'),
        html.Br()
    ]))

    return output

if __name__ == '__main__':
    app.run(debug=True)