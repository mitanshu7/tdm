import boto3
import os
import zipfile
from glob import glob
import shutil
from huggingface_hub import HfApi
import gradio as gr
from tqdm.auto import tqdm
import threading


################################################################################

# Declarations:
print("Declaring variables.")
# AWS S3 service name
service_name = 's3'

# AWS S3 bucket names
biorxiv_bucket_name = 'biorxiv-src-monthly'
medrxiv_bucket_name = 'medrxiv-src-monthly'

# AWS region name
region_name = 'us-east-1'

# Hugging Face destination repository name
destination_repo_name = 'xml-dump-monthly'

################################################################################

print("Initiating clients.")

# Create a S3 client
s3_client = boto3.client(
    service_name='s3',
    region_name=region_name,
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
paginator = s3_client.get_paginator('list_objects_v2')

# Create a Hugging Face API client
access_token =  os.getenv('HF_API_KEY')
hugging_face_api = HfApi(token=access_token)

# Create a dataset repo
hugging_face_api.create_repo(
    repo_id=destination_repo_name,
    repo_type="dataset",
    private=False,
    exist_ok=True
)

# Extract Hugging facec username
username = hugging_face_api.whoami()['name']
repo_id = f"{username}/{destination_repo_name}"

################################################################################

def download_biorxiv(Prefix=""):
    
    print("Downloading Biorxiv files.")

    # Output folders for downloaded files
    biorxiv_output_folder = Prefix + 'biorxiv-xml-dump'

    # Create output folders if they don't exist
    os.makedirs(biorxiv_output_folder, exist_ok=True)

    # Gather all objects from Biorxiv bucket
    biorxiv_pages = paginator.paginate(
        Bucket=biorxiv_bucket_name,
        RequestPayer='requester',
        Prefix=Prefix
    ).build_full_result()

    # Dowload all objects from Biorxiv bucket
    for biorxiv_object in tqdm(biorxiv_pages['Contents'], desc=Prefix):

        # Get the file name
        file = biorxiv_object['Key']

        # Check if the file is a zip file
        if file.endswith(".meca"):

            # Proccess the zip file
            try:

                # Download the file
                s3_client.download_file(biorxiv_bucket_name, file, 'tmp_bio.meca', ExtraArgs={'RequestPayer':'requester'})
                    
                # Unzip meca file
                with zipfile.ZipFile('tmp_bio.meca', 'r') as zip_ref:
                    zip_ref.extractall("tmp_bio")

                # Gather the xml file
                xml = glob('tmp_bio/content/*.xml')

                # Copy the xml file to the output folder
                shutil.copy(xml[0], biorxiv_output_folder)

                # Remove the tmp_bio folder and file
                shutil.rmtree('tmp_bio')
                os.remove('tmp_bio.meca')

            except Exception as e:

                print(f"Error processing file {file}: {e}")


    # Zip the output folder
    shutil.make_archive(biorxiv_output_folder, 'zip', biorxiv_output_folder)

    # Upload the zip files to Hugging Face
    print(f"Uploading {biorxiv_output_folder}.zip to Hugging Face repo {repo_id}.")
    hugging_face_api.upload_file(path_or_fileobj=f'{biorxiv_output_folder}.zip', path_in_repo=f'{biorxiv_output_folder}.zip', repo_id=repo_id, repo_type="dataset")
    
    print("Biorxiv Done.")

# Create separate threads function
first_thread = threading.Thread(target=download_biorxiv, args=("Current_Content/September_2024/",))

# Start thread
first_thread.start()

################################################################################
def download_medrxiv(Prefix=""):

    print("Downloading Medrxiv files.")

    # Output folders for downloaded files
    medrxiv_output_folder = Prefix + 'medrxiv-xml-dump'

    # Create output folders if they don't exist
    os.makedirs(medrxiv_output_folder, exist_ok=True)

    # Gather all objects from Medrxiv bucket
    medrxiv_pages = paginator.paginate(
        Bucket=medrxiv_bucket_name,
        RequestPayer='requester',
        Prefix=Prefix
    ).build_full_result()

    # Dowload all objects from Medrxiv bucket
    for medrxiv_object in tqdm(medrxiv_pages['Contents'], desc=Prefix):

        # Get the file name
        file = medrxiv_object['Key']

        # Check if the file is a zip file
        if file.endswith(".meca"):

            # Proccess the zip file
            try:

                # Download the file
                s3_client.download_file(medrxiv_bucket_name, file, 'tmp_med.meca', ExtraArgs={'RequestPayer':'requester'})
                    
                # Unzip meca file
                with zipfile.ZipFile('tmp_med.meca', 'r') as zip_ref:
                    zip_ref.extractall("tmp_med")

                # Gather the xml file
                xml = glob('tmp_med/content/*.xml')

                # Copy the xml file to the output folder
                shutil.copy(xml[0], medrxiv_output_folder)

                # Remove the tmp_med folder and file
                shutil.rmtree('tmp_med')
                os.remove('tmp_med.meca')

            except Exception as e:
                print(f"Error processing file {file}: {e}")


    # Zip the output folder
    shutil.make_archive(medrxiv_output_folder, 'zip', medrxiv_output_folder)

    print(f"Uploading {medrxiv_output_folder}.zip to Hugging Face repo {repo_id}.")

    hugging_face_api.upload_file(path_or_fileobj=f'{medrxiv_output_folder}.zip', path_in_repo=f'{medrxiv_output_folder}.zip', repo_id=repo_id, repo_type="dataset")

    print("Medrxiv Done.")

# Create separate threads function
second_thread = threading.Thread(target=download_medrxiv, args=("Current_Content/September_2024/",))

# Start thread
second_thread.start()

###############################################################################

# Dummy app

def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

demo = gr.Interface(
    fn=greet,
    inputs=["text", "slider"],
    outputs=["text"],
)

demo.launch()

