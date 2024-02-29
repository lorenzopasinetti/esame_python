class ExamException(Exception):
    pass


class CSVTimeSeriesFile():
    def __init__(self, name):
        self.name = name


    def get_data(self):
        try:
            my_file = open(self.name,'r')
            my_file.readline()
            righe = 0
            for riga in my_file: 
                righe = righe + 1
            if righe == 0:
                raise ExamException('Il file è vuoto')

        except Exception as e:
            raise ExamException('Errore in apertura del file:') from e
        else: 
            list = []
            my_file = open(self.name, 'r')
            for linea in my_file:
                linea = linea.strip()

                if linea and ',' in linea:
                    elements = linea.split(",")
                    verifica = True
                    verifica_2 = True
                    if elements[0]!= 'date' and elements[1].isdigit() and '-' in elements[0]:
                        anno_corrente = elements[0].split("-")[0]
                        mese_corrente = elements[0].split("-")[1]
                        int(anno_corrente)
                        int(mese_corrente)
                        for item in list:
                            if elements[0] == item[0]:
                                verifica = False
                            anno_precedente = item[0].split("-")[0]
                            mese_precedente = item[0].split("-")[1]
                            if anno_corrente < anno_precedente:
                                verifica_2 = False
                            if anno_corrente == anno_precedente and mese_corrente<mese_precedente:
                                verifica_2 = False
                        if not verifica:
                            raise ExamException('Ci sono elementi ripetuti')
                        else:
                            if not verifica_2:
                                raise ExamException('La serie non è ordinata')
                            else:
                                list.append([elements[0], int(elements[1])])
            if list == []:
                raise ExamException('La lista è vuota')
                
            my_file.close()
            return list


def find_min_max(time_series):
    esterno = {}
    val_min = 0
    val_max = 0
    min = []
    max = []
    for element in time_series:             
        anno = element[0].split("-")[0]
        mese = element[0].split("-")[1]
        if anno not in esterno:
            min = []
            max = []
            val_min = element[1]
            val_max = element[1]
            min.append(mese)
            max.append(mese)
            interno = {"min": min, "max":max}
            esterno[anno] = interno
        else:
            if element[1]>val_max:
                max = []
                val_max = element[1]
                max.append(mese)
            else: 
                if element[1] == val_max:
                    max.append(mese)

            if element[1]<val_min:
                min = []
                val_min = element[1]
                min.append(mese)
            else:
                if element[1] == val_min:
                    min.append(mese)
            interno = {"min": min, "max":max}
            esterno[anno] = interno
    return esterno

my_file = 'data.csv'
file = CSVTimeSeriesFile(my_file)
time_series = file.get_data()
print(find_min_max(time_series))