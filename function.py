from pydub import AudioSegment
import os

def process_audio_file(file_path, output_format='wav'):
    # Load the audio file
    audio = AudioSegment.from_file(file_path)

    # Extract audio channels
    channels = audio.split_to_mono()

    # Get basic information
    duration = audio.duration_seconds
    sample_width = audio.sample_width
    sample_rate = audio.frame_rate
    channels_count = len(channels)

    # Convert file format
    output_path = os.path.splitext(file_path)[0] + '.' + output_format
    audio.export(output_path, format=output_format)

    # Return the extracted channels and basic information
    return channels, duration, sample_width, sample_rate, channels_count, output_path

# Example usage
file_path = 'test_audio.wav'
output_format = 'mp3'

channels, duration, sample_width, sample_rate, channels_count, output_path = process_audio_file(file_path, output_format)

print("Channels:", channels)
print("Duration:", duration)
print("Sample Width:", sample_width)
print("Sample Rate:", sample_rate)
print("Channels Count:", channels_count)
print("Output Path:", output_path)
