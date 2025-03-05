#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="$SCRIPT_DIR/generated"
git clone https://github.com/archiver-appliance/epicsarchiverap.git $TARGET_DIR/epicsarchiverap
cp $TARGET_DIR/epicsarchiverap/src/main/edu/stanford/slac/archiverappliance/PB/EPICSEvent.proto $TARGET_DIR
rm -r $TARGET_DIR/epicsarchiverap/
protoc $TARGET_DIR/EPICSEvent.proto --python_out=$TARGET_DIR --pyi_out=$TARGET_DIR --proto_path=$TARGET_DIR
rm $TARGET_DIR/EPICSEvent.proto
echo "Generated files found in $TARGET_DIR/"
