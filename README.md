# Divale Data Analysis
# Project Overview

This repository contains the source code and analysis scripts for the Divale Data Analysis project at Eduvos Higher Education Institution. Developed by Divale Mbelo, this project focuses on analyzing specific datasets to derive insights and visualizes the results through a deployed application.

The project is structured to address specific analytical questions (q1 through q4) and includes a deployment-ready application interface.

Student: Divale Mbelo (@Divale2712)

Supervisor: Siphuma Thendo (@thendoshane)

# Repository Structure
The repository is organized as follows:

1. app.py: The main entry point for the application (likely a Streamlit or Flask dashboard) that visualizes the analysis results.

2. deployment.py: Scripts and configurations required for deploying the application to a server or cloud environment.

3. deployment/: Directory containing additional deployment assets for streamlit.

4. q1_q2.py: Python script containing the analysis and code for Questions 1 and 2.

5. q3.py: Python script containing the analysis and code for Question 3.

6. q4.py: Python script containing the analysis and code for Question 4.

# Installation & Setup
To run this project locally, follow these steps:

# 1. Clone the Repository
On Bash:

- git clone https://github.com/thendoshane/Data_Analysis_By_Divale_Mbelo.git
- cd Divale_DataAnalysis
# 2. Set Up a Virtual Environment (Optional but Recommended)

Windows:
- python -m venv venv
- venv\Scripts\activate

macOS/Linux:
- python3 -m venv venv
- source venv/bin/activate

# 3. Install Dependencies

On Bash:

- pip install pandas numpy streamlit

# Usage
- Running the Analysis
- You can run individual analysis scripts to see the raw output or data processing steps:

On Bash:

- python q1_q2.py
- python q3.py
- python q4.py

Launching the Application

To start the web application interface:

On Bash:

# If using Streamlit
streamlit run app.py

# If using standard Python
python app.py

# Features
1. Data Processing: Cleaning and preparation of raw data for analysis.

2. Statistical Analysis: Detailed breakdown of metrics as required by the project scope.

3. Visualization: Interactive charts and graphs (via app.py) to present findings effectively.

4. Deployment
This project includes a deployment module, facilitating easy deployment to platforms like Streamlit Cloud, Heroku, or AWS. Refer to deployment.py for specific configurations.

5. Acknowledgements
This project was completed under the supervision of Siphuma Thendo (@thendoshane) providing guidance on methodology and analytical approaches.
