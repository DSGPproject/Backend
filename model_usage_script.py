import tensorflow as tf
import sys
import numpy as np
from PIL import Image

def load_and_preprocess_image(image_path):
    # Load the image. Adjust this line to match your model's expected input dimensions.
    img = Image.open(image_path).resize((256, 256))  # Adjusted from 224x224 to 256x256
    img = np.array(img, dtype=np.float32) / 255.0  # Normalize the image if necessary
    img = np.expand_dims(img, axis=0)  # Add batch dimension if your model expects it
    return img

def run_model(model_path, image_path):
    # Load the TensorFlow model
    model = tf.saved_model.load(model_path)
    
    # Preprocess the image
    processed_img = load_and_preprocess_image(image_path)
    
    # Get the serving signature
    infer = model.signatures['serving_default']

    # Prepare input as a dictionary to match the expected input signature
    # The key should match the expected input tensor name. This may require you to check your model's signature.
    # Commonly, the input tensor name could be something like 'input_1', 'conv2d_input', etc.
    # If unsure, you can print(model.signatures['serving_default'].inputs) to inspect the expected input signature
    input_tensor_name = list(infer.structured_input_signature[1].keys())[0]
    pred = infer(**{input_tensor_name: tf.constant(processed_img, dtype=tf.float32)})

    # Extract and return the prediction. Adjust as necessary.
    # Here, we assume the model returns a dictionary with at least one output.
    prediction_result = pred[list(pred.keys())[0]]  # This accesses the first output of the prediction.
    return prediction_result.numpy()  # Convert to numpy array if needed

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python model_usage_script.py <model_path> <image_path>")
        sys.exit(1)
        
    model_path = sys.argv[1]  # Get model directory path from command line argument
    image_path = sys.argv[2]  # Get image path from command line argument

    prediction = run_model(model_path, image_path)
    print(prediction)  # Print the prediction. Adjust formatting as necessary.
