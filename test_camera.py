import cv2
print("Starting camera test...")
print("Press 'Q' to quit")

# Initialize the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera")
else:
    print("Camera opened successfully")
    print("Looking for camera window...")
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break

        # Display the frame
        cv2.imshow('Camera Test (Press Q to quit)', frame)

        # Check for 'q' key to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Q pressed, closing...")
            break

# Release everything
cap.release()
cv2.destroyAllWindows()
print("Camera test completed")