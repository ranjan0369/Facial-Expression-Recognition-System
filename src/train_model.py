import os
import cv2
import glob as gb
import random
import numpy as np

# List of emotions
emojis = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"] 

# Initialize fisher face classifier
fisher_face = cv2.face.FisherFaceRecognizer_create()

os.makedirs("result", exist_ok=True)

def get_files(emotion, data_dir="facial-dataset/train"):
    """Get training and validation files for an emotion."""
    files = gb.glob(os.path.join(data_dir, emotion, "*"))
    random.shuffle(files)
    split_idx = int(len(files)*0.67)
    training = files[:split_idx]
    validation = files[split_idx:]
    return training, validation

def load_images(file_list):
    """Load images as grayscale numpy arrays."""
    images = []
    for f in file_list:
        img = cv2.imread(f)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        images.append(gray)
    return images

def prepare_dataset():
    """Prepare training and validation datasets."""
    training_data, training_labels = [], []
    validation_data, validation_labels = [], []

    for idx, emotion in enumerate(emojis):
        training_files, validation_files = get_files(emotion)
        
        training_data += load_images(training_files)
        training_labels += [idx]*len(training_files)

        validation_data += load_images(validation_files)
        validation_labels += [idx]*len(validation_files)

    return (training_data, np.array(training_labels),
            validation_data, np.array(validation_labels))

def train_model():
    print("Preparing dataset...")
    training_data, training_labels, validation_data, validation_labels = prepare_dataset()
    
    print(f"Training model with {len(training_labels)} images...")
    fisher_face.train(training_data, training_labels)
    
    model_path = "result/fisher_model.xml"
    fisher_face.save(model_path)
    print(f"Model saved at {model_path}")

    return model_path, validation_data, validation_labels

if __name__ == "__main__":
    train_model()