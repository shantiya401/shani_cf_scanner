# shani_cf_scanner
Cloud flare clean ip scanner 2

# Shani CF IP Scanner

## Overview

Shani CF IP Scanner is a tool designed to scan IP addresses within a specified range to measure their connectivity and performance. This tool is useful for network administrators and developers who need to test the availability and performance of IP addresses in their network or infrastructure.

## Features

- Scan a specified range of IP addresses.
- Measure ping response times.
- Check download speeds from a given test URL.
- Display results in a table format.
- View real-time logs of scan progress and results.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/shantiya401/shani-cf-ip-scanner.git
Navigate to the project directory:

cd shani-cf-ip-scanner

Install the required dependencies:

Ensure you have Python and Flask installed. You can install Flask using pip:

pip install flask

Run the application:

python app.py


The application will start and be accessible at http://localhost:5000.

Usage
Open the application in your web browser.
Select an IP range from the dropdown menu.
Enter a test URL if needed (default is Cloudflare speed test).
Specify the number of IPs to scan and the maximum acceptable ping time.
Click "Start Scan" to begin the scanning process.
Click "Stop Scan" to halt the scan and reset the process.
Real-Time Updates
The application uses WebSocket for real-time updates. Ensure that your browser supports WebSocket connections.

Contributing
Contributions are welcome! Please submit a pull request or open an issue if you encounter any bugs or have suggestions for improvements.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
For questions or support, please contact your.email@example.com.

