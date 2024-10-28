import tensorflow as tf
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
import os
import traceback

# Ruta al modelo guardado
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models/modelo_pre.h5')

# Cargar el modelo
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print('Modelo cargado correctamente')
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Nombres de las clases (reemplaza con las clases de tu modelo)
class_names = ['Bebidas', 'Carne', 'Frutas', 'Lacteos', 'Licores', 'Menestras', 'Verduras']  # Ajusta los nombres según tus clases

def predict_image(image_path):
    img_height, img_width = 180, 180  # Usa las mismas dimensiones que en el entrenamiento
    try:
        print(f"Procesando imagen en: {image_path}")
        # Cargar y preprocesar la imagen
        img = load_img(image_path, target_size=(img_height, img_width))
        print('Imagen procesada correctamente')
        img_array = img_to_array(img)
        print(f"Dimensiones de la imagen después de convertir a array: {img_array.shape}")
        img_array = np.expand_dims(img_array, axis=0)  # Crear un batch de tamaño 1
        print(f"Dimensiones de la imagen después de expandir: {img_array.shape}")

        # Hacer la predicción
        predictions = model.predict(img_array)
        print(f"Predicción obtenida: {predictions}")
        score = tf.nn.softmax(predictions[0])
        print(f"Score después de aplicar softmax: {score}")

        return class_names[np.argmax(score)], 100 * np.max(score)
    except Exception as e:
        print(f"Error during prediction: {e}")
        traceback.print_exc()  # Mostrar la traza completa del error en la consola
        return None, None

def image_classification_view(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']
        image_path = f'temp/{image.name}'

        # Asegurarse de que el directorio temporal existe
        if not os.path.exists('temp'):
            os.makedirs('temp')

        try:
            # Guardar la imagen temporalmente
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            print(f"Imagen guardada temporalmente en: {image_path}")

            # Realizar predicción
            class_name, confidence = predict_image(image_path)

            # Eliminar la imagen después de la predicción
            os.remove(image_path)

            # Verificar si la predicción fue exitosa
            if class_name is not None and confidence is not None:
                return JsonResponse({
                    'class_name': class_name,
                    'confidence': float(confidence)  # Convertir a float
                })
            else:
                print("Error durante la predicción. Resultado inválido.")
                return JsonResponse({
                    'error': 'Error during prediction. Please try again.'
                }, status=500)
        except Exception as e:
            # Mostrar la traza completa del error
            print(f"Error handling the image: {e}")
            traceback.print_exc()  # Mostrar la traza completa del error en la consola
            if os.path.exists(image_path):
                os.remove(image_path)
            return JsonResponse({
                'error': 'An error occurred while processing the image.'
            }, status=500)

    return render(request, 'clasificacion.html')

