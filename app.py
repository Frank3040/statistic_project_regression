from flask import Flask, render_template, request, send_file,session
import os
from scripts.limpieza_script import Manager

# Creamos una instancia de la clase Flask
app = Flask(__name__)
# Establecemos la carpeta en la que se guardarán los archivos
app.config['UPLOAD_FOLDER'] = 'saved_files'
app.secret_key = 'tu_clave_secreta'
# Establecemos el tipo de achivo que será aceptado
ALLOWED_EXTENSIONS = {'csv'}
# Función para verificar la extensión del archivo
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Obtener la ruta al directorio actual del script
current_directory = os.path.dirname(os.path.abspath(__file__))
print(current_directory)
upload_folder = os.path.join(current_directory, app.config['UPLOAD_FOLDER'])
print(upload_folder)

# Asegurarse de que el directorio 'saved_files' exista
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No selected file')
    
    if file and allowed_file(file.filename):
        # Asegurarse de que el nombre de archivo sea seguro antes de guardarlo
        file_path = os.path.join(upload_folder, 'input.csv')
        file.save(file_path)
        return render_template('index.html', success=True)

    return render_template('index.html', error='Invalid file type. Please upload a CSV file.')

@app.route('/limpieza')
def limpieza():
    input_path = os.path.join(upload_folder, 'input.csv')
    
    output_path = os.path.join(upload_folder, 'dataset_limpio.csv')

    Datos = Manager(input_path)
    limpieza_result = Datos.LimpiezaTotal()
    # Guarda el archivo limpio
    limpieza_result.to_csv(output_path, index=False)
    return render_template('index.html', limpieza_success=True)

@app.route('/download')
def download():
    output_path = os.path.join(upload_folder, 'dataset_limpio.csv')
    return send_file(output_path, as_attachment=True)

@app.route('/entrenamiento', methods=['GET', 'POST'])
def entrenamiento():
    input_path = os.path.join(upload_folder, 'dataset_limpio.csv')
    output_path = os.path.join(upload_folder, 'model_report.txt')
    resultado = None
    error = None

    if request.method == 'POST':
        try:
            # Obtener el número decimal del formulario
            num1 = float(request.form['num1'])
            session['numero'] = num1
            # Validar que esté dentro del rango 0.10 a 0.90
            if 0.10 <= num1 <= 0.90:
                # Realizar la función
                Datos = Manager(input_path)
                modelo = Datos.train_and_evaluate_model(num1)
                # Supongamos que text_report es el resultado de self.lr_model.summary()
                text_report = modelo.summary()
                # Convertir el resultado a texto
                text_data = str(text_report)
                # Guardar el texto en un archivo
                file_path = output_path  # Reemplaza con la ruta deseada
                
                with open(file_path, "w") as file:
                    file.write(text_data)
                    
                resultado = f"Operación exitosa con el número {num1}"
            else:
                error = "El número decimal debe estar entre 0.10 y 0.90"

        except ValueError:
            error = "Ingrese un número decimal válido."
        except Exception as e:
            error = str(e)
            
    return render_template('index.html', resultado=resultado, error2=error)

@app.route('/downloadd')
def download2():
    output_path = os.path.join(upload_folder, 'model_report.txt')
    return send_file(output_path, as_attachment=True)

@app.route("/prediccion", methods=['GET','POST'])
def prediccion():
    input_path = os.path.join(upload_folder, 'input.csv')
    resultado2 = None
    error = None

    if request.method == 'POST':
        
        # Obtener el número decimal del formulario
        yr = int(request.form['valor1'])
        worday = int(request.form['valor2'])
        tem = float(request.form['valor3'])
        atem = float(request.form['valor4'])
        hum = float(request.form['valor5'])
        winspe = float(request.form['valor6'])
        ssn2 = int(request.form['valor7'])
        ssn3 = int(request.form['valor8'])
        ssn4 = int(request.form['valor9'])
        mnt3 = int(request.form['valor10'])
        mnt9 = int(request.form['valor11'])
        mnt10 = int(request.form['valor12'])
        wday6 = int(request.form['valor13'])
        wdsh2 = int(request.form['valor14'])
        wdsh3 = int(request.form['valor15'])         
        # Realizar la función
        Datos = Manager(input_path)
        Datos.LimpiezaTotal()
        num1 = session.get('numero')
        model = Datos.train_and_evaluate_model(num1)
        input_features = [yr,worday,tem,atem,hum,winspe,ssn2,ssn3,ssn4,mnt3,mnt9,mnt10,wday6,wdsh2,wdsh3]
        print(input_features)
        prediction = Datos.predict_single_value(input_features)
        predictionf = float(prediction)
        resultado = f"El resultado de la predicción es: {predictionf}"
                     
    return render_template('index.html', resultado2=resultado, error3=error)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")