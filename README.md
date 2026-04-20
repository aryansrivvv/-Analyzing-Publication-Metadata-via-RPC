```markdown
# Analyzing Publication Metadata via RPC

**Author:** [Your Name]  
**Student ID:** MDS202508  

## Project Overview
This project implements a distributed Map-Reduce architecture in Python to analyze a remote dataset of publication titles. The application interfaces with a remote RPC server to authenticate, retrieve data, and compute the Top 10 most frequent first words across 1,000 publication files (`pub_0.txt` to `pub_999.txt`), ultimately submitting the findings back to the server for automated verification.

## Features & Architecture
* **Map-Reduce Implementation:** Utilizes Python's `multiprocessing.Pool` to parallelize data retrieval and word counting.
* **Dynamic RPC Authentication:** Implements a session-based login system that generates dynamic SHA-256 secret keys for secure API communication.
* **Fault Tolerance & Throttling:** Gracefully handles the server's strict 100 requests/second rate limit by catching HTTP 429 (Too Many Requests) errors and implementing an exponential backoff/retry mechanism.
* **Containerized:** Fully containerized using `python:3.11-slim` to ensure the final Docker image remains well under the 300MB assignment limit.

## Repository Structure
* `app.py`: The main Python application containing the Map-Reduce logic and RPC API calls.
* `Dockerfile`: The configuration file used to build the container image.
* `codespace_output.png`: Verification screenshot demonstrating successful execution and the final 10/10 score.
* `.gitignore`: Excludes local virtual environments and large `.tar` files from version control.

## Execution Instructions

### Option 1: Running in GitHub Codespaces (Primary Method)
As per the assignment requirements, this application is designed to be executed inside a GitHub Codespace.
1. Open this repository in GitHub.
2. Click the green **<> Code** button and select the **Codespaces** tab.
3. Click **Create codespace on main**.
4. Once the web-based terminal loads, install the required external library:
   ```bash
   pip install requests
   ```
5. Execute the application:
   ```bash
   python app.py
   ```
6. The script will process the 1,000 files and output the final verification score directly to the terminal.

### Option 2: Running locally with Docker
To build and verify the Docker image locally before exporting:
1. Build the image:
   ```bash
   docker build -t app_image .
   ```
2. Run the container:
   ```bash
   docker run --rm app_image
   ```
3. Export the container to a `.tar` file for final portal submission:
   ```bash
   docker save app_image -o firstname_MDS202508_Assignment01.tar
   ```

### Option 3: Standard Local Execution (Virtual Environment)
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install requests
   ```
3. Run the script:
   ```bash
   python app.py
   ```
```