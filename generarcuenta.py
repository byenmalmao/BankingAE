import random

def generar_cuenta_fidebank():
    """
    Genera un número de cuenta bancaria para Fidebank con estructura identificable.
    
    Estructura propuesta para Fidebank:
    - BIN (6 dígitos): 456789 (ejemplo)
    - Identificación de sucursal (3 dígitos)
    - Tipo de cuenta (2 dígitos)
    - Número de cuenta (7 dígitos)
    - Dígito verificador (1 dígito)
    - Longitud total: 19 dígitos
    
    Returns:
        dict: Información completa de la cuenta generada
    """
    
    # BIN específico para Fidebank
    BIN_FIDEBANK = "100"
    
    # Tipos de cuenta para Fidebank
    tipos_cuenta = {
        'Ahorros': '01',
        'Corriente': '02',
        'Nómina': '03',
        'Plazo Fijo': '04',
        'Empresarial': '05'
    }
    
    # Seleccionar tipo de cuenta aleatoriamente
    tipo_nombre, codigo_tipo = random.choice(list(tipos_cuenta.items()))
    
    # Generar código de sucursal (3 dígitos)
  
    
    # Generar número de cuenta principal (7 dígitos)
    numero_cuenta = f"{random.randint(1, 9999999):07d}"
    
    # Crear número base sin dígito verificador
    base = BIN_FIDEBANK  + codigo_tipo + numero_cuenta
    
    # Calcular dígito verificador usando algoritmo Luhn (modificado)
    total = 0
    for i, digito in enumerate(base):
        num = int(digito)
        if i % 2 == 0:  # Posiciones pares (considerando 0-based)
            num *= 2
            if num > 9:
                num = (num // 10) + (num % 10)
        total += num
    
    digito_verificador = (10 - (total % 10)) % 10
    
    # Formatear número de cuenta completo
    numero_completo = f"{base}{digito_verificador}"
    
    
    
    # Formatear para mejor legibilidad
    numero_formateado = f"{BIN_FIDEBANK}{codigo_tipo} {numero_cuenta} {digito_verificador}"
    
    return numero_completo
    """"
    return {
        'banco': 'Fidebank',
        'bin': BIN_FIDEBANK,
        'numero_cuenta': numero_completo,
        'numero_formateado': numero_formateado,
        'sucursal': codigo_sucursal,
        'tipo_cuenta': tipo_nombre,
        'digito_verificador': digito_verificador,
        'longitud': len(numero_completo)
    }"""