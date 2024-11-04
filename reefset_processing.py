# import json
# import os
# import random
# from pydub import AudioSegment

# # Load the JSON file
# with open("reefset_annotations.json") as f:
#     annotations = json.load(f)

# # Create an output directory if it doesn't exist
# output_dir = "reefset_mixed"
# os.makedirs(output_dir, exist_ok=True)

# # Organize audio files by dataset
# dataset_files = {}
# for item in annotations:
#     dataset = item["dataset"]
#     if dataset not in dataset_files:
#         dataset_files[dataset] = {}
#     dataset_files[dataset][item["label"]] = item["file_name"]

# # Filter datasets that have at least 4 distinct labels
# valid_datasets = {k: v for k, v in dataset_files.items() if len(v) >= 4}

# mixed_count = 0
# for dataset, label_files in valid_datasets.items():
#     labels = list(label_files.keys())
    
#     # Randomly create up to 22,000 mixed files
#     for i in range(22000):
#         # Randomly select 4 unique labels
#         selected_labels = random.sample(labels, 4)
#         selected_files = [label_files[label] for label in selected_labels]

#         # Load and mix audio files
#         mixed_audio = None
#         source_dir = os.path.join(output_dir, f"example_{i:05d}_sources")
#         os.makedirs(source_dir, exist_ok=True)
        
#         for label, source_path in zip(selected_labels, selected_files):
#             audio = AudioSegment.from_wav("full_dataset/"+source_path)
            
#             # Save source file with label in filename
#             source_output_path = os.path.join(source_dir, f"example_{i:05d}_source_{label}.wav")
#             audio.export(source_output_path, format="wav")
            
#             # Mix audio
#             if mixed_audio is None:
#                 mixed_audio = audio
#             else:
#                 mixed_audio = mixed_audio.overlay(audio)

#         # Save the mixed audio file
#         mixed_output_path = os.path.join(output_dir, f"example_{i:05d}.wav")
#         mixed_audio.export(mixed_output_path, format="wav")
#         mixed_count += 1

# print(f"Completed mixing {mixed_count} audio examples.")

import json
import os
import random
from pydub import AudioSegment

# Load the JSON file
with open("reefset_annotations.json") as f:
    annotations = json.load(f)

# Create an output directory if it doesn't exist
output_dir = "reefset_mixed"
os.makedirs(output_dir, exist_ok=True)

# Organize audio files by dataset
dataset_files = {}
for item in annotations:
    dataset = item["dataset"]
    if dataset not in dataset_files:
        dataset_files[dataset] = {}
    dataset_files[dataset][item["label"]] = item["file_name"]

# Filter datasets that have at least 4 distinct labels
valid_datasets = {k: v for k, v in dataset_files.items() if len(v) >= 4}

mixed_count = 0
for dataset, label_files in valid_datasets.items():
    labels = list(label_files.keys())
    
    # Create up to 22,000 mixed files
    for i in range(22000):
        # Randomly select exactly 4 unique labels
        selected_labels = random.sample(labels, 4)
        selected_files = [label_files[label] for label in selected_labels]

        # Load and mix audio files
        mixed_audio = None
        source_dir = os.path.join(output_dir, f"example_{i:05d}_sources")
        
        # Ensure the source subfolder is cleared and only includes the 4 selected sources
        os.makedirs(source_dir, exist_ok=True)
        
        # Track only 4 selected sources for the subfolder
        for label, source_path in zip(selected_labels, selected_files):
            audio = AudioSegment.from_wav("full_dataset/" + source_path)
            
            # Save each source file with label in filename
            source_output_path = os.path.join(source_dir, f"example_{i:05d}_source_{label}.wav")
            audio.export(source_output_path, format="wav")
            
            # Mix audio files
            if mixed_audio is None:
                mixed_audio = audio
            else:
                mixed_audio = mixed_audio.overlay(audio)

        # Save the mixed audio file
        mixed_output_path = os.path.join(output_dir, f"example_{i:05d}.wav")
        mixed_audio.export(mixed_output_path, format="wav")
        mixed_count += 1

print(f"Completed mixing {mixed_count} audio examples.")
