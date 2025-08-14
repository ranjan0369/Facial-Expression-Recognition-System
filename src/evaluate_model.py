import cv2
import numpy as np
from train_model import emojis  # reuse the same list

def evaluate_model(model_path, test_images, test_labels):
    """Load model and evaluate accuracy."""
    fisher_face = cv2.face.FisherFaceRecognizer_create()
    fisher_face.read(model_path)

    correct = 0
    for idx, img in enumerate(test_images):
        pred, conf = fisher_face.predict(img)
        if pred == test_labels[idx]:
            correct += 1
    accuracy = (correct / len(test_labels)) * 100
    return accuracy

if __name__ == "__main__":
    from train_model import train_model
    # Train model and get validation set
    model_path, val_images, val_labels = train_model()

    # Evaluate
    acc = evaluate_model(model_path, val_images, val_labels)
    print(f"Validation Accuracy: {acc:.2f}%")