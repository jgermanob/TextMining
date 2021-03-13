# 1. Lectura del archivo trabalenguas.txt #
input_file = open('trabalenguas.txt', 'r').read()

# 2. Extraer trabalenguas en una sola línea, eliminar las comillas #
input_file = input_file.split('\n')

tongue_twister = []

for line in input_file:
    if line != '':
        if line[0] == '"':
            line = line[1:len(line)-1]
            tongue_twister.append(line)

# 3. Impresión de trabalenguas #
for tt in tongue_twister:
    print(tt) 
