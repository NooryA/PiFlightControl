# Raspberry Pi Airplane Controller

This repository contains code for controlling an airplane using a Raspberry Pi. The system handles servo movements for wings, tail, and motor, along with telemetry logging from various sensors.

## Features

- **Servo Control:**
  - Controls servos for ailerons, elevator, rudder, and motor using PWM signals.
  - Throttle control for motor speed using ESC.

- **Telemetry Logging:**
  - Logs data from sensors like BMP3XX (temperature and pressure) and MPU6050 (accelerometer and gyroscope).
  - Saves telemetry data to a CSV file for later analysis.

- **PPM Signal Handling:**
  - Reads and processes PPM signals to control servos and motor.

## File Structure

### 1. `RF_control.py`
- Reads PWM signals and maps them to a range for controlling RF positions.
- Features:
  - PWM signal reading.
  - Mapping signal values to desired ranges.

### 2. `combined.py`
- Main control program that:
  - Handles PPM signal processing.
  - Controls servos and motor using PPM input.
  - Logs telemetry data to a CSV file.
- Features:
  - Servo angle calculation based on signal durations.
  - Real-time telemetry logging from BMP3XX and MPU6050 sensors.

### 3. `sensors.py`
- Standalone script for logging telemetry data.
- Logs temperature, pressure, accelerometer, and gyroscope data to a CSV file.

## Prerequisites

### Hardware:
- Raspberry Pi (any model with GPIO support).
- Servo motors for ailerons, elevator, and rudder.
- Electronic Speed Controller (ESC) for the motor.
- BMP3XX sensor (for temperature and pressure).
- MPU6050 sensor (for accelerometer and gyroscope).

### Software:
- Python 3.7 or later.
- Libraries:
  - `RPi.GPIO`
  - `pigpio`
  - `adafruit_bmp3xx`
  - `adafruit_servokit`
  - `mpu6050`
  - `busio`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/repo_name.git
   cd repo_name
   ```

2. Install required Python packages:
   ```bash
   pip install RPi.GPIO pigpio adafruit-circuitpython-bmp3xx adafruit-circuitpython-servokit mpu6050-python
   ```

3. Enable `pigpio` daemon:
   ```bash
   sudo pigpiod
   ```

## Usage

### Running Individual Scripts:

1. **Run `RF_control.py`:**
   ```bash
   python RF_control.py
   ```
   Monitors PWM input and prints RF position values.

2. **Run `sensors.py`:**
   ```bash
   python sensors.py
   ```
   Logs telemetry data from sensors to `telemetry_data.csv`.

3. **Run `combined.py`:**
   ```bash
   python combined.py
   ```
   Controls servos and motor while logging telemetry data.

## Telemetry Data
- The telemetry data is saved to `telemetry_data.csv` in the following format:
  ```csv
  Timestamp,Temperature,Pressure,X_Acceleration,Y_Acceleration,Z_Acceleration,X_Gyro,Y_Gyro,Z_Gyro
  2025-01-26 12:00:00,25.00,1013.25,0.12,-0.08,9.81,0.01,0.02,0.03
  ```
