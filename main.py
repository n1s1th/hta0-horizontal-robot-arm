"""
Main control script for Horizontal Travel Robot Arm (HTA0)

This script provides three operational modes:
1. RunTests() - Hardware testing and calibration
2. RunPickandPlace() - Autonomous pick-and-place operation  
3. ImageDetection() - Safe computer vision testing (no arm movement)

For detailed explanation, see MAIN_PY_EXPLANATION.md
"""
import main_loop


# Configuration variables
serial_port='/dev/ttyACM0'  # Arduino serial port (alternative: '/dev/ttyACM1')
imgdir="/home/pi/Desktop/Captures/"  # Directory for saving captured images
imgprefix="CapF"  # Filename prefix for saved images

# Initialize the main control loop that coordinates camera, vision, and arm control
loop=main_loop.main_loop(serial_port)


def RunTests():
    """
    Hardware Testing Mode
    
    Tests basic arm movement functionality. Currently executes only the home 
    position test for safety. Other test functions are available but commented out.
    
    Available tests:
    - test_arm(): Complete movement test sequence
    - test_arm_XYZ(x,y,z): Move to specific coordinates  
    - test_arm_home(): Move to home position (currently active)
    - test_arm_home_plane(): Move to home at base level
    - test_arm_clearcamera(): Move arm away from camera view
    """
    # Arm Movement Testing
    #loop.test_arm()  # Full movement test sequence
    #loop.test_arm_XYZ(5,5,-9)  # Move to specific coordinates (X=5, Y=5, Z=-9)
    loop.test_arm_home()  # Move to home position - CURRENTLY ACTIVE
    #loop.test_arm_home_plane()  # Move to home position at base level
    #loop.test_arm_clearcamera()  # Clear camera field of view

def RunPickandPlace():
    """
    Autonomous Pick-and-Place Mode
    
    Fully autonomous operation mode that:
    1. Captures live camera feed
    2. Detects objects using computer vision
    3. Calculates real-world coordinates from pixel positions
    4. Automatically moves arm to pick up and place objects
    
    WARNING: Arm will move automatically when objects are detected!
    """
    # Run Pick and Place with full automation
    fullscreen=False      # Display camera in windowed mode
    detectXYZ=True        # Enable object detection
    calculateXYZ=True     # Convert pixels to real-world coordinates
    move_arm=True         # ENABLE PHYSICAL ARM MOVEMENT
    loop.capturefromPiCamera(imgdir,imgprefix,fullscreen,detectXYZ,calculateXYZ,move_arm)

def ImageDetection():
    """
    Image Detection/Development Mode (SAFE)
    
    Safe mode for testing computer vision without arm movement. Perfect for:
    - Developing and testing object detection algorithms
    - Calibrating camera-to-coordinate mapping
    - Capturing images for analysis (press Space to save, ESC to exit)
    
    Key safety feature: move_arm=False prevents physical arm movement
    """
    # Work on Image Detection (press ESC when done, Space to capture image)
    loop.test_arm_clearcamera()  # Move arm away from camera initially

    fullscreen=False      # Display camera in windowed mode
    # Set detectXYZ to False when you want to use this loop only to capture pictures (press spacebar)
    detectXYZ=True        # Enable object detection with visual overlay
    # Set calculateXYZ to enable real world XYZ coordinate calculation
    calculateXYZ=True     # Convert pixel coordinates to real-world coordinates
    move_arm=False        # SAFETY: Disable physical arm movement
    loop.capturefromPiCamera(imgdir,imgprefix,fullscreen,detectXYZ,calculateXYZ,move_arm)

    loop.test_arm_home()  # Return arm to home position when finished

# ============================================================================
# PROGRAM EXECUTION - Choose operation mode by commenting/uncommenting below
# ============================================================================

# Testing Mode: Safe hardware testing (only home position movement)
#RunTests()

# Production Mode: Full autonomous pick-and-place operation
# WARNING: Arm will move automatically when objects are detected!
#RunPickandPlace()

# Development Mode: Safe computer vision testing (NO arm movement) - CURRENTLY ACTIVE
# Press Space to capture images, ESC to exit
ImageDetection()
