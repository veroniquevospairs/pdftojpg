from flask import Flask, request, render_template
import fitz
from PIL import Image
from io import BytesIO
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    pdf_file = request.files['pdf_file']
    pdf_file_path = os.path.join('templates/static', pdf_file.filename)
    pdf_file.save(pdf_file_path)

    output_folder = "templates/static"
    convert_pdf_to_jpg(pdf_file_path, output_folder)
    return "Conversion terminée. Vérifiez le dossier 'static' pour les images."

import os

def convert_pdf_to_jpg(pdf_file, output_folder):
    pdf_document = fitz.open(pdf_file)
    
    # Obtenez le nom du fichier PDF sans l'extension
    pdf_file_name = os.path.splitext(os.path.basename(pdf_file))[0]
    
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            base_image = pdf_document.extract_image(img[0])
            image_data = base_image["image"]
            image_bytes = BytesIO(image_data)
            image = Image.open(image_bytes)
            
            # Construisez le chemin du fichier image avec le même nom que le fichier PDF
            image_path = f"{output_folder}/{pdf_file_name}_page_{page_number + 1}_image_{img_index + 1}.jpg"
            
            image.save(image_path, "JPEG")
            print(f"Image saved: {image_path}")
    
    pdf_document.close()




if __name__ == '__main__':
    app.run(debug=True)

