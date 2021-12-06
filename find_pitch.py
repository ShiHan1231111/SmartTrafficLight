import os
import glob
import time
import librosa
import librosa.display
import matplotlib.style as ms
import sounddevice as sd
from scipy.io.wavfile import write

ms.use('seaborn-muted')


def record_audio():
    fs = 8000  # Sample rate
    seconds = 10  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished

    save_path = r'record_sirens_audio'

    named_tuple = time.localtime()  # get struct_time
    time_string = time.strftime("%m-%d-%Y_%H%M%S", named_tuple)

    filename = os.path.join(save_path, time_string + ".wav")

    write(filename, fs, myrecording)

    detect_pitch(filename)


def camdf(y, sr, tau, N):
    D = 0.0
    for n in range(N):
        D += abs(y[(n + tau) % N] - y[n])
    return D


def detect_pitch(filename):
    # Reading the audio file
    print(filename)
    y, sr = librosa.load(filename, sr=8000)

    camdf_list = []

    N = len(y[:513])
    start = time.time()
    for i in range(512):
        camdf_list.append(camdf(y=y, sr=sr, tau=i, N=N))
    end = time.time()
    print("Execution time for CAMDF is {} secs".format(round((end - start), 4)))

    interval = camdf_list[4:100]
    min_D = min(interval)
    pitch_detected = round(sr / (interval.index(min_D) + 4), 2)
    print("Detected Pitch: {} Hz".format(pitch_detected))

    if 990 <= pitch_detected <= 1250:
        print("Doppler effect detected.")
    else:
        print("Not doppler effect detected")


def main():
    while True:
        try:
            record_audio()
            time.sleep(1)

        except KeyboardInterrupt:
            break
        except TypeError:
            print("Type Error occurs")
            break
        except IOError:
            print("IO Error Occurs")
            break


if __name__ == "__main__":
    main()
