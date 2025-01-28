import numpy as np

def read_file_to_1d_array(file_path,dtype):
    data = np.loadtxt(file_path, dtype)
    return data.flatten()

def write_febio_with_data(input_file: str, output_file: str, element, point):
    # Read the XML content from the input file
    with open(input_file, "r") as file:
        template_content = file.read()
    # Split the content for each section
    #Control 
    Control_section = template_content.split("<Control>")
    Control_section = Control_section[1].split("</Control>")
    control_content = Control_section[0]
    #Globals
    Globals_section = template_content.split("<Globals>")
    Globals_section = Globals_section[1].split("</Globals>")
    globals_content = Globals_section[0]    
    #Material
    Material_section = template_content.split("<Material>")
    Material_section = Material_section[1].split("</Material>")
    material_content = Material_section[0]
    #Mesh
    #node
    node_content = "\n          <Nodes name="'Object_number'">"
    node_content += f"\n            </Nodes>"
    #Elements
    element_content = "\n           <Elements type="'tri3'" name="'Part1'">"
    element_content += f"\n         </Elements>"
    #Boundry 
    boundary_content = "\n          <Surface name="'fixed-surface'">"
    boundary_content += f"\n            </Surface>\n"
    #append all sub-sections  
    mesh_content = f"{node_content}{element_content}{boundary_content}"
    #mesh domain
    domain_content = """	<MeshDomains>
		<ShellDomain name="Part2" mat="Material1">
			<shell_thickness>0.01</shell_thickness>
		</ShellDomain>
	</MeshDomains>"""
    #boundary 
    bc_content = """	<Boundary>
		<bc name="ZeroDisplacement1" node_set="@surface:fixed-surface" type="zero displacement">
			<x_dof>1</x_dof>
			<y_dof>1</y_dof>
			<z_dof>1</z_dof>
		</bc>
	</Boundary>"""
    #Loads
    loads_content ="""	<Loads>
		<surface_load name="Pressure1" surface="Pressure1" type="pressure">
			<pressure lc="1">-10000</pressure>
			<symmetric_stiffness>1</symmetric_stiffness>
			<linear>0</linear>
			<shell_bottom>0</shell_bottom>
		</surface_load>
	</Loads>"""
    #LoadData
    LoadData_section = template_content.split("<LoadData>")
    LoadData_section = LoadData_section[1].split("</LoadData>")
    loaddata_content = LoadData_section[0]
    #Output
    Output_section = template_content.split("<Output>")
    Output_section = Output_section[1].split("</Output>")
    output_content = Output_section[0]    
    #print(material_content.strip())
    # header and footer of feb file
    feb_content_start = """<?xml version="1.0" encoding="ISO-8859-1"?>
<febio_spec version="4.0">
    <Module type="solid"/>"""
    feb_content_end = """</febio_spec>\n"""

    feb_content = f"{feb_content_start}"
    feb_content += f"\n     <Control>{control_content}</Control>\n"
    feb_content += f"       <Globals>{globals_content}</Globals>\n"
    feb_content += f"       <Material>{material_content}</Material>\n"
    feb_content += f"       <Mesh>{mesh_content}       </Mesh>\n"
    feb_content += f"{domain_content}\n"
    feb_content += f"{bc_content}\n"
    feb_content += f"{domain_content}\n"
    feb_content += f"{loads_content}\n"
    feb_content += f"       <LoadData>{loaddata_content}</LoadData>\n"
    feb_content += f"       <Output>{output_content}</Output>\n"
    feb_content += f"{feb_content_end}\n"
    # Write the updated content to the file
    with open(output_file, "w") as file:
        file.write(feb_content)

# read a element file in txt format
file_path = "data/element.txt"  
element = read_file_to_1d_array(file_path,int)
print("Element Array:", element)

# read a element file in txt format
file_path = "data/points.txt"  
point = read_file_to_1d_array(file_path,float)
print("points Array:", point)

write_febio_with_data("data/Model.txt","test.feb", element, point)
print("File written successfully!")

