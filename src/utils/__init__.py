def binary(a, length:int=None) -> str:
    if length != None:
        return '{0:0{1}b}'.format(a, length)
    else:
        return bin(a).removeprefix('0b')