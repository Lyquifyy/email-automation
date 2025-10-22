import subprocess
import time

def start_ollama_model(model_name):
    """
    Starts the Ollama model in the background.
    """
    try:
        # Start the model in a separate process
        process = subprocess.Popen(
            ["ollama", "run", model_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Give it a few seconds to start
        time.sleep(5)

        # Optionally, check if the model is up by pinging it or sending a small request here
        print(f"{model_name} started successfully.")
        return process  # Keep the process if you want to terminate it later

    except Exception as e:
        print(f"Failed to start {model_name}: {e}")
        return None
