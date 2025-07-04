import asyncio
# Import connection management functions
from dfhack_client_python.dfhack_remote import remote, connect, close
# Import protobuf message types
from dfhack_client_python.py_export.CoreProtocol_pb2 import StringMessage
from dfhack_client_python.py_export.RemoteFortressReader_pb2 import UnitList

## Declare DFHack exported interfaces
@remote
async def GetVersion(output: StringMessage = None): pass

@remote(plugin='RemoteFortressReader')
async def GetUnitList(output: UnitList = None): pass

# Test
async def main():
    await connect()
    print( "DFHack Version: ", (await GetVersion()).value )
    print( "Units: ", len((await GetUnitList()).creature_list))
    await close()

asyncio.run(main())
