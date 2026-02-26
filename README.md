<p align="center">
  <img src="static/logo/logo2222.jpg" alt="Vajr Signals Logo" width="200"/>
</p>

<h1 align="center">Vajr Signals: LoRaWAN GPS Tracking</h1>

<p align="center">
  <strong>A high-performance real-time GPS monitoring system for LoRaWAN-enabled devices.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"/>
  <img src="https://img.shields.io/badge/Django-5.1.6-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django Version"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License"/>
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status"/>
</p>

---

## 📖 Overview

Vajr Signals is a comprehensive full-stack solution designed for field monitoring and safety tracking. The system seamlessly integrates with LoRaWAN gateways, parsing TeraTerm telemetry logs to provide a live, interactive map visualization of device movements and emergency SOS alerts.

---

## 📍 Table of Contents

- [📸 Visual Overview](#-visual-overview)
- [🚀 Key Features](#-key-features)
- [🛠️ Tech Stack](#-tech-stack)
- [⚙️ Getting Started](#-getting-started)
- [🛰️ How it Works](#-how-it-works)
- [📂 Structure](#-structure)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

---

## 📸 Visual Overview

### 🗺️ Main Dashboard
> Experience real-time precision tracking on a dynamic map.

![Dashboard showing real-time tracking](static/screenshots/dashboard.png)

### 🔐 User Authentication
> Secure, role-based access for device management.

| Login Interface | Active Session |
| :---: | :---: |
| ![Login Page Empty](static/screenshots/login_empty.png) | ![Login Page Filled](static/screenshots/login.png) |

### ⚙️ Device Management & Status
> Configure device parameters and monitor live API data streams.

| Configuration | Live Data Feed |
| :---: | :---: |
| ![Device Configuration Modal](static/screenshots/device_config.png) | ![Live API Data Fetching](static/screenshots/api_fetch.png) |

---

## 🚀 Key Features

- ✅ **Real-time Visualization**: Interactive map with multi-device tracking.
- ✅ **Smart Ingestion**: Automatic parsing of TeraTerm `.log` files for seamless data sync.
- ✅ **Advanced SOS System**: Instant visual & audio alerts for emergency packets.
- ✅ **Customizable UI**: Set unique marker colors and visibility states for each device.
- ✅ **History & Filtering**: Detailed path reconstruction with customizable time intervals.
- ✅ **Secure Auth**: Robust email-based authentication system.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Python 3.10+, Django 5.1.6, Django REST Framework |
| **Frontend** | HTML5, Vanilla JavaScript, CSS3 |
| **Database** | SQLite / MySQL |
| **Mapping** | Leaflet.js / OpenStreetMap |
| **Assets** | Pillow (Image Processing), MySQLClient |

---

## ⚙️ Getting Started

### 📋 Prerequisites
- Python 3.10 or higher
- `pip` (Python package manager)
- MySQL (Optional, for production environments)

### 🚀 Installation Steps

1. **Clone & Enter Directory**
   ```bash
   git clone <repository-url>
   cd lorawan_gps_tracking
   ```

2. **Environment Setup**
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

### 🏃 Running the Application
```bash
python manage.py runserver
```

---

## 🛰️ How it Works (Log Ingestion)

1. **Log Collection**: Devices log data via TeraTerm to the project root.
2. **Naming Pattern**: `teraterm_YYMMDD.log` (e.g., `teraterm_250225.log`).
3. **Parsing**: `LogIngestionService` extracts `LAT`, `LONG`, `DEV_ID`, and `PCKT_ID`.
4. **Alarms**: `PCKT_ID: SOS` automatically triggers the emergency siren and UI alerts.

---

## 📂 Project Structure

- 📁 `GPS_App/`: Core monitoring logic, models, and API endpoints.
- 📁 `GPS_Tracking/`: System configuration and settings.
- 📁 `templates/`: Clean, responsive HTML templates.
- 📁 `static/`: Project assets (CSS, JS, Audio, Screenshots).
- 📄 `requirements.txt`: Package dependencies.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---
<p align="center">
  <i>Created with ❤️ for GPS Monitoring Excellence.</i>
</p>
