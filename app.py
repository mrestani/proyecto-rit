from flask import Flask, json,  request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os


UPLOAD_FOLDER = '/home/mariana/ws/proyecto-rit'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#metodo como index para seleccionar el archivo
@app.route('/', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':

        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            print('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))

    return render_template('index.html')


@app.route('/resultados-de-palabras', methods=['GET', 'POST'])
def mostrar_resultados():

    sel = request.form.get('comp_select')
    palabras = procesar_texto(sel)
    labels = ['adjetivos', 'pronombres', 'sustantivos', 'verbos', 'sin clasificar']
    legend = 'frecuencias'
    resultados = []

    for p in palabras:
        resultados.append(p)

    return render_template('grafico.html', values=resultados, labels=labels, legend=legend)


"""
Retornar el texto como un json
"""
@app.route('/texto', methods=['POST', 'GET'])
def obtener_texto():

    lineas_texto = []
    json_data = {}

    for arc in os.listdir('/home/mariana/ws/proyecto-rit'):

        if arc.endswith(".txt"):

            lineas_texto.append(arc)
            json_data = json.dumps([dict(name=arc) for l in lineas_texto])

            return json_data


def procesar_texto(texto):

    #listas de clasificaciones que se encuentren en el texto
    lista_de_verbos = []
    lista_de_adjetivos= []
    lista_de_pronombres = []
    lista_de_sustantivos = []

    #palabras sin clasificacion
    resto_de_palabras = []

    resultados = []

    with open(texto, "r") as t:

        adjetivos = get_adjetivos()
        pronombres = get_pronombres()
        sustantivos = get_sustantivos()
        verbos = get_verbos()

        for linea in t:
            for p in linea.split():
                palabra = formato_palabra(p)

                if palabra in adjetivos:
                    lista_de_adjetivos.append()
                elif palabra in pronombres:
                    lista_de_pronombres.append()
                elif palabra in sustantivos:
                    lista_de_sustantivos.append()
                elif palabra.endswith(verbos):
                    lista_de_verbos.append()

                #si no tiene clasificacion
                else:
                    resto_de_palabras.append()

    resultados.append(len(lista_de_adjetivos))
    resultados.append(len(lista_de_pronombres))
    resultados.append(len(lista_de_sustantivos))
    resultados.append(len(lista_de_verbos))

    print(resultados)
    return resultados


"""
Métodos para obtener las clasificaciones de las palabras
"""
def get_adjetivos():

    with open("adjetivos.txt", "r") as a:
        a.readlines()
        adjetivos = a.decode('utf-8').lower()
        return adjetivos


def get_pronombres():

    with open("pronombres.txt", "r") as p:
        p.readlines()
        pronombres = p.decode('utf-8').lower()
        return pronombres


def get_sustantivos():

    with open("sustantivos.txt", "r") as s:
        s.readlines()
        sustantivos = s.decode('utf-8').lower()
        return sustantivos


def get_verbos():

    with open("verbos.txt", "r") as v:
        v.readlines()
        verbos = v.decode('utf-8').lower()
        return verbos


#cambiar formato de palabras para que sean minusculas
# y sea facil de compararlas
def formato_palabra(palabra):

    palabra_min = palabra.lower()
    return palabra_min


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"))
