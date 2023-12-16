import subprocess

# Define the list of Python scripts to run in order
scripts_to_run = [
    "defillama_chain_data_sync.py",
    "historical_tvl_storage.py",
    "defillama_tvl_analysis.py",
    "send_to_discord.py",
]

# Loop through the scripts and run them one by one
for script in scripts_to_run:
    print(f"Running script: {script}")
    subprocess.run(["python3", script])

print("All scripts have been executed.")
