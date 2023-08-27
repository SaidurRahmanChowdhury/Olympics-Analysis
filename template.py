import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

project_name="Olympics Analysis"

list_of_files=[
    f"source/{project_name}/__init__.py",
    f"source/{project_name}/notebook/__init__.py",
    "app.py",
    "helper.py",
    "preprocessor.py",
    "requirements.txt",
    "setup.py"
]

for filepath in list_of_files:
    filepath=Path(filepath)
    filedir,filename=os.path.split(filepath)
    
    if filedir != "":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file {filename}")
        
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath,'w') as f:
            pass
        logging.info(f"Creating empty file : {filepath}")
        
    
    else:
        logging.info(f"{filename} is already exist")