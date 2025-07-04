# Python DFHack RPC client  
(originally 'Blendwarf' by Alef - http://www.bay12forums.com/smf/index.php?topic=178089.0)

## Usage

By default this package includes all of the code necessary to connect to DFHack (version 51.13-r1) through its custom RPC protocal. Use the following steps to test this out.

### Clone dfhack-client-python Repository

```bash
git clone https://github.com/McArcady/dfhack-client-python.git
```

### Install dfhack-client-python

```bash
cd dfhack-client-python
pip install .
```

### Run Dwarf Fortress with DFHack

At this point make sure both Dwarf Fortress and DFHack are installed. Open Dwarf Fortress and load into a game (the game can be paused).

### Run the Example Script

```bash
python ./example/blendwarf.py
```
If everything is working and you have successfully connected to your game via RPC, you will see a print out containing the number of units in your currently open game!

## Development

In order to make changes to this package or generate python files for other version of DFHack. Follow the steps below.

### Requirements

- python 3
- cmake
- protobuf

### Fetch Protobuf Files (Optional)

If you need to fetch a different version of .proto files, you can run the `./scripts/fetch_proto_files.py` script. You must pass a valid DFHack tag name as an argument.
```bash
python ./scripts/fetch_proto_files.py --tag="51.13-r1"
```
*This will dump all `.proto` files into the `./proto/51.13-r1/` directory*

### Generate Python Protobuf Code

To generate the necessary python files from the `./proto/<tag>/` directory, run the `./scripts/generate_python.py` script. You must pass the `<tag>` in as an argument

```bash
python ./scripts/generate_python.py --tag="51.13-r1"
```
*This will generate one python file in `./src/dfhack_client_python/py_export/` per .proto file in `./proto/<tag>/` for the provided `<tag>`*

### Install the Package

Now that all the python code is generated, make sure to install the package

```bash
pip install -e .
```

### Test Your Changes
At this point you can run the `./examples/blendwarf.py` script to test your changes. Make sure Dwarf Fortress is running, DFHack is installed, and you are loaded into a game.
```bash
python ./examples/blendwarf.py
```
