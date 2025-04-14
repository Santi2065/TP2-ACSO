def cuenta(target, words, lo, hi):
    if lo > hi:
        raise ValueError("Rango inválido: la búsqueda debería explotar la bomba.")
    mid = (lo + hi) // 2   # Esto equivale al cálculo de (low & high) + ((low ^ high) >> 1)
    mid_word = words[mid]
    # Usamos una comparación lexicográfica similar a strcmp:
    # Devuelve -1 si target < mid_word, 0 si son iguales y 1 si target > mid_word.
    cmp_result = (target > mid_word) - (target < mid_word)
    ascii_val = ord(mid_word[0])  # valor del primer carácter de la palabra en la posición media
    if cmp_result == 0:
        # Base: si la palabra coincide, se retorna el valor del primer carácter
        return ascii_val
    elif cmp_result > 0:
        # Si target es mayor, se busca en la mitad superior.
        if hi <= mid:
            raise ValueError("Bomba explota: cota superior inválida en búsqueda superior.")
        # Se suma el valor del carácter actual y se continúa la búsqueda en [mid+1, hi]
        return ascii_val + cuenta(target, words, mid + 1, hi)
    else:
        # Si target es menor, se busca en la mitad inferior.
        if lo >= mid:
            raise ValueError("Bomba explota: cota inferior inválida en búsqueda inferior.")
        return ascii_val + cuenta(target, words, lo, mid - 1)

def main():
    # Lee el archivo 'palabras.txt' y genera una lista de palabras (líneas, sin espacios en blanco)
    try:
        with open("palabras.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("No se encontró 'palabras.txt'. Asegúrate de que el archivo esté en el mismo directorio.")
        return

    n = len(lines)
    print(f"Se encontraron {n} palabras en 'palabras.txt'.")
    
    # Aquí podrías asumir que el rango de búsqueda es todo el arreglo.
    # En la bomba, el límite superior se calcula como (número ingresado - 1).
    # Normalmente, se espera que la entrada (número) sea igual a cuenta(...).
    # Como guía, buscamos candidatos cuyos resultados estén entre 401 y 799.
    rango_min = 401
    rango_max = 799

    # Para automatizar, podemos iterar por cada palabra candidata (del propio archivo)
    # y ver cuál produce un resultado dentro del rango.
    # En muchos bomb labs la clave no es una palabra existente, pero este es un buen punto de partida.
    print("Probando palabras del archivo para ver qué resultados dan:")
    for candidate in lines:
        try:
            resultado = cuenta(candidate, lines, 0, n - 1)
        except ValueError:
            continue
        if rango_min <= resultado <= rango_max:
            print(f"Candidato: '{candidate}' --> Resultado: {resultado}")
    
    # Si no encuentras resultados “aceptables” entre las palabras del archivo,
    # podrías considerar probar pequeñas variaciones (por ejemplo, modificando una letra)
    # o iterar sobre un conjunto predefinido de candidatos.
    #
    # Otra estrategia es usar GDB con Python para inspeccionar en tiempo real los parámetros
    # y el camino de la búsqueda binaria en memoria.

if __name__ == "__main__":
    main()