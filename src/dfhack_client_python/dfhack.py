"""
Interfaces for DFHack functions available through its RPC connection.
"""

from dfhack_client_python.dfhack_remote import remote

# Core Protocol imports
from dfhack_client_python.py_export.CoreProtocol_pb2 import (
    StringMessage, EmptyMessage, IntMessage, CoreBindRequest, CoreBindReply,
    CoreRunCommandRequest, CoreRunLuaRequest, StringListMessage
)

# Basic API imports  
from dfhack_client_python.py_export.BasicApi_pb2 import (
    GetWorldInfoOut, ListEnumsOut, ListJobSkillsOut, ListMaterialsIn,
    ListMaterialsOut, ListUnitsIn, ListUnitsOut, ListSquadsIn, 
    ListSquadsOut, SetUnitLaborsIn
)

# Remote Fortress Reader imports
from dfhack_client_python.py_export.RemoteFortressReader_pb2 import (
    UnitList, MaterialList, BlockRequest, BlockList, TiletypeList, PlantList,
    ViewInfo, MapInfo, BuildingList, WorldMap, RegionMaps, CreatureRawList,
    ListRequest, PlantRawList, ScreenCapture, KeyboardEvent, DigCommand,
    SingleBool, VersionInfo, Status, Language
)

from dfhack_client_python.py_export.AdventureControl_pb2 import (
    MoveCommandParams, MenuContents, MiscMoveParams
)

# Dwarf Control imports
from dfhack_client_python.py_export.DwarfControl_pb2 import (
    SidebarState, SidebarCommand
)

## Core Protocol Methods
@remote
async def GetVersion(output: StringMessage = None): pass

@remote
async def GetDFVersion(output: StringMessage = None): pass

@remote
async def BindMethod(input: CoreBindRequest, output: CoreBindReply = None): pass

@remote
async def RunCommand(input: CoreRunCommandRequest): pass

@remote
async def CoreSuspend(output: IntMessage = None): pass

@remote
async def CoreResume(output: IntMessage = None): pass

@remote
async def RunLua(input: CoreRunLuaRequest, output: StringListMessage = None): pass

## Basic API Methods
@remote
async def GetWorldInfo(output: GetWorldInfoOut = None): pass

@remote
async def ListEnums(output: ListEnumsOut = None): pass

@remote
async def ListJobSkills(output: ListJobSkillsOut = None): pass

@remote
async def ListMaterials(input: ListMaterialsIn, output: ListMaterialsOut = None): pass

@remote
async def ListUnits(input: ListUnitsIn, output: ListUnitsOut = None): pass

@remote
async def ListSquads(input: ListSquadsIn, output: ListSquadsOut = None): pass

@remote
async def SetUnitLabors(input: SetUnitLaborsIn): pass

## Remote Fortress Reader Methods
@remote(plugin='RemoteFortressReader')
async def GetMaterialList(output: MaterialList = None): pass

@remote(plugin='RemoteFortressReader')
async def GetGrowthList(output: MaterialList = None): pass

@remote(plugin='RemoteFortressReader')
async def GetBlockList(input: BlockRequest, output: BlockList = None): pass

@remote(plugin='RemoteFortressReader')
async def CheckHashes(): pass

@remote(plugin='RemoteFortressReader')
async def GetTiletypeList(output: TiletypeList = None): pass

@remote(plugin='RemoteFortressReader')
async def GetPlantList(input: BlockRequest, output: PlantList = None): pass

@remote(plugin='RemoteFortressReader')
async def GetUnitList(output: UnitList = None): pass

@remote(plugin='RemoteFortressReader')
async def GetUnitListInside(input: BlockRequest, output: UnitList = None): pass

@remote(plugin='RemoteFortressReader')
async def GetViewInfo(output: ViewInfo = None): pass

@remote(plugin='RemoteFortressReader')
async def GetMapInfo(output: MapInfo = None): pass

@remote(plugin='RemoteFortressReader')
async def ResetMapHashes(): pass

@remote(plugin='RemoteFortressReader')
async def GetItemList(output: MaterialList = None): pass

@remote(plugin='RemoteFortressReader')
async def GetBuildingDefList(output: BuildingList = None): pass

@remote(plugin='RemoteFortressReader')
async def GetWorldMap(output: WorldMap = None): pass

@remote(plugin='RemoteFortressReader')
async def GetWorldMapNew(output: WorldMap = None): pass

@remote(plugin='RemoteFortressReader')
async def GetRegionMaps(output: RegionMaps = None): pass

@remote(plugin='RemoteFortressReader')
async def GetRegionMapsNew(output: RegionMaps = None): pass

@remote(plugin='RemoteFortressReader')
async def GetCreatureRaws(output: CreatureRawList = None): pass

@remote(plugin='RemoteFortressReader')
async def GetPartialCreatureRaws(input: ListRequest, output: CreatureRawList = None): pass

@remote(plugin='RemoteFortressReader')
async def GetWorldMapCenter(output: WorldMap = None): pass

@remote(plugin='RemoteFortressReader')
async def GetPlantRaws(output: PlantRawList = None): pass

@remote(plugin='RemoteFortressReader')
async def GetPartialPlantRaws(input: ListRequest, output: PlantRawList = None): pass

@remote(plugin='RemoteFortressReader')
async def CopyScreen(output: ScreenCapture = None): pass

@remote(plugin='RemoteFortressReader')
async def PassKeyboardEvent(input: KeyboardEvent): pass

@remote(plugin='RemoteFortressReader')
async def SendDigCommand(input: DigCommand): pass

@remote(plugin='RemoteFortressReader')
async def SetPauseState(input: SingleBool): pass

@remote(plugin='RemoteFortressReader')
async def GetPauseState(output: SingleBool = None): pass

@remote(plugin='RemoteFortressReader')
async def GetVersionInfo(output: VersionInfo = None): pass

@remote(plugin='RemoteFortressReader')
async def GetReports(output: Status = None): pass

@remote(plugin='RemoteFortressReader')
async def MoveCommand(input: MoveCommandParams): pass

@remote(plugin='RemoteFortressReader')
async def JumpCommand(input: MoveCommandParams): pass

@remote(plugin='RemoteFortressReader')
async def MenuQuery(output: MenuContents = None): pass

@remote(plugin='RemoteFortressReader')
async def MovementSelectCommand(input: IntMessage): pass

@remote(plugin='RemoteFortressReader')
async def MiscMoveCommand(input: MiscMoveParams): pass

@remote(plugin='RemoteFortressReader')
async def GetLanguage(output: Language = None): pass

@remote(plugin='RemoteFortressReader')
async def GetGameValidity(output: SingleBool = None): pass

## Dwarf Control Methods
@remote(plugin='RemoteFortressReader')
async def GetSideMenu(output: SidebarState = None): pass

@remote(plugin='RemoteFortressReader')
async def SetSideMenu(input: SidebarCommand): pass