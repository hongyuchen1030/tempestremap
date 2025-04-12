import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path.home() / "uxarray"))
sys.path.insert(0, str(Path.home() / "xarray"))
import uxarray as ux
import pandas as pd

if len(sys.argv) != 2:
    print("Usage: python generate_connectiviey.py <mesh_path>")
    sys.exit(1)

mesh_path = Path(sys.argv[1]).resolve()

if not mesh_path.exists():
    print(f" File not found: {mesh_path}")
    sys.exit(1)

# Parse mesh name and resolution from filename
mesh_name = mesh_path.stem  
csv_name = f"{mesh_name}_edge_cartesian.csv"
csv_path = mesh_path.parent / csv_name


uxgrid = ux.open_grid(str(mesh_path))


print(uxgrid)

# Collect edge data (Cartesian)
records = []
for face_id in range(uxgrid.n_face):
    face_nodes = uxgrid.face_node_connectivity[face_id].values
    face_nodes = face_nodes[face_nodes != -1]

    for i in range(len(face_nodes)):
        src = face_nodes[i]
        tgt = face_nodes[(i + 1) % len(face_nodes)]

        records.append({
            "face_id": face_id,
            "src_x": uxgrid.node_x[src].item(),
            "src_y": uxgrid.node_y[src].item(),
            "src_z": uxgrid.node_z[src].item(),
            "tgt_x": uxgrid.node_x[tgt].item(),
            "tgt_y": uxgrid.node_y[tgt].item(),
            "tgt_z": uxgrid.node_z[tgt].item(),
        })

df = pd.DataFrame(records)
df.to_csv(csv_path, index=False)

print(f"✅ CSV written to {csv_path}")