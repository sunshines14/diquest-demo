#!/bin/bash

stage=0
basedir=/home/soonshin/sss/workplace/diquest
inputfile=$basedir/input/input285.mp4
modelfile11=$basedir/model/11model-035-0.6208-0.8758.tflite
modelfile3=$basedir/model/3model-183-0.3535-0.9388.tflite


if [ $stage -le 0 ]; then
    ffmpeg -loglevel 8 -y -i $inputfile -acodec pcm_s16le -ac 1 -ar 16000 $basedir/input/input-16k.wav || exit 1;
    sox --i $basedir/input/input-16k.wav
fi

if [ $stage -le 1 ]; then
    python3 -W ignore $basedir/aed-preprob.py $basedir/input/input-16k.wav $basedir/aed-files/ || exit 1;
    find $basedir/aed-files -name '*.wav' | sort > $basedir/input/aed-files.txt || exit 1;
    
    python3 -W ignore $basedir/aed.py $modelfile11 $basedir/input/aed-files.txt $basedir/output/aed-result.csv || exit 1;
fi

if [ $stage -le 2 ]; then
    ffmpeg -loglevel 8 -y -i $inputfile -acodec pcm_s16le -ac 1 -ar 48000 $basedir/input/input-48k.wav || exit 1;
    sox --i $basedir/input/input-48k.wav
fi

if [ $stage -le 3 ]; then
    python3 -W ignore $basedir/asc-preprob.py $basedir/input/input-48k.wav $basedir/asc-files/ || exit 1;
    find $basedir/asc-files -name '*.wav' | sort > $basedir/input/asc-files.txt || exit 1;
    
    python3 -W ignore $basedir/asc.py $modelfile3 $basedir/input/asc-files.txt $basedir/output/asc-result.csv || exit 1;
fi

rm input/input-16k.wav input/input-48k.wav input/aed-files.txt input/asc-files.txt
rm aed-files/* asc-files/*