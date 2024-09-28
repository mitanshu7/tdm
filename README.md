Title: XML Dump Project - Biorxiv and Medrxiv Data Extraction and Upload to Hugging Face Dataset

## Project Overview

This project is designed to download `.meca` (ZIP) files from the Biorxiv and Medrxiv S3 buckets on AWS, extract XML files with full-text articles in them, and upload them to a Hugging Face dataset repository. The project uses Python and several libraries including boto3 for AWS S3 operations, Hugging Face Hub for dataset management, and Gradio for creating a simple user interface.

## Prerequisites

- AWS S3 bucket access credentials (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY)
- Hugging Face API key (HF_API_KEY)
- Python 3.x
- Required Python libraries: boto3, huggingface_hub, gradio, tqdm, threading

## Setup

1. Clone the repository to your local machine.
2. Install the required Python libraries using pip:

```bash
pip install boto3 huggingface_hub gradio tqdm
```

3. Add your AWS S3 bucket access credentials and Hugging Face API key to your environment variables or the script itself.

## Usage

0. Create a 🤗 account and create **2** new Space with Gradio as template. One for Biorxiv, another for Medrxiv.

1. Upload the `app.py` and `requirements.txt` file to the Hugging Face Spaces.

2. Delete function for *Medrxiv* in `app.py` to process *Biorxiv* data from 1 space. And vice versa for the other space.

3. The script will start downloading the XML files from the Biorxiv/Medrxiv S3 buckets, process them, and upload them to a Hugging Face dataset repository.

4. A simple user interface will be launched using Gradio so as to avoid the 'Starting' timeout of 30 miutes on Hugging Face Spaces. (Although it is modifiable upto `5h59m`. [Source](https://huggingface.co/docs/hub/spaces-config-reference#spaces-configuration-reference:~:text=startup_duration_timeout%3A%20string))

## Important Notes

- This project is hosted on Hugging Face Spaces. To make this work, you need to add your secrets (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and HF_API_KEY) in the Hugging Face Spaces settings.
- The script uses multithreading to download and process files from both Biorxiv and Medrxiv buckets simultaneously.DO NOT USE IT THIS WAY. Since I am using same tmp folder for both the preprint server and it will cause a race condition. Use parts of the script seperately.
- The script handles errors that may occur during the processing of files. If an error occurs, the script will print an error message and continue with the next file.
- The script creates a dataset repository on Hugging Face if it doesn't exist. The repository is set to public by default.
- The script uploads the processed XML files as zip archives to the Hugging Face dataset repository.

## License

This project is licensed under the MIT License. See the LICENSE file for details.