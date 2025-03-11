import os
import whisper
import torchaudio

def preprocess_and_resample_audio(input_path, output_path, target_sr=16000):
    """
    Preprocess and resample the audio file, save it for reuse.
    """
    # Load the audio
    waveform, sr = torchaudio.load(input_path)

    # Resample if necessary
    if sr != target_sr:
        print(f"Resampling from {sr} Hz to {target_sr} Hz...")
        resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=target_sr)
        waveform = resampler(waveform)
    else:
        print("No resampling needed.")

    # Save the resampled audio for reuse
    torchaudio.save(output_path, waveform, target_sr)
    print(f"Resampled audio saved to: {output_path}")
    return output_path



def transcribe_audio(audio_path, custom_context):
    """
    Transcribe audio using OpenAI Whisper with a custom vocabulary context.
    """
    # Load the Whisper model
    model_name = "base"  # Options: tiny, base, small, medium, large
    model = whisper.load_model(model_name)

    # Transcribe the audio
    result = model.transcribe(audio_path, initial_prompt=custom_context)

    # Print the transcription
    print("\nTranscription:\n", result["text"])

def main():
    # Define paths
    audio_file_path = "AkhiJhyal_01.wav"  # Replace with your file's location
    resampled_file_path = "resampled_audio.wav"  # Adjust the path as needed

    # Preprocess and resample the audio
    resampled_audio = preprocess_and_resample_audio(audio_file_path, resampled_file_path)

    # Transcribe the resampled audio without custom vocabulary
    print("\n\nWithout custom vocabulary:\n")
    custom_context = ""
    transcribe_audio(resampled_audio, custom_context)

    # Transcribe the resampled audio with custom vocabulary
    print("\n\nWith custom vocabulary:\n")
    custom_context = "Yali, Garuda, Akhi Jhyal, Prayer Wheel"
    transcribe_audio(resampled_audio, custom_context)

if __name__ == "__main__":
    main()
