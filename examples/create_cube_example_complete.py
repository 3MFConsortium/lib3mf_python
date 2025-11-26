import lib3mf
from lib3mf import get_wrapper

# Get version
def get_version(wrapper):
    major, minor, micro = wrapper.GetLibraryVersion()
    print("Lib3MF version: {:d}.{:d}.{:d}".format(major, minor, micro), end="")
    hasInfo, prereleaseinfo = wrapper.GetPrereleaseInformation()
    if hasInfo:
        print("-" + prereleaseinfo, end="")
    hasInfo, buildinfo = wrapper.GetBuildInformation()
    if hasInfo:
        print("+" + buildinfo, end="")
    print("")


# Create vertex in a mesh
def create_vertex(_mesh, x, y, z):
    position = lib3mf.Position()
    position.Coordinates[0] = float(x)
    position.Coordinates[1] = float(y)
    position.Coordinates[2] = float(z)
    _mesh.AddVertex(position)
    return position


# Add triangle in a mesh
def add_triangle(_mesh, p1, p2, p3):
    triangle = lib3mf.Triangle()
    triangle.Indices[0] = p1
    triangle.Indices[1] = p2
    triangle.Indices[2] = p3
    _mesh.AddTriangle(triangle)
    return triangle


# Get a wrapper object
wrapper = get_wrapper()

# Check version always
get_version(wrapper)

# Create a model
model = wrapper.CreateModel()
mesh_object = model.AddMeshObject()
mesh_object.SetName("Box")

# Define the size of the cube
fSizeX, fSizeY, fSizeZ = 100.0, 200.0, 300.0

# Create vertices
vertices = [
    create_vertex(mesh_object, 0, 0, 0),
    create_vertex(mesh_object, fSizeX, 0, 0),
    create_vertex(mesh_object, fSizeX, fSizeY, 0),
    create_vertex(mesh_object, 0, fSizeY, 0),
    create_vertex(mesh_object, 0, 0, fSizeZ),
    create_vertex(mesh_object, fSizeX, 0, fSizeZ),
    create_vertex(mesh_object, fSizeX, fSizeY, fSizeZ),
    create_vertex(mesh_object, 0, fSizeY, fSizeZ)
]

# Define triangles by vertices indices
triangle_indices = [
    (2, 1, 0), (0, 3, 2), (4, 5, 6), (6, 7, 4),
    (0, 1, 5), (5, 4, 0), (2, 3, 7), (7, 6, 2),
    (1, 2, 6), (6, 5, 1), (3, 0, 4), (4, 7, 3)
]

# Create triangles
triangles = []
for v0, v1, v2 in triangle_indices:
    triangles.append(add_triangle(mesh_object, v0, v1, v2))

# Set geometry to the mesh object after creating vertices and triangles
mesh_object.SetGeometry(vertices, triangles)

# Add build item with an identity transform
model.AddBuildItem(mesh_object, wrapper.GetIdentityTransform())

# Save the model to a 3MF file
writer = model.QueryWriter("3mf")
writer.WriteToFile("cube.3mf")