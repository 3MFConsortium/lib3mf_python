import atexit
import lib3mf
from lib3mf import Lib3MF as _L  # this is the generated Lib3MF.py module


print("Using lib3mf from:", lib3mf.__file__)
print("Using Lib3MF module from:", _L.__file__)

# --- Create some lib3mf objects as GLOBALS (so they live until shutdown) ---

wrapper = lib3mf.get_wrapper()
model = wrapper.CreateModel()
mesh = model.AddMeshObject()
mesh.SetName("py313-shutdown-test")
writer = model.QueryWriter("3mf")


def simulate_shutdown_bug():
    print("Simulating interpreter teardown: setting Lib3MF.ErrorCodes = None")
    # This mimics what CPython does when tearing down modules:
    _L.ErrorCodes = None

    print("Deleting mesh -> Base.__del__ -> Wrapper.Release -> checkError(ErrorCodes=None)")
    # Deleting the mesh will trigger Base.__del__, which calls wrapper.Release(self),
    # which calls checkError and tries to use ErrorCodes.SUCCESS -> boom.
    global mesh
    del mesh


atexit.register(simulate_shutdown_bug)

print("Setup complete. Exiting will trigger simulated shutdown.\n")
