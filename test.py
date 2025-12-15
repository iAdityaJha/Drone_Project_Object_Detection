import airsim
import cv2
import numpy as np
from ultralytics import YOLO

# --- CONFIGURATION ---
CONFIDENCE_THRESHOLD = 0.5
RELEVANT_CLASSES = [0, 1, 2, 3, 5, 7]  # Person, Bike, Car, Motorbike, Bus, Truck
SPEED = 5  # Speed in m/s

def connect_to_drone():
    client = airsim.MultirotorClient()
    try:
        client.confirmConnection()
        client.enableApiControl(True)
        client.armDisarm(True)
        print("Connected to AirSim and Armed!")
        return client
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def handle_keys(key, client):
    """
    Maps keyboard keys to drone movements.
    Async methods are used so the video feed doesn't freeze.
    """
    if key == -1:
        return 

   
    
    if key == ord('w'):  # Forward
        client.moveByVelocityBodyFrameAsync(SPEED, 0, 0, 0.5)
        print("Moving Forward")
    elif key == ord('s'):  # Backward
        client.moveByVelocityBodyFrameAsync(-SPEED, 0, 0, 0.5)
        print("Moving Backward")
    elif key == ord('a'):  # Slide Left
        client.moveByVelocityBodyFrameAsync(0, -SPEED, 0, 0.5)
        print("Moving Left")
    elif key == ord('d'):  # Slide Right
        client.moveByVelocityBodyFrameAsync(0, SPEED, 0, 0.5)
        print("Moving Right")
        
    # --- ALTITUDE & YAW (Arrow Keys) ---
    elif key == 2490368:  
    # Up Arrow
        client.moveByVelocityBodyFrameAsync(0, 0, -SPEED, 0.5)
        print("Ascending")
    elif key == 2621440:  # Down Arrow
        client.moveByVelocityBodyFrameAsync(0, 0, SPEED, 0.5)
        print("Descending")
    elif key == ord('q'): # Rotate Left
        client.rotateByYawRateAsync(-30, 0.5)
        print("Rotate Left")
    elif key == ord('e'): # Rotate Right
        client.rotateByYawRateAsync(30, 0.5)
        print("Rotate Right")

def main():
    model = YOLO('yolov8n.pt') 
    client = connect_to_drone()
    if not client: return

    print("Taking off...")
    client.takeoffAsync().join()
    client.moveToPositionAsync(0, 0, -5, 5).join() # Hover at 5m

    print("Controls:")
    print("  [W/S] Forward/Back")
    print("  [A/D] Left/Right")
    print("  [Q/E] Rotate Left/Right")
    print("  [Z/X] Up/Down (Z=Up, X=Down)")
    print("  [ESC] Quit")

    while True:
        # 1. Capture Image
        responses = client.simGetImages([
            airsim.ImageRequest("front_center", airsim.ImageType.Scene, False, False)
        ])

        if not responses: continue

        # 2. Process Image
        response = responses[0]
        img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
        
        if img1d.size > 0:
            frame = img1d.reshape(response.height, response.width, 3)
            
            # 3. Detect Objects
            results = model(frame, verbose=False, classes=RELEVANT_CLASSES, conf=CONFIDENCE_THRESHOLD)
            annotated_frame = results[0].plot()

            # 4. Display
            # cv2.imshow("Drone Control Center", annotated_frame)
            large_frame = cv2.resize(annotated_frame, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_LINEAR)
            
            cv2.imshow("Drone Control Center", large_frame)
        # 5. Handle Keyboard Input
        
        key = cv2.waitKey(1) & 0xFF 

        if key == 27: # ESC key
            break
        
        # Simple mapping for Z/X since arrow keys can be tricky across platforms in cv2
        if key == ord('z'): # Up
            client.moveByVelocityBodyFrameAsync(0, 0, -SPEED, 0.5)
        elif key == ord('x'): # Down
            client.moveByVelocityBodyFrameAsync(0, 0, SPEED, 0.5)
        else:
            handle_keys(key, client)

    
    print("Landing...")
    client.landAsync().join()
    client.armDisarm(False)
    client.enableApiControl(False)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()