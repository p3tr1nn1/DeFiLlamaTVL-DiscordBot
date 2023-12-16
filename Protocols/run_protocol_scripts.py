import subprocess

# Define the list of Python scripts to run in order
scripts_to_run = [
    "fetch_protocol_data.py",
    "calculate_average_tvl.py",
    "generate_json.py",
    "send_protocols_to_discord.py",
]

# Loop through the scripts and run them one by one
for script in scripts_to_run:
    print(f"Running script: {script}")
    subprocess.run(["python3", script])

print("All scripts have been executed.")
