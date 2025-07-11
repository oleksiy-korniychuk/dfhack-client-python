import sys
import asyncio
from async_lru import alru_cache
from enum import IntEnum
from inspect import signature, Parameter

from .py_export.CoreProtocol_pb2 import EmptyMessage, CoreBindReply, CoreBindRequest, CoreTextNotification, CoreErrorNotification

_reader, _writer = None, None

class DFHackError(Exception):
    """Exception raised when a DFHack command fails"""
    def __init__(self, code, message=None):
        self.code = code
        try:
            self.code_name = CoreErrorNotification.ErrorCode.Name(code)
        except ValueError:
            self.code_name = f"Unknown({code})"
        self.message = message or f"DFHack command failed with error code: {self.code} ({self.code_name})"
        super().__init__(self.message)

class DFHackReplyCode(IntEnum):
    RPC_REPLY_RESULT = -1
    RPC_REPLY_FAIL   = -2
    RPC_REPLY_TEXT   = -3
    RPC_REQUEST_QUIT = -4

def header(id, size):
    return id.to_bytes(2, sys.byteorder, signed=True) + \
        b'\x00\x00' + \
        size.to_bytes(4, sys.byteorder)

async def get_header():
    h = await _reader.read(8)
    id = int.from_bytes(h[0:2], sys.byteorder, signed=True)
    size = int.from_bytes(h[4:8], sys.byteorder)
    
    # For RPC_REPLY_FAIL, the size field is reused for command_result
    if id == DFHackReplyCode.RPC_REPLY_FAIL:
        command_result = size
        raise DFHackError(command_result)
    
    return id, size

def request(id, msg):
    s = msg.SerializeToString()
    h = header(id, len(s))
    return h + s

def unmarshal(id, msg):
    if id == DFHackReplyCode.RPC_REPLY_RESULT:
        obj = CoreBindReply()
        obj.ParseFromString(msg)
        return obj.assigned_id
    elif id == DFHackReplyCode.RPC_REPLY_TEXT:
        obj = CoreTextNotification()
        obj.ParseFromString(msg)
        raise Exception(obj)
    elif id == DFHackReplyCode.RPC_REPLY_FAIL:
        error_code = int.from_bytes(msg, sys.byteorder, signed=True)
        raise DFHackError(error_code)
    else:
        raise DFHackError(f"Unknown reply code: {id}")

@alru_cache(maxsize=65534)
async def BindMethod(method, input_msg, output_msg, plugin=''):
    """Issue a CoreBindRequest to DFHack and caches the returned identifier number"""
    br = CoreBindRequest()
    br.method, br.input_msg, br.output_msg, br.plugin = \
        method, input_msg.DESCRIPTOR.full_name, output_msg.DESCRIPTOR.full_name, plugin
    _writer.write( request(0, br) )
    id, size = await get_header()
    return unmarshal(id, await _reader.read(size))

async def close():
    buf = header(DFHackReplyCode.RPC_REQUEST_QUIT, 0) + b'\x00\x00\x00\x00'
    _writer.write(buf) ; await _writer.drain()
    _writer.close() ; await _writer.wait_closed()

def handshake_request():
    n = 1
    return b'DFHack?\n' + n.to_bytes(4, sys.byteorder, signed=False)

async def connect():
    global _reader, _writer
    _reader, _writer = await asyncio.open_connection('127.0.0.1', 5000)
    _writer.write( handshake_request() )
    msg = await _reader.read(12)
    if b'DFHack!\n\x01\x00\x00\x00' != msg:  # handshake_reply
        _reader, _writer = None, None

def get_param_type(param):
    if param and param.annotation != Parameter.empty:
        return param.annotation
    return EmptyMessage

def remote(func=None, *, plugin=''):
    """Decorator for DFHack remote functions.
    
    Usage:
        @remote
        async def GetVersion(output: StringMessage = None): 
            pass
            
        @remote(plugin='RemoteFortressReader')
        async def GetVersionInfo(input: EmptyMessage = None, output: VersionInfo = None):
            pass
    """
    from functools import update_wrapper
    
    def decorator(f):
        params = signature(f).parameters
        input_type = get_param_type(params.get('input'))
        output_type = get_param_type(params.get('output'))

        async def wrapper(*args, **kwargs):
            _id = await BindMethod(f.__name__, input_type, output_type, plugin=plugin)
            input_value = kwargs.get('input') if kwargs.get('input') else input_type()
            _writer.write( request(_id, input_value) )

            # According to the protocol, the server may send zero or more RPC_REPLY_TEXT
            # messages followed by either RPC_REPLY_RESULT or RPC_REPLY_FAIL
            while True:
                id, size = await get_header()
                
                if id == DFHackReplyCode.RPC_REPLY_TEXT:
                    # Handle text notification
                    buffer = await _reader.read(size)
                    size -= len(buffer)
                    while size:
                        more = await _reader.read(size)
                        buffer += more
                        size -= len(more)
                    text_obj = CoreTextNotification()
                    text_obj.ParseFromString(buffer)
                    # Log text notifications to standard output
                    print(f"[INFO] DFHack: {text_obj.text}")
                    continue
                elif id == DFHackReplyCode.RPC_REPLY_RESULT:
                    # Handle successful result
                    buffer = await _reader.read(size)
                    size -= len(buffer)
                    while size:
                        more = await _reader.read(size)
                        buffer += more
                        size -= len(more)
                    obj = output_type()
                    obj.ParseFromString(buffer)
                    return obj
                elif id == DFHackReplyCode.RPC_REPLY_FAIL:
                    # This should have been handled in get_header(), but just in case
                    error_code = size
                    raise DFHackError(error_code)
                else:
                    raise DFHackError(f"Unexpected reply code: {id}")

        return update_wrapper(wrapper, f)
    
    if func is None:
        # Called as @remote(plugin='SomePlugin')
        return decorator
    else:
        # Called as @remote
        return decorator(func)
