# from flask import Flask, render_template, request, jsonify, send_file
# from flask_cors import CORS
# import pickle
# import os
# import SimpleITK as sitk
# import numpy as np
# from skimage import measure
# import trimesh
# import shutil

# app = Flask(__name__)
# CORS(app, origins='*')

# # Load the model (in this case, any required pre-trained data)
# model_path = "model.pkl"
# if os.path.exists(model_path):
#     with open(model_path, "rb") as model_file:
#         model = pickle.load(model_file)
#         print("Model loaded successfully.")
# else:
#     model = None
#     print("Model file not found.")

# # Path to your existing DICOM folder on your desktop
# dicom_dir = r"C:\Users\HP\Desktop\Test"

# # Ensure static folder exists
# static_dir = os.path.join(app.root_path, 'static')
# os.makedirs(static_dir, exist_ok=True)

# # Create an endpoint to process the DICOM folder and generate 3D model
# @app.route('/generate_3d_model', methods=['POST'])
# def generate_3d_model():
#     # Check if DICOM files are included in the request
#     if not os.path.exists(dicom_dir):
#         return jsonify({"error": "DICOM folder not found at the specified path."}), 400

#     # List all files in the directory (make sure they're DICOM files)
#     dicom_files = [f for f in os.listdir(dicom_dir) if f.endswith('.dcm')]
    
#     if not dicom_files:
#         return jsonify({"error": "No DICOM files found in the specified folder."}), 400

#     # Read the DICOM series
#     try:
#         reader = sitk.ImageSeriesReader()
#         dicom_file_paths = [os.path.join(dicom_dir, f) for f in dicom_files]
#         reader.SetFileNames(dicom_file_paths)
#         image = reader.Execute()
#         image_array = sitk.GetArrayFromImage(image)

#         # Apply segmentation and reconstruction logic (example thresholding)
#         segmented_volume = (image_array > 0.9)  # Modify threshold as needed
#         verts, faces, _, _ = measure.marching_cubes(segmented_volume, step_size=1)

#         # Save the 3D model to an STL file in the static folder
#         stl_file = os.path.join(static_dir, "output_modelll.stl")
#         mesh = trimesh.Trimesh(vertices=verts, faces=faces)
#         mesh.export(stl_file)
#     except Exception as e:
#         return jsonify({"error": f"Processing failed: {e}"}), 500

#     # Return the 3D model file for download
#     return send_file(stl_file, as_attachment=True)

# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == "__main__":
#     app.run(port=5000, debug=True)


# from flask import Flask, render_template, request, jsonify, send_file
# from flask_cors import CORS
# import os
# import tempfile
# import SimpleITK as sitk
# import numpy as np
# from skimage import measure
# import trimesh
# import logging

# app = Flask(__name__)
# CORS(app, origins='*')

# # Configure logging
# logging.basicConfig(level=logging.DEBUG, 
#                     format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# @app.route('/', methods=['GET'])
# def index():
#     """Render the main page with file upload capability."""
#     return render_template('index.html')

# @app.route('/generate_3d_model', methods=['POST'])
# def generate_3d_model():
#     """
#     Process uploaded DICOM files and generate a 3D model.
    
#     Returns:
#         Flask response with STL file or error message
#     """
#     # Check if files were uploaded
#     if 'dicom_files' not in request.files:
#         logger.error("No files uploaded")
#         return jsonify({"error": "No files uploaded"}), 400
    
#     # Get the list of uploaded files
#     uploaded_files = request.files.getlist('dicom_files')
    
#     if not uploaded_files or uploaded_files[0].filename == '':
#         logger.error("No files selected")
#         return jsonify({"error": "No files selected"}), 400
    
#     # Create a temporary directory to store uploaded DICOM files
#     with tempfile.TemporaryDirectory() as temp_dicom_dir:
#         try:
#             # Save uploaded files to temporary directory
#             dicom_file_paths = []
#             for file in uploaded_files:
#                 # Ensure only DICOM files are processed
#                 if file.filename.lower().endswith('.dcm'):
#                     # Use the entire temporary directory, not a subdirectory
#                     file_path = os.path.join(temp_dicom_dir, file.filename)
                    
#                     # Log the intended save path
#                     logger.info(f"Attempting to save file to: {file_path}")
                    
#                     # Ensure the directory exists
#                     os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
#                     # Save the file
#                     file.save(file_path)
                    
#                     dicom_file_paths.append(file_path)
#                     logger.info(f"Saved DICOM file: {file_path}")
            
#             # Validate DICOM files
#             if not dicom_file_paths:
#                 logger.error("No valid DICOM files uploaded")
#                 return jsonify({"error": "No valid DICOM files uploaded"}), 400
            
#             # Log the file paths for debugging
#             logger.debug(f"DICOM file paths: {dicom_file_paths}")
            
#             # Read the DICOM series
#             reader = sitk.ImageSeriesReader()
#             reader.SetFileNames(dicom_file_paths)
#             image = reader.Execute()
#             image_array = sitk.GetArrayFromImage(image)

#             logger.info(f"Image array shape: {image_array.shape}")

#             # Advanced segmentation 
#             threshold = np.mean(image_array)  # Dynamic thresholding
#             logger.info(f"Threshold value: {threshold}")
            
