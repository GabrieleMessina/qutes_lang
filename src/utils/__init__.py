def binary(a:int, length:int=None) -> str:
    if length != None:
        return '{0:0{1}b}'.format(a, length)
    else:
        return bin(a).removeprefix('0b')
    
def flatten_list(a:list) -> list:
    return [item for sublist in a for item in sublist]

def is_power_of_two(n):
    return (n != 0) and (n & (n-1) == 0)