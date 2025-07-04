cmake_minimum_required(VERSION 3.13)
project(blendwarf NONE)

# Make version configurable via command line
option(TAG "DFHack version tag to use (e.g., 51.13-r1)" "51.13-r1")

set(PROTOC-BIN "protoc")
set(PROTO-DIR "${CMAKE_CURRENT_SOURCE_DIR}/../proto/${TAG}")
set(PY-DIR "${CMAKE_CURRENT_SOURCE_DIR}/../src/dfhack_client_python/py_export")

# Dynamically find all .proto files in the PROTO-DIR
file(GLOB PROTO_FILES "${PROTO-DIR}/*.proto")

# Create the protoc command with all found .proto files
add_custom_command(OUTPUT protos
  COMMAND ${CMAKE_COMMAND} -E make_directory ${PY-DIR}
  COMMAND ${CMAKE_COMMAND} -E touch ${PY-DIR}/__init__.py
  COMMAND "${PROTOC-BIN}"
  -I${PROTO-DIR}
  --python_out=${PY-DIR}
  ${PROTO_FILES}
)

add_custom_target(DONE ALL
  DEPENDS protos
)