#             segmented_volume = (image_array > threshold)

#             # Marching cubes for surface reconstruction
#             verts, faces, _, _ = measure.marching_cubes(segmented_volume, step_size=1)

#             logger.info(f"Vertices shape: {verts.shape}, Faces shape: {faces.shape}")

#             # Prepare output directory 
#             output_dir = os.path.join(app.root_path, 'static', 'output')
#             os.makedirs(output_dir, exist_ok=True)
            
#             # Save 3D model
#             stl_file = os.path.join(output_dir, "output_model.stl")
#             mesh = trimesh.Trimesh(vertices=verts, faces=faces)
#             mesh.export(stl_file)

#             logger.info(f"STL file saved: {stl_file}")

#             return send_file(stl_file, as_attachment=True)

#         except Exception as e:
#             logger.error(f"3D model generation error: {e}", exc_info=True)
#             return jsonify({"error": f"Processing failed: {str(e)}"}), 500

# if __name__ == "__main__":
#     app.run(port=5000, debug=True)




from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
import pickle
import SimpleITK as sitk
import numpy as np
from skimage import measure
import trimesh
import logging

app = Flask(__name__)
CORS(app, origins='*')

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Model loading function
def load_model(model_path):
    """
    Safely load a pre-trained model from a pickle file.
    
    Args:
        model_path (str): Path to the pickle file containing the model.
    
    Returns:
        object: Loaded model or None if loading fails
    """
    try:
        if os.path.exists(model_path):
            with open(model_path, "rb") as model_file:
                model = pickle.load(model_file)
                logger.info(f"Model loaded successfully from {model_path}")
                return model
        else:
            logger.error(f"Model file not found at {model_path}")
            return None
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None

# Load the model at application startup
MODEL_PATH = "model.pkl"
ML_MODEL = load_model(MODEL_PATH)

@app.route('/generate_3d_model', methods=['POST'])
def generate_3d_model():
    """
    Process uploaded DICOM files and generate a 3D model.
    
    Returns:
        Flask response with STL file or error message
    """
    # Check if files were uploaded
    if 'dicom_files' not in request.files:
        logger.error("No files uploaded")
        return jsonify({"error": "No files uploaded"}), 400
    
    # Get the list of uploaded files
    uploaded_files = request.files.getlist('dicom_files')
    
    if not uploaded_files or uploaded_files[0].filename == '':
        logger.error("No files selected")
        return jsonify({"error": "No files selected"}), 400
    
    # Create a temporary directory to store uploaded DICOM files
    with tempfile.TemporaryDirectory() as temp_dicom_dir:
        try:
            # Save uploaded files to temporary directory
            dicom_file_paths = []
            for file in uploaded_files:
                # Ensure only DICOM files are processed
                if file.filename.lower().endswith('.dcm'):
                    file_path = os.path.join(temp_dicom_dir, file.filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    file.save(file_path)
                    dicom_file_paths.append(file_path)
                    logger.info(f"Saved DICOM file: {file_path}")
            
            # Validate DICOM files
            if not dicom_file_paths:
                logger.error("No valid DICOM files uploaded")
                return jsonify({"error": "No valid DICOM files uploaded"}), 400
            
            # Read the DICOM series
            reader = sitk.ImageSeriesReader()
            reader.SetFileNames(dicom_file_paths)
            image = reader.Execute()
            image_array = sitk.GetArrayFromImage(image)

            # Model-based processing (if model is loaded)
            if ML_MODEL:
                try:
                    # Example of potential model usage 
                    # This is a placeholder and depends on your specific model
                    logger.info("Applying ML model to image")
                    
                    # Possible model applications:
                    # 1. Segmentation
                    # segmented_volume = ML_MODEL.predict(image_array)
                    
                    # 2. Feature extraction
                    # features = ML_MODEL.extract_features(image_array)
                    
                    # 3. Custom preprocessing
                    # processed_array = ML_MODEL.preprocess(image_array)
                    
                    # Placeholder: use mean thresholding if no specific model logic
                    threshold = np.mean(image_array)
                    segmented_volume = (image_array > 0.5)
                
                except Exception as model_error:
                    logger.warning(f"Model processing failed: {model_error}")
                    # Fallback to default thresholding
                    threshold = np.mean(image_array)
                    segmented_volume = (image_array > threshold)
            else:
                # Default processing if no model is loaded
                logger.warning("No ML model loaded. Using default thresholding.")
                threshold = np.mean(image_array)
                segmented_volume = (image_array > 0.5)

            # Marching cubes for surface reconstruction
            verts, faces, _, _ = measure.marching_cubes(segmented_volume, step_size=1)

            # Prepare output directory 
            output_dir = os.path.join(app.root_path, 'static', 'output')
            os.makedirs(output_dir, exist_ok=True)
            
            # Save 3D model
            stl_file = os.path.join(output_dir, "final.stl")
            mesh = trimesh.Trimesh(vertices=verts, faces=faces)
            mesh.export(stl_file)

            return send_file(stl_file, as_attachment=True)

        except Exception as e:
            logger.error(f"3D model generation error: {e}", exc_info=True)
            return jsonify({"error": f"Processing failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)