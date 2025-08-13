# Main.py Code Explanation

## Overview
`main.py` is the entry point and control script for the Horizontal Travel Robot Arm (HTA0) system. It provides three distinct operational modes for testing, autonomous pick-and-place operations, and image detection/calibration.

## System Architecture
The robot arm system consists of several interconnected components:
- **Raspberry Pi Camera**: Captures real-time video for object detection
- **Arduino Controller**: Controls the physical robot arm via serial communication
- **Computer Vision Processing**: Uses OpenCV for image recognition and coordinate calculation
- **Main Control Loop**: Orchestrates camera capture, object detection, and arm movements

## Code Structure

### 1. Import and Initialization
```python
import main_loop

# Configuration variables
serial_port='/dev/ttyACM0'  #'/dev/ttyACM1'
imgdir="/home/pi/Desktop/Captures/"
imgprefix="CapF"

# Initialize the main control loop
loop=main_loop.main_loop(serial_port)
```

**Purpose**: 
- Imports the main control loop module that handles camera operations and arm control
- Sets up configuration for Arduino serial communication and image storage
- Creates the main loop instance that will coordinate all system operations

**Configuration Variables**:
- `serial_port`: USB port for Arduino communication (typically `/dev/ttyACM0` or `/dev/ttyACM1`)
- `imgdir`: Directory where captured images are stored
- `imgprefix`: Filename prefix for saved images

### 2. Operation Modes

The system provides three main operation modes through dedicated functions:

#### A. RunTests() - Hardware Testing Mode
```python
def RunTests():
    #Arm Movement Testing
    #loop.test_arm()
    #loop.test_arm_XYZ(5,5,-9)
    loop.test_arm_home()
    #loop.test_arm_home_plane()
    #loop.test_arm_clearcamera()
```

**Purpose**: Tests basic arm movement functionality
**What it does**:
- Currently only executes `test_arm_home()` which moves the arm to its home position
- Other test functions are commented out but available:
  - `test_arm()`: Complete arm movement test sequence
  - `test_arm_XYZ(5,5,-9)`: Move arm to specific coordinates (X=5, Y=5, Z=-9)
  - `test_arm_home_plane()`: Move arm to home position at base level
  - `test_arm_clearcamera()`: Move arm away from camera's field of view

#### B. RunPickandPlace() - Autonomous Operation Mode
```python
def RunPickandPlace():
    #Run Pick and Place
    fullscreen=False
    detectXYZ=True
    calculateXYZ=True
    move_arm=True
    loop.capturefromPiCamera(imgdir,imgprefix,fullscreen,detectXYZ,calculateXYZ,move_arm)
```

**Purpose**: Fully autonomous pick-and-place operation
**Configuration**:
- `fullscreen=False`: Camera display in windowed mode
- `detectXYZ=True`: Enable object detection in camera feed
- `calculateXYZ=True`: Convert pixel coordinates to real-world coordinates
- `move_arm=True`: Allow the arm to physically move to pick up detected objects

**What it does**:
1. Starts camera capture loop
2. Detects objects in the camera feed
3. Calculates real-world coordinates of detected objects
4. Automatically moves the arm to pick up and place objects

#### C. ImageDetection() - Development/Calibration Mode
```python
def ImageDetection():
    #Work on Image Detection (press ESC when done, Space to capture image)
    loop.test_arm_clearcamera()

    fullscreen=False
    detectXYZ=True
    calculateXYZ=True
    move_arm=False  # Key difference: arm doesn't move
    loop.capturefromPiCamera(imgdir,imgprefix,fullscreen,detectXYZ,calculateXYZ,move_arm)

    loop.test_arm_home()
```

**Purpose**: Safe mode for testing computer vision without arm movement
**Configuration**:
- `move_arm=False`: Prevents physical arm movement (key safety feature)
- All detection and calculation features remain active
- User can capture images manually using spacebar key

**What it does**:
1. Moves arm away from camera view initially
2. Starts camera feed with object detection overlay
3. Shows detected objects and their calculated coordinates
4. Allows manual image capture (press Space) for analysis
5. Returns arm to home position when finished (press ESC)

### 3. Program Execution
```python
#RunTests()
#RunPickandPlace()
ImageDetection()
```

**Current Configuration**: The system is set to run in `ImageDetection()` mode by default.
- This is the safest mode for development and testing
- Other modes are commented out to prevent accidental activation

## Key Features and Safety

### Safety Features
1. **Safe Default Mode**: `ImageDetection()` runs with `move_arm=False` to prevent unexpected arm movement
2. **Manual Control**: User can press ESC to exit the camera loop at any time
3. **Arm Positioning**: Arm is moved to clear camera view initially and returned home at the end

### User Controls (during camera operation)
- **ESC Key**: Exit the camera loop and stop the program
- **Space Key**: Manually capture and save an image to the specified directory

### System Integration
The `main.py` script integrates several complex subsystems:

1. **Camera System** (`camera_realworldxyz.py`):
   - Captures live video feed from Raspberry Pi camera
   - Performs background subtraction for object detection
   - Converts pixel coordinates to real-world XYZ coordinates

2. **Image Recognition** (`image_recognition_singlecam.py`):
   - Processes camera images to detect objects
   - Uses background subtraction and contour detection
   - Calculates object centroids and bounding rectangles

3. **Arduino Communication** (`commands_arduino.py`):
   - Sends movement commands to Arduino via serial port
   - Controls arm position using XYZ coordinates
   - Manages gripper open/close operations

4. **Main Control Loop** (`main_loop.py`):
   - Orchestrates camera capture, image processing, and arm control
   - Manages timing and synchronization between components
   - Provides the main execution framework

## Usage Recommendations

### For Development/Testing:
- Use `ImageDetection()` mode (default) to safely test computer vision
- Verify object detection accuracy before enabling arm movement

### For Calibration:
- Use `RunTests()` to verify arm movement functionality
- Test individual arm positions and movements

### For Production:
- Switch to `RunPickandPlace()` only after thorough testing
- Ensure proper calibration of camera-to-arm coordinate mapping

## Troubleshooting

### Common Issues:
1. **Serial Port**: If Arduino connection fails, check `serial_port` variable
2. **Camera**: Ensure Raspberry Pi camera is properly connected and enabled
3. **Permissions**: Verify proper permissions for camera and serial port access
4. **Directory**: Ensure `imgdir` exists and is writable

### Switching Modes:
To change operation modes, comment/uncomment the appropriate function calls at the bottom of the file:

```python
# For testing only:
RunTests()

# For autonomous operation:
# RunPickandPlace()

# For development/calibration:
# ImageDetection()
```