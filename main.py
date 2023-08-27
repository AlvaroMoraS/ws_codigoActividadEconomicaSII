import csv
import requests
from bs4 import BeautifulSoup

#--=============capturo datos de Actividad Económica desde sitio web del SII================--
r = requests.get('https://www.sii.cl/ayudas/ayudas_por_servicios/1956-codigos-1959.html').text #con ".text" extraigo el código HTML
soup = BeautifulSoup(r, "lxml") #la documentación de BeautifulSoup recomienda usar "lxml" por su velocidad.


#--=============función para limpiar saltos de línea y espacios de un texto================--
def limpiarTexto(texto):
    textoSinN = texto.replace("\n", "")
    textoSinR = textoSinN.replace("\r", "")
    textoSinEspaciosEnExtremos = textoSinR.strip() #elimina espacio de los extremos
    textoSinEspaciosEnMedio = ' '.join(textoSinEspaciosEnExtremos.split()) #divide el texto por palabra, y luego los une con un espacio en medio
    return textoSinEspaciosEnMedio


#--=============rubros económicos (nivel 1)================--
rubroEconomico_html = soup.find_all('font') #busco por "font" porque se observa que todos los rubros económicos tienen un tag de <font>

rubroEconomico = list()
for i in rubroEconomico_html:
    rubroEconomico.append(limpiarTexto(i.text))
#print(rubroEconomico)


#--=============ahora que tengo los rubros económicos, tengo que almacenar todos los "td" de la tabla en una lista que represente cada fila ("tr")============--
tr_html = soup.find_all('tr')

tabla = list()
for fila in tr_html:
    filaRecorrida = []
    for columna in fila.find_all('td'):
        filaRecorrida.append(limpiarTexto(columna.text))
    tabla.append(filaRecorrida)
"""
for fila in tabla:
    print(fila)
"""

#--=============buscar subtipo de Rubro Económico (nivel 2)================--

numFila = 0
subRubroEconomico = list()

for fila in tabla:
    for celda in fila:
        if celda == 'Código':
            subRubroEconomico.append(tabla[numFila][1])
    numFila += 1

"""
for registro in subRubroEconomico:
    print(registro)
"""


#--=============aquí armo la lista final ya depurada, con los niveles de rubro económico 1 y 2 como primeros elementos================--
filaRubroEco = -1
filaSubRubroEco = -1 
nFila = 0

tablaDepurada = list()

for fila in tabla:
    if fila==[]:
        filaRubroEco += 1
        nFila += 1
        continue
    else:
        for celda in fila:
            if celda == 'Código':
                filaSubRubroEco += 1
            
        filaRecorrida = []
        filaRecorrida = fila
        filaRecorrida.insert(0,subRubroEconomico[filaSubRubroEco])
        filaRecorrida.insert(0,rubroEconomico[filaRubroEco])
        tablaDepurada.append(filaRecorrida)

    nFila += 1
"""
for x in tablaDepurada:
    print(x)
"""

#--=============elimino los elementos de la lista que tengan un valor en la posición 2 con valor igual a "Código"================--
i = 0
#tablaDepurada.pop(0)
for i in range(0, len(tablaDepurada)):
    if i == len(tablaDepurada):
        break
    if tablaDepurada[i][2] == 'Código':
        tablaDepurada.pop(i)
        i -= 1
"""
for i in tablaDepurada:
    print(i)
"""

#--=============genero el encabezado que usaré para el CSV, lo inserto como primer registro de la lista, y genero el archivo CSV================--
encabezados = ['Rubro Económico', 'Subtipo Rubro Económico', 'Código Actividad Económica', 'Actividad Económica', 'Afecto a IVA', 'Categoría Tributaria', 'Disponible Internet']

tablaDepurada.insert(0,encabezados)

with open('codigosActividadEconomicaSII.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='|') #utilizo un pipe (|) como separador entre valores, ya que hay textos con comas(,), y punto y coma(;).
    writer.writerows(tablaDepurada)

print("*"*30)
print("Archivo generado exitosamente")
print("*"*30)
