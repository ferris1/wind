import ctypes

lib = ctypes.CDLL('./wnet.dll')

# Make python convert its values to C representation.
lib.StartNetThread.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
lib.StartNetThread.restype = ctypes.c_void_p


lib.StartNetThread(pyToNet, pyFromNet, ip, port)
