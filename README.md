# RAMI Marine Robots Project
This repository is for the RAMI Marine Robots Cascade Evaluation Campaign, focusing on building a pipeline that integrates object detection, OCR, and data processing for underwater object recognition. Each team member will contribute their part of the code in a structured way to enable easy integration.

## Project Structure
The repository is organized to allow each team member to work on their part of the project independently. Each team member has their own folder to upload and manage their code. The main pipeline script will combine all individual parts.

## folder structure
* Uploading code:
Place your script(s) for your assigned task in your folder. Ensure your code has clear inputs and outputs so it can be easily integrated into the main pipeline.
* Document requirements
If your code has specific dependencies, add a requirements.txt file in your folder.
## Pipeline Integration
The main integration is handled by the run_pipeline.sh script in the pipeline/ folder. This script orchestrates the data flow, calling each team member’s code in sequence. It combines outputs from each module (e.g., object detection output fed into OCR) and generates a final report.
## Committing Code
To keep the repository organized, follow these guidelines when committing code:

Commit Message Format: Use clear and consistent commit messages, such as:
feature: added OCR script in member_name1 folder
docs: updated README with pipeline usage instructions
fix: corrected bug in object detection code
Pull Requests: When you’re ready to integrate your code with the pipeline, create a pull request for review.

## Additional Notes
Version Control: Ensure any updates or fixes are committed regularly with proper comments.
Testing: Test each module individually before integration, as well as after integration into the pipeline.
