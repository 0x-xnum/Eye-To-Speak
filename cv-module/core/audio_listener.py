import threading
import speech_recognition as sr

class AudioContextListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.last_heard_sentence = ""
        self.is_listening = False
        self.thread = None

    def _listen_loop(self):
        """
        Background daemon loop that continuously listens to the microphone.
        """
        # Suppress ALSA/Jack warnings if any by redirecting stderr (mostly a Linux issue, but good practice)
        with sr.Microphone() as source:
            # Calibrate ambient noise once at startup
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            while self.is_listening:
                try:
                    # Listen for audio in short bursts
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=5)
                    
                    # Transcribe using Google's free API
                    text = self.recognizer.recognize_google(audio)
                    if text:
                        self.last_heard_sentence = text.lower()
                        print(f"\n[Audio Listener] Heard: '{self.last_heard_sentence}'")
                        
                except sr.WaitTimeoutError:
                    # No speech detected in the timeout window, just continue
                    pass
                except sr.UnknownValueError:
                    # Speech was unintelligible
                    pass
                except sr.RequestError as e:
                    print(f"[Audio Listener] API Error: {e}")
                except Exception as e:
                    pass

    def start(self):
        if not self.is_listening:
            self.is_listening = True
            self.thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.thread.start()
            print("[Audio Listener] Background thread started.")

    def stop(self):
        self.is_listening = False
        if self.thread:
            self.thread.join(timeout=1.0)
            
    def get_context(self):
        return self.last_heard_sentence
        
    def clear_context(self):
        self.last_heard_sentence = ""
