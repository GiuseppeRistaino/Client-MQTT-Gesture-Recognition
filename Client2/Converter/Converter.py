import os, struct, binascii

'''
Convertitore da esadecimale a float da file
- file = file contenente i valori esadecimali
'''
def hexToFloat(file):
    sensors = []
    with open(file) as openfileobject:
        lines = ""
        for line in openfileobject:
            lines += line.rstrip('\n')
        vector = lines.split(",")
        # elimina i primi 8 byte
        for index, elem in enumerate(vector):
            del vector[0]
            if index == 7:
                break
        print vector
        iterator = 0
        for index, elem in enumerate(vector):
            if iterator == 2:
                id = vector[index]
            elif iterator == 6:
                try:
                    x_acc_hex = vector[index + 3] + vector[index + 2] + vector[index + 1] + vector[index]
                    x_acc_hex.strip('\n')
                    x_acc = struct.unpack("!f", x_acc_hex.decode('hex'))[0]
                    if str(x_acc).__contains__('e'):
                        x_acc = 0.0
                    print str(x_acc_hex) + " = " + str(x_acc)
                except IndexError:
                    x_acc = 'null'
            elif iterator == 10:
                try:
                    y_acc_hex = vector[index + 3] + vector[index + 2] + vector[index + 1] + vector[index]
                    y_acc_hex.strip('\n')
                    y_acc = struct.unpack("!f", y_acc_hex.decode('hex'))[0]
                    if str(y_acc).__contains__('e'):
                        y_acc = 0.0
                except IndexError:
                    y_acc = 'null'
            elif iterator == 14:
                try:
                    z_acc_hex = vector[index + 3] + vector[index + 2] + vector[index + 1] + vector[index]
                    z_acc_hex.strip('\n')
                    z_acc = struct.unpack("!f", z_acc_hex.decode('hex'))[0]
                    if str(z_acc).__contains__('e'):
                        z_acc = 0.0
                except IndexError:
                    z_acc = 'null'
            elif iterator == 18:
                try:
                    x_gir_hex = vector[index + 3] + vector[index + 2] + vector[index + 1] + vector[index]
                    x_gir_hex.strip('\n')
                    x_gir = struct.unpack("!f", x_gir_hex.decode('hex'))[0]
                    if str(x_gir).__contains__('e'):
                        x_gir = 0.0
                except IndexError:
                    x_gir = 'null'
            elif iterator == 22:
                try:
                    y_gir_hex = vector[index + 3] + vector[index + 2] + vector[index + 1] + vector[index]
                    y_gir_hex.strip('\n')
                    y_gir = struct.unpack("!f", y_gir_hex.decode('hex'))[0]
                    if str(y_gir).__contains__('e'):
                        y_gir = 0.0
                except IndexError:
                    y_gir = 'null'
            elif iterator == 26:
                try:
                    z_gir_hex = vector[index + 3] + vector[index + 2] + vector[index + 1] + vector[index]
                    z_gir_hex.strip('\n')
                    z_gir = struct.unpack("!f", z_gir_hex.decode('hex'))[0]
                    if str(z_gir).__contains__('e'):
                        z_gir = 0.0
                except IndexError:
                    z_gir = 'null'
            if iterator == 41:
                if id == '03' or id =='04' or id == '01' or id == '05':
                    sensors.append(
                        {'id': id, 'x_acc': x_acc, 'y_acc': y_acc, 'z_acc': z_acc, 'x_gir': x_gir, 'y_gir': y_gir,
                         'z_gir': z_gir})
                iterator = 0
            else:
                iterator += 1

    return sensors

'''
Scrive il file csv di tutti i nodi
sensors: lista delle osservazioni di tutti i nodi (lista di dizionari)
'''
def writeCSV(sensors):
    file = open("./csv/test.csv", 'w')
    for elem in sensors:
        #file.write(elem['id']+',')
        file.write(str(elem['x_acc']) +',')
        file.write(str(elem['y_acc']) +',')
        file.write(str(elem['z_acc']) +',')
        file.write(str(elem['x_gir']) +',')
        file.write(str(elem['y_gir']) +',')
        file.write(str(elem['z_gir']) +',')

