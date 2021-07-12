import sys
import soundfile as sound
import numpy as np

NORM = False

def preprob(input_path, output_path):
    y, sr = sound.read(input_path)
    duration = y.shape[0]/16000
    
    seconds_division = 50
    window_length = int(16000/seconds_division)
    y_abs = np.absolute(y)
    y_mean = y_abs.mean()
    
    k = 5
    ratio = 0.3
    sec = 16000
    win = 10
    cnt = 0
    total_length = int(duration*seconds_division)/k
    
    if NORM :
        for n in range(5):
            normalized = []
            for i in range(n*int(total_length), (n+1)*int(total_length)):
                #if i % 1000 == 0:
                #    print (i)
                window = y[i*window_length : (i+1)*window_length]
                window_abs = np.absolute(window)
                if (window_abs.mean() > y_mean*ratio):
                    normalized = np.concatenate((normalized, window))
                else:
                    zero_window = np.zeros(window.shape)
                    normalized = np.concatenate((normalized, zero_window))
            print("iteration:",n, "duration:",duration/k, "normalized_duration:",normalized.shape[0]/16000)
            for i in range(int(normalized.shape[0]/sec)-3):
                cnt = cnt+1
                sound.write(output_path + '{:05}'.format(cnt) + '.wav', normalized[i*sec : (i+win)*sec], 16000)
            print("number of accumulated files:",cnt)
    else:
        for i in range(int(y.shape[0]/sec)):
            cnt = cnt+1
            sound.write(output_path + '{:05}'.format(cnt) + '.wav', y[i*sec : (i+win)*sec], 16000)
        print("number of accumulated files:",cnt)
    
if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    preprob(input_path, output_path)
