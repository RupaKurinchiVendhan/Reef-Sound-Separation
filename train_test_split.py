import os
import random
import shutil

# Define source and target directories
source_dir = "reefset_mixed"
output_dir = "reefset_mixed_split"

# Create output directories if they don't exist
subfolders = ["eval", "train", "validation"]
for subfolder in subfolders:
    os.makedirs(os.path.join(output_dir, subfolder), exist_ok=True)

# Get all the mixed audio files in the source directory
mixed_files = [f for f in os.listdir(source_dir) if f.endswith(".wav")]

# Shuffle files randomly
random.shuffle(mixed_files)

# Define split sizes
eval_count = 20000
train_count = 1000
validation_count = 1000

# Assign files to each split
eval_files = mixed_files[:eval_count]
train_files = mixed_files[eval_count:eval_count + train_count]
validation_files = mixed_files[eval_count + train_count:eval_count + train_count + validation_count]

# Helper function to copy files and their corresponding source folders
def copy_files(file_list, target_subfolder):
    for file_name in file_list:
        # Copy mixed file
        src_file_path = os.path.join(source_dir, file_name)
        dest_file_path = os.path.join(output_dir, target_subfolder, file_name)
        shutil.copy(src_file_path, dest_file_path)
        
        # Copy corresponding source folder if it exists
        source_folder_name = file_name.replace(".wav", "_sources")
        src_folder_path = os.path.join(source_dir, source_folder_name)
        dest_folder_path = os.path.join(output_dir, target_subfolder, source_folder_name)
        
        if os.path.isdir(src_folder_path):
            shutil.copytree(src_folder_path, dest_folder_path)

# Copy files to each target subfolder
copy_files(eval_files, "eval")
copy_files(train_files, "train")
copy_files(validation_files, "validation")

print("Files have been successfully split into eval, train, and validation folders.")