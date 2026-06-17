def validate_ip(ip: str) -> tuple[int, str]:
    if not ip or not isinstance(ip, str):
        raise ValueError("IP-адрес должен быть непустой строкой")
        
    if "." in ip:
        return 4, _validate_ipv4(ip)
    elif ":" in ip:
        return 6, _validate_ipv6(ip)
    else:
        raise ValueError("Некорректный сетевой адрес")

def _validate_ipv4(ip: str) -> str:
    parts = ip.strip().split(".")
    
    if len(parts) != 4:
        raise ValueError(f"IPv4 должен состоять из 4 групп, получено: {len(parts)}")
    
    for part in parts:
        if not part.isdigit():
            raise ValueError(f"IPv4 Каждая группа должна состоять только из цифр: {part}")
        if not (0 <= int(part) <= 255):
            raise ValueError(f"IPv4 Число должно быть в диапазоне от 0 до 255: {part}")
        if len(part) > 1 and part[0] == "0":
            raise ValueError(f"IPv4 Ведущие нули запрещены: {part}") 
        
    return ip
  
def _validate_ipv6(ip: str) -> str:
    if ":::" in ip:
        raise ValueError("IPv6 Некорректное сжатие ':::'")    
    if ip.count("::") > 1:
        raise ValueError("IPv6 Сжатие '::' может использоваться только один раз")
    
    parts = ip.strip().lower().split(":")
    filled_groups = [part for part in parts if part != ""]
    
    if "::" not in ip and len(parts) != 8:
        raise ValueError(f"IPv6 должен состоять из 8 групп, получено: {len(parts)}")    
    if "::" in ip: 
        if len(filled_groups) >= 8:
            raise ValueError(f"IPv6 Некорректное количество групп для сокращенной записи: {len(filled_groups)}")
        else:
            missing_groups = 8 - len(filled_groups)
            parts = _normalize_ipv6(parts, missing_groups)

    hexdigits = set("0123456789abcdef")
    normalized_parts = []
    
    for part in parts:
        if len(part) > 4:
            raise ValueError(f"IPv6 группа не может быть длиннее 4 символов: {part}")
        if not set(part).issubset(hexdigits):
            raise ValueError(f"IPv6 содержит недопустимые символы: {part}")
        
        normalized_parts.append(part.zfill(4))  
                           
    return ":".join(normalized_parts)

def _normalize_ipv6(ip_parts: list, missing_groups: int) -> list:
    result = []
    flag = False
    
    for part in ip_parts:
        if part == "":
            if not flag:
                result.extend(["0000"] * missing_groups)
                flag = True
            else: 
                continue
        else:
            result.append(part)
            
    return result
        
            