#!/bin/bash
module load climate-utils
module load python
module load cray-netcdf
# List of resolutions (edit as needed)
resolutions=(10 20 30 40 50 60)

# Paths
BIN_DIR="./bin"
OUTPUT_DIR="./output"
PY_SCRIPT="./scripts/generate_connectivity.py"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Mesh types
meshes=("COMesh" "CSMesh")

# Loop over meshes and resolutions
for mesh in "${meshes[@]}"; do
    for res in "${resolutions[@]}"; do
        mesh_file="${OUTPUT_DIR}/${mesh}_${res}.g"

        if [ "$mesh" == "COMesh" ]; then
            echo " Generating ICOMesh at res $res -> $mesh_file"
            "$BIN_DIR/GenerateICOMesh" --res "$res" --dual --file "$mesh_file"
        elif [ "$mesh" == "CSMesh" ]; then
            echo " Generating CSMesh at res $res -> $mesh_file"
            "$BIN_DIR/GenerateCSMesh" --res "$res" --alt --file "$mesh_file"
        else
            echo "❌ Unknown mesh type: $mesh"
            continue
        fi

        # Call Python script to generate corresponding CSV
        echo "🔸 Generating connectivity CSV for $mesh_file"
        python3 "$PY_SCRIPT" "$mesh_file"
    done
done
