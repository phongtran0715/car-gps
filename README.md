# Car GPS Tracking Application

## Description

The Car GPS Tracking application is a Python Django project designed for real-time tracking and management of vehicles using GPS data. This application provides functionalities to monitor car locations, speed, and odometer readings, offering a comprehensive overview of vehicle metrics for personal or fleet management purposes.

## Features

- **Real-time GPS Tracking**: Monitors the real-time location of cars using GPS data.
- **Speed Monitoring**: Tracks and records the speed of each vehicle.
- **Odometer Reading**: Logs odometer readings to monitor distance traveled.
- **Historical Data**: Stores historical data for location, speed, and odometer readings for reporting and analysis.
- **User Dashboard**: A Django-admin based dashboard for easy management and viewing of vehicle metrics.
- **Alerts and Notifications**: Configurable alerts for specific events such as speed thresholds being exceeded or entering/exiting designated geofenced areas.

## Getting Started

### Prerequisites

- Python 3.x
- Django
- Django REST Framework (for API endpoints)
- A GPS tracking device installed in each vehicle with internet connectivity

### Installation

1. Clone the repository to your local machine:
`git clone https://github.com/phongtran0715/car-gps.git`

2. Navigate to the cloned directory:
`cd car-gps`

3. Install the required Python dependencies:
`pip install -r requirements.txt`


### Configuration

1. Configure your Django settings (`settings.py`) with your database and other environment-specific settings.
2. Set up the GPS tracking devices to send data to your server endpoint, as defined in your Django application routes.

### Running the Application

Execute the following command to run the Django server:
`python manage.py runserver`



## Contact

Phong Tran - Telegram: @phongtran0715 - Skype: @phongtran0715


