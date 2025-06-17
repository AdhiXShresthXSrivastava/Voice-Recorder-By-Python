import pyaudio
import wave
import keyboard
import time
import os

class VoiceRecorder:
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.recording = False
        self.frames = []
        self.p = pyaudio.PyAudio()
        
    def start_recording(self):
        print("Recording started... Press 'q' to stop recording")
        self.recording = True
        self.frames = []
        
        stream = self.p.open(format=self.FORMAT,
                           channels=self.CHANNELS,
                           rate=self.RATE,
                           input=True,
                           frames_per_buffer=self.CHUNK)
        
        while self.recording:
            data = stream.read(self.CHUNK)
            self.frames.append(data)
            
            if keyboard.is_pressed('q'):
                self.recording = False
                
        stream.stop_stream()
        stream.close()
        
    def save_recording(self, filename="recording.wav"):
        if not os.path.exists("recordings"):
            os.makedirs("recordings")
            
        filepath = os.path.join("recordings", filename)
        wf = wave.open(filepath, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print(f"Recording saved as {filepath}")
        
    def close(self):
        self.p.terminate()

def main():
    recorder = VoiceRecorder()
    try:
        print("Press 'r' to start recording")
        while True:
            if keyboard.is_pressed('r'):
                recorder.start_recording()
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                recorder.save_recording(f"recording_{timestamp}.wav")
                print("Press 'r' to start a new recording or 'q' to quit")
            if keyboard.is_pressed('q'):
                break
    finally:
        recorder.close()

if __name__ == "__main__":
    main()