'''
Scrive il file csv di un solo nodo
sensors: lista delle osservazioni di tutti i nodi (lista di dizionari)
node: id del nodo che si vuole prendere in considerazione
'''
def writeCSVForNode(sensors, node):
    file = open("./csv/test.csv", 'w')
    for elem in sensors:
        if (elem['id'] == node):
            file.write(elem['id']+',')
            file.write(str(elem['x_acc']) +',')
            file.write(str(elem['y_acc']) +',')
            file.write(str(elem['z_acc']) +',')
            file.write(str(elem['x_gir']) +',')
            file.write(str(elem['y_gir']) +',')
            file.write(str(elem['z_gir']) +'\n')

'''
Convertitore da esadecimale a float di una stringa
- line: stringa contenente i valori esadecimali separati da virgola
'''
def hexToFloatForLine(line):
    sensors = []
    vector = line.split(",")
    if len(vector) > 169:
        # elimina i primi 8 byte
        for index, elem in enumerate(vector):
            del vector[0]
            if index == 7:
                break
    iterator = 0
    for index, elem in enumerate(vector):
        if iterator == 2:
            id = vector[index]
        elif iterator == 6:
            try:
                x_acc_hex = vector[index + 3] + vector[index + 2] + vector[index + 1] + vector[index]
                x_acc_hex.strip('\n')
                x_acc = struct.unpack("!f", x_acc_hex.decode('hex'))[0]
                if str(x_acc).__contains__('e'):
                    x_acc = 0.0
            except IndexError:
                x_acc = 'null'
        elif iterator == 10:
            try:
                y_acc_hex = vector[index + 3] + vector[index + 2] + vector[index + 1] + vector[index]
                y_acc_hex.strip('\n')
                y_acc = struct.unpack("!f", y_acc_hex.decode('hex'))[0]
                if str(y_acc).__contains__('e'):
                    y_acc = 0.0
            except IndexError:
                y_acc = 'null'
        elif iterator == 14:
            try:
                z_acc_hex = vector[index + 3] + vector[index + 2] + vector[index + 1] + vector[index]
                z_acc_hex.strip('\n')
                z_acc = struct.unpack("!f", z_acc_hex.decode('hex'))[0]
                if str(z_acc).__contains__('e'):
                    z_acc = 0.0
            except IndexError:
                z_acc = 'null'
        elif iterator == 18:
            try:
                x_gir_hex = vector[index + 3] + vector[index + 2] + vector[index + 1] + vector[index]
                x_gir_hex.strip('\n')
                x_gir = struct.unpack("!f", x_gir_hex.decode('hex'))[0]
                if str(x_gir).__contains__('e'):
                    x_gir = 0.0
            except IndexError:
                x_gir = 'null'
        elif iterator == 22:
            try:
                y_gir_hex = vector[index + 3] + vector[index + 2] + vector[index + 1] + vector[index]
                y_gir_hex.strip('\n')
                y_gir = struct.unpack("!f", y_gir_hex.decode('hex'))[0]
                if str(y_gir).__contains__('e'):
                    y_gir = 0.0
            except IndexError:
                y_gir = 'null'
        elif iterator == 26:
            try:
                z_gir_hex = vector[index + 3] + vector[index + 2] + vector[index + 1] + vector[index]
                z_gir_hex.strip('\n')
                z_gir = struct.unpack("!f", z_gir_hex.decode('hex'))[0]
                if str(z_gir).__contains__('e'):
                    z_gir = 0.0
            except IndexError:
                z_gir = 'null'
        if iterator == 41:
            if id == '03' or id =='04' or id == '01' or id == '05':
                sensors.append(
                    {'id': id, 'x_acc': x_acc, 'y_acc': y_acc, 'z_acc': z_acc, 'x_gir': x_gir, 'y_gir': y_gir,
                     'z_gir': z_gir})
            iterator = 0
        else:
            iterator += 1

    return sensors