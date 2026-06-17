from ip_validator import validate_ip

def _ipv4_to_int(ip: str) -> int:    
    octets = map(int, ip.split("."))    
    res = 0    
    
    for o in octets:
        res = (res << 8) + o
        
    return res

def _find_min_mask_ipv4_xor(ip1: str, ip2: str) -> int:
    int1 = _ipv4_to_int(ip1)
    int2 = _ipv4_to_int(ip2)    
    # XOR подсветит единицей первое несовпадение слева
    diff = int1 ^ int2    
    # Если адреса абсолютно идентичны, общая маска максимальна
    if diff == 0:
        return 32        
    # diff.bit_length() показывает длину отличающегося хвоста справа.
    # Вычитаем этот "хвост" и получаем количество общих бит слева.
    return 32 - diff.bit_length()

def _ipv6_to_int(ip: str) -> int:
    hexes = map(lambda x: int(x, 16), ip.split(":"))
    res = 0
    
    for h in hexes:
        res = (res << 16) + h
        
    return res

def _find_min_mask_ipv6_xor(ip1, ip2):
    int1 = _ipv6_to_int(ip1)
    int2 = _ipv6_to_int(ip2)

    diff = int1 ^ int2
    
    if diff == 0:
        return 128
        
    return 128 - diff.bit_length()

def find_minimal_mask(ip_a: str, ip_b: str):
    version_a, ip_a = validate_ip(ip_a)
    version_b, ip_b = validate_ip(ip_b)
    
    if version_a != version_b:
        raise TypeError(
            f"Невозможно сравнить адреса разных версий! "
            f"Первый адрес: IPv{version_a}, второй адрес: IPv{version_b}"
        )
        
    if version_a == 4:
        return _find_min_mask_ipv4_xor(ip_a, ip_b)
    else:
        return _find_min_mask_ipv6_xor(ip_a, ip_b)