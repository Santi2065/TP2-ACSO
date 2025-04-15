def cuenta(target, words, lo, hi):
    if lo > hi:
        raise ValueError("Rango inválido: la búsqueda debería explotar la bomba.")
    mid = (lo + hi) // 2   # Esto equivale al cálculo de (low & high) + ((low ^ high) >> 1)
    mid_word = words[mid]
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
    
    rango_min = 401
    rango_max = 799


    print("Probando palabras del archivo para ver qué resultados dan:")
    for candidate in lines:
        try:
            resultado = cuenta(candidate, lines, 0, n - 1)
        except ValueError:
            continue
        if rango_min <= resultado <= rango_max:
            print(f"Candidato: '{candidate}' --> Resultado: {resultado}")

if __name__ == "__main__":
    main()