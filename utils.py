import time

def type_check (val, Type):
    if Type == 'dict':
        return isinstance(val, dict)
    if Type == 'list':
        return isinstance(val, list)
    if Type == 'str':
        return isinstance(val, str)
    if Type == 'int':
        return isinstance(val, int)

def object_check (obj, key, Type):
  if not type_check (obj, 'dict') or not key in obj:
     return False
  return type_check (obj [key], Type)

def timems ():
    return int(round(time.time() * 1000))
