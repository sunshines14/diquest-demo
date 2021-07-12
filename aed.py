import sys
import librosa
import datetime
import numpy as np
import tensorflow as tf
import soundfile as sound


model_path = sys.argv[1]
infile = sys.argv[2]
outfile = sys.argv[3]

sr = 16000
duration = 0.4
num_freq_bin = 40
num_fft = 321
hop_length = int(num_fft / 2)
num_time_bin = int(np.ceil(duration * sr / hop_length))
num_channel = 1
use_delta = False

classes = [['baby'],['bicycle'],['boiling'],['car'],['carpassing'],
           ['dog'],['door'],['jackhammer'],['scream'],['speech'],['unknown']]


def deltas(X_in):
    X_out = (X_in[:,:,2:,:]-X_in[:,:,:-2,:])/10.0
    X_out = X_out[:,:,1:-1,:]+(X_in[:,:,4:,:]-X_in[:,:,:-4,:])/5.0
    return X_out


def feats(wavpath):
    y, sr = sound.read(wavpath)
    logmel_data = np.zeros((num_freq_bin, num_time_bin, num_channel), 'float32')
    
    max_len = int(duration*sr)
    y_len = len(y)
    if y_len >= max_len:
        y = y[:max_len]
    else:
        num_repeats = round((max_len/y_len) + 1)
        y_repeat = y.repeat(num_repeats, 0)
        padded_y = y_repeat[:max_len]
        y = padded_y
    
    logmel_data[:,:,0] = librosa.feature.melspectrogram(y[:], 
                                                        sr=sr, 
                                                        n_fft=num_fft, 
                                                        hop_length=hop_length,
                                                        n_mels=num_freq_bin, 
                                                        fmin=0.0, 
                                                        fmax=sr/2, 
                                                        htk=True, 
                                                        norm=None)
    
    logmel_data = np.log(logmel_data+1e-8)
    #for j in range(len(logmel_data[:,:,0][:,0])):
    #    mean = np.mean(logmel_data[:,:,0][j,:])
    #    std = np.std(logmel_data[:,:,0][j,:])
    #    logmel_data[:,:,0][j,:] = ((logmel_data[:,:,0][j,:]-mean)/std)
    #    logmel_data[:,:,0][np.isnan(logmel_data[:,:,0])]=0.
    return logmel_data


def time(sec):
    return str(datetime.timedelta(seconds=sec))


def process(i, threshold, logmel_data, outfile, model):
    unknown_flag = False
    
    if use_delta:
        logmel_data_deltas = deltas(logmel_data)
        logmel_data_deltas_deltas = deltas(logmel_data_deltas)
        logmel_data = np.concatenate((logmel_data[:,:,4:-4,:], logmel_data_deltas[:,:,2:-2,:], logmel_data_deltas_deltas), axis=-1)
        
    input_index = model.get_input_details()[0]["index"]
    output_index = model.get_output_details()[0]["index"]
    
    test_image = np.expand_dims(logmel_data, axis=0).astype(np.float32)
    model.set_tensor(input_index, test_image)
    model.invoke()
    softmax = model.get_tensor(output_index)
    result = np.argmax(softmax[0])
    
    if float(softmax[0][int(result)]) > threshold:
        unknown_flag = False
        out_softmax = softmax
        out_result = result
        out_classes = classes
    else:
        unknown_flag = True
        
    if unknown_flag == True:
        outfile.write(str(time(round(i*0.1,1))) + ',' + str(0.0) + ',' + 'unknown')
        outfile.write('\n')
        #print(round(i*0.1,1), 'unknown')
        print(time(round(i*0.1,1)), 'unknown')
    else:
        outfile.write(str(time(round(i*0.1,1))) + ',' + str(out_softmax[0][int(out_result)]) + ',' + out_classes[int(out_result)][0])
        outfile.write('\n')
        #print(round(i*0.1,1), out_softmax[0][int(out_result)], out_classes[int(out_result)][0])
        print(time(round(i*0.1,1)), out_softmax[0][int(out_result)], out_classes[int(out_result)][0])


if __name__ == "__main__":
    model = tf.lite.Interpreter(model_path=model_path)
    model.allocate_tensors()
    
    with open(infile, 'r') as infile:
        with open(outfile, 'w') as outfile:
            outfile.write('onset' + ',' + 'score' + ',' + 'predict')
            outfile.write('\n')
            files = infile.readlines()
            
            for i in range(len(files)):
                wavpath = files[i].replace('\n','')
                logmel_data = feats(wavpath)
                i = int(wavpath.split('/')[-1].replace('.wav',''))
                threshold = 0.5
                process(i, threshold, logmel_data, outfile, model)
                