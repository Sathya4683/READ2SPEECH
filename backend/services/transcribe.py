import os

def save_audio_bytes_to_mp3(audio_bytes: bytes, output_path: str) -> None:
    """
    Save raw audio bytes to an MP3 file.

    Args:
        audio_bytes (bytes): The raw audio content.
        output_path (str): The path where the .mp3 file should be saved.
    """
    with open(output_path, 'wb') as f:
        f.write(audio_bytes)
    print(f"Saved audio to: {os.path.abspath(output_path)}")
