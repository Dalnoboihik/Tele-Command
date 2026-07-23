# BrewSpherix

<div align="center">
  <pre>
    ____  ____  _______       _______ __ __ ____
   / __ )/ __ \/ ____/ |     / / ___// //_//  _/
  / __  / /_/ / __/  | | /| / /\__ \/ ,<   / /  
 / /_/ / _, _/ /___  | |/ |/ /___/ / /| |_/ /   
/_____/_/ |_/_____/  |__/|__//____/_/ |_/___/   
  </pre>
  
  <strong>BrewSpherix</strong> — Web-based Server Management Panel
  
  [![Version](https://img.shields.io/badge/version-0.1.0--alpha-blue)](https://github.com/Dalnoboihik/brewspherix)
  [![Python](https://img.shields.io/badge/python-3.8+-green)](https://www.python.org/)
  [![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)
  [![Status](https://img.shields.io/badge/status-active--development-orange)](https://github.com/Dalnoboihik/brewspherix)
</div>

---

## Important Notice

If you download a pre-compiled build (.exe), Windows may flag it as potentially dangerous, and VirusTotal may mark it as suspicious. This is NORMAL for early alpha versions. If you don't trust the build, you can compile it yourself from source code.

---

## About

BrewSpherix is a lightweight web-based server management panel designed for monitoring system resources and remote administration. The project is in active development (v0.1.0-alpha).

---

## Current Features

### System Monitoring
- CPU: Real-time processor load display (updates every second)
- RAM: Memory usage monitoring with visual progress bar
- Load Graphs: Visualization of CPU and RAM load history over the last hour
- Statistics: Display of current and maximum load values
- System Information: Processor model and RAM size display

### Server Management
- Shutdown: Remote server shutdown with timer (10 seconds)
- Reboot: Remote server restart with timer (10 seconds)
- Protection: Action confirmation before executing critical commands

### Interface
- Dark Theme: Developer-oriented dark color scheme
- Responsive Design: Correct display on PC and mobile devices
- Floating Commands: Background animations with code snippets from various programming languages
- Clock: Real-time clock display

### Security
- Authorization: Simple login system with session cookies
- Protection: Panel access only after successful authentication

---

## Roadmap

### Upcoming Updates (v0.2.0)
- Save load history to file (JSON/CSV)
- Linux and macOS support
- System log viewer
- Disk space monitoring
- Auto-refresh page on data change

### Medium-term Plans (v0.3.0)
- Process manager (start/stop)
- File manager (browse/upload/delete)
- Notification settings for critical load
- Export statistics to CSV/PDF
- Docker support

### Long-term Plans (v1.0.0)
- Multi-user mode
- Role and permission system
- Windows Services management
- Network interface monitoring
- REST API for integration with other systems
- Telegram/Email notifications
- Action history (audit log)

---

## Quick Start

### Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Windows (for full functionality)

### Installation from Source

git clone https://github.com/Dalnoboihik/brewspherix.git
cd brewspherix
pip install psutil
python server.py

### Running
1. Open your browser and go to: http://localhost:3000
2. Enter login and password (default: admin / admin)
3. Enjoy managing your server

---

## Project Structure

brewspherix/
├── server.py          # Main Python server
├── index.html         # Management panel (main page)
├── login.html         # Authorization page
├── Clean.bat          # Example cleanup script
├── reboot.bat         # Reboot script
└── README.md          # Documentation

---

## Technical Details

### Technologies Used
- Backend: Python 3.8+ (built-in HTTP server)
- Frontend: HTML5, CSS3, JavaScript
- Libraries:
  - psutil — system information collection
  - Chart.js — graph visualization
- Build: PyInstaller (for .exe version)

### System Requirements
- RAM: from 128 MB
- Processor: any
- Disk: from 50 MB
- OS: Windows 7/8/10/11

---

## License

This project is distributed under the MIT License. You are free to use, modify, and distribute the code.

---

## Author

<div align="center">
  <a href="https://github.com/Dalnoboihik">Dalnoboihik</a>
</div>

---

## Contributing

Any suggestions, ideas, and pull requests are welcome. If you find a bug or want to suggest an improvement, create an issue in the repository.

---

## Contact

- GitHub: Dalnoboihik
- Email: ngorbunov520@gmail.com

---

<div align="center">
  Made with coffee and code for the community