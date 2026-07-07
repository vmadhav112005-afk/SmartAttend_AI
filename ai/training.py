import face_recognition
import os
import pickle
import numpy as np
import logging
from database.db import DatabaseManager

class FaceTrainer:
    def __init__(self, dataset_path="dataset", model_path="models"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.dataset_path = os.path.join(base_dir, dataset_path)
        self.model_path = os.path.join(base_dir, model_path)
        self.db = DatabaseManager()
        
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)

    def train_model(self, progress_callback=None):
        """
        Scans dataset/, extracts encodings, averages them, 
        updates the database and dumps to encodings.pkl.
        """
        known_encodings = []
        known_names = []
        known_ids = []

        if not os.path.exists(self.dataset_path) or not os.listdir(self.dataset_path):
            logging.warning("Training attempt with empty dataset.")
            return False, "No student datasets found. Please register students first."

        folders = [f for f in os.listdir(self.dataset_path) if os.path.isdir(os.path.join(self.dataset_path, f))]
        total_folders = len(folders)
        
        if total_folders == 0:
            return False, "No registered student folders found."

        for i, folder in enumerate(folders):
            folder_path = os.path.join(self.dataset_path, folder)
            try:
                # Format: student_id_name
                student_id, name = folder.split('_', 1)
            except ValueError:
                logging.error(f"Skipping folder {folder} due to naming mismatch (expected ID_Name).")
                continue

            image_files = [img for img in os.listdir(folder_path) if img.endswith(('.jpg', '.png', '.jpeg'))]
            student_encodings = []

            for img_file in image_files:
                img_path = os.path.join(folder_path, img_file)
                try:
                    image = face_recognition.load_image_file(img_path)
                    encodings = face_recognition.face_encodings(image)
                    if len(encodings) > 0:
                        student_encodings.append(encodings[0])
                except Exception as e:
                    logging.error(f"Error encoding image {img_file}: {e}")

            if student_encodings:
                avg_encoding = np.mean(student_encodings, axis=0)
                known_encodings.append(avg_encoding)
                known_names.append(name)
                known_ids.append(student_id)
                
                # Update DB student record
                encoding_blob = pickle.dumps(avg_encoding)
                self.db.update_student_encoding(student_id, encoding_blob)
            
            if progress_callback:
                progress_callback((i + 1) / total_folders)

        if not known_encodings:
            return False, "No faces could be encoded successfully from the datasets."

        # Save to models/encodings.pkl
        try:
            data = {"encodings": known_encodings, "names": known_names, "ids": known_ids}
            model_file = os.path.join(self.model_path, "encodings.pkl")
            with open(model_file, "wb") as f:
                pickle.dump(data, f)
            logging.info(f"Model successfully saved to {model_file}")
            return True, "Model trained successfully."
        except Exception as e:
            logging.error(f"Failed to save model: {e}")
            return False, f"Model save error: {str(e)}"
