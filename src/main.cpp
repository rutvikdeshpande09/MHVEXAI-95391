#include "vex.h"

using namespace vex;

// Devices
brain  Brain;
inertial InertialSensor(PORT15); // change PORT1 to whichever port it’s plugged into

int main() {
    // Calibrate the inertial
    InertialSensor.calibrate();
    while (InertialSensor.isCalibrating()) {
        wait(100, msec);
    }

    while (true) {
        // Get inertial values
        double heading = InertialSensor.heading(degrees);     // 0–360 compass style
        double rotation = InertialSensor.rotation(degrees);   // continuous angle

        // Print to robot brain screen
        Brain.Screen.clearScreen();
        Brain.Screen.setCursor(1,1);
        Brain.Screen.print("Heading: %.2f", heading);
        Brain.Screen.setCursor(2,1);
        Brain.Screen.print("Rotation: %.2f", rotation);

        // Print to VS Code console
        printf("Heading: %.2f | Rotation: %.2f\n", heading, rotation);

        wait(200, msec); // slow the loop a bit
    }
}