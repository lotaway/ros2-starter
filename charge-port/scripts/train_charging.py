from ultralytics import YOLO
import torch
import os

def train_charging_detector():
    # 1. Load pre-trained model
    model = YOLO('yolov8n.pt') 
    
    # Check if data config exists
    data_yaml = 'dataset/charging_port.yaml'
    if not os.path.exists(data_yaml):
        print(f"Warning: {data_yaml} not found. Please ensure dataset structure is correct.")
        return

    # 2. Training parameters
    results = model.train(
        data=data_yaml,
        epochs=100,
        imgsz=640,
        batch=16,
        device='cuda' if torch.cuda.is_available() else 'cpu',
        workers=8,
        optimizer='AdamW',
        lr0=0.001,
        lrf=0.01,
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=0.0,
        translate=0.1,
        scale=0.5,
        shear=0.0,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.5,
        mosaic=1.0,
        mixup=0.0,
        patience=50,
        save=True,
        save_period=10,
        project='runs/train_charging',
        name='charging_detector',
    )
    
    # 3. Validation
    metrics = model.val()
    print(f"mAP50-95: {metrics.box.map}")
    print(f"mAP50: {metrics.box.map50}")
    
    # 4. Export
    model.export(format='onnx', imgsz=640)
    print("Training complete. Model saved to runs/train_charging/charging_detector/weights/best.pt")
    
    return model

if __name__ == '__main__':
    train_charging_detector()
