#include "vex.h"
#include <cmath> // for fabs()

using namespace vex;

// Brain and controller
brain Brain;
controller Controller1;

// Motors (adjust ports and reversed flags)
motor frontLeftMotor(PORT20, gearSetting::ratio18_1, false);
motor backLeftMotor(PORT11, gearSetting::ratio18_1, false);
motor frontRightMotor(PORT10, gearSetting::ratio18_1, true);
motor backRightMotor(PORT1, gearSetting::ratio18_1, true);

// Helper function to spin a motor with signed speed
void spinMotorSigned(motor &m, double speed) {
    if (speed >= 0) {
        m.spin(vex::directionType::fwd, speed, vex::velocityUnits::pct);
    } else {
        m.spin(vex::directionType::rev, fabs(speed), vex::velocityUnits::pct);
    }
}

int main() {
    while (true) {
        // Joystick inputs
        double forwardVal = Controller1.Axis4.position(percent);
        double strafeVal  = Controller1.Axis3.position(percent);
        double rotateVal  = Controller1.Axis1.position(percent);

        // Calculate mecanum motor speeds
        double frontLeftSpeed  = forwardVal + strafeVal + rotateVal;
        double backLeftSpeed   = forwardVal - strafeVal + rotateVal;
        double frontRightSpeed = forwardVal - strafeVal - rotateVal;
        double backRightSpeed  = forwardVal + strafeVal - rotateVal;

        // Spin motors using helper function
        spinMotorSigned(frontLeftMotor, frontLeftSpeed);
        spinMotorSigned(backLeftMotor, backLeftSpeed);
        spinMotorSigned(frontRightMotor, frontRightSpeed);
        spinMotorSigned(backRightMotor, backRightSpeed);

        wait(20, msec); // Small delay for stability
    }
}
