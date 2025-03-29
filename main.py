import os
import pygame
import wave
import pyaudio

def play_mp3(file_path):
    """
    Play an MP3 file using pygame.
    
    :param file_path: Path to the MP3 file.
    """
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        print(f"Playing MP3 file: {file_path}...")
        while pygame.mixer.music.get_busy():
            continue
    except Exception as e:
        print(f"Error during MP3 playback: {e}")

def play_wav(file_path):
    """
    Play a WAV file using pyaudio.
    
    :param file_path: Path to the WAV file.
    """
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    chunk = 1024
    try:
        wf = wave.open(file_path, 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        print(f"Playing WAV file: {file_path}...")
        data = wf.readframes(chunk)
        while data:
            stream.write(data)
            data = wf.readframes(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()
    except Exception as e:
        print(f"Error during WAV playback: {e}")

def record_audio(output_file, record_seconds, channels=2, rate=48000):
    """
    Record audio and save it as a high-quality WAV file.

    :param output_file: Path to save the recorded WAV file.
    :param record_seconds: Duration of the recording in seconds.
    :param channels: Number of audio channels (default is 2 for stereo).
    :param rate: Sampling rate (default is 48000 Hz for better quality).
    """
    chunk = 1024
    p = pyaudio.PyAudio()

    try:
        stream = p.open(format=pyaudio.paInt24,  # 24-bit depth for better quality
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

        print("Recording...")
        frames = []

        for _ in range(0, int(rate / chunk * record_seconds)):
            data = stream.read(chunk)
            frames.append(data)

        print("Recording finished.")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(output_file, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt24))  # Match bit depth
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()
    except Exception as e:
        print(f"Error during recording: {e}")

if __name__ == "__main__":
    # Play an MP3 file
    mp3_file = "welcomeMessage.mp3"
    play_mp3(mp3_file)

    # Record audio and save it as a WAV file
    output_file = "recorded_audio.wav"
    record_seconds = 5  # Record for 5 seconds
    print("Starting audio recording...")
    record_audio(output_file, record_seconds)
    print(f"Audio recorded and saved to {output_file}")

    # Play a WAV file
    play_wav(output_file)
