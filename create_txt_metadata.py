import os

# Define directories
reefset_dir = "reefset_mixed_split"
eval_dir = os.path.join(reefset_dir, "validation")
output_file = os.path.join(reefset_dir, "validation_example_list.txt")

# Open output file for writing
with open(output_file, "w") as f_out:
    # Iterate over each mixed file in the eval directory
    for mixed_file in os.listdir(eval_dir):
        if mixed_file.endswith(".wav"):
            # Construct the mixed file path
            mixed_file_path = os.path.join("validation", mixed_file)

            # Find the corresponding source folder
            source_folder_name = mixed_file.replace(".wav", "_sources")
            source_folder_path = os.path.join(eval_dir, source_folder_name)
            
            # Collect source file paths if the source folder exists
            if os.path.isdir(source_folder_path):
                source_file_paths = []
                for source_file in os.listdir(source_folder_path):
                    if source_file.endswith(".wav"):
                        source_file_path = os.path.join("validation", source_folder_name, source_file)
                        source_file_paths.append(source_file_path)
                
                # Write mixed file path and source file paths to the output file
                line = "\t".join([mixed_file_path] + source_file_paths)
                f_out.write(line + "\n")

print("eval_example_list.txt has been created with paths to each eval file and its corresponding sources.")
