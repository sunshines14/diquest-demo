#!/bin/bash

stage=0
basedir=/home/soonshin/sss/workplace/diquest

if [ $stage -le 0 ]; then
    ffmpeg -loglevel 8 -y -i $basedir/input/input.mp3 -acodec pcm_s16le -ac 1 -ar 16000 $basedir/input/input-16k.wav || exit 1;
    sox --i $basedir/input/input-16k.wav
fi

if [ $stage -le 1 ]; then
    python3 $basedir/aed-preprob.py $basedir/input/input-16k.wav $basedir/aed-files/ || exit 1;
    find $basedir/aed-files -name '*.wav' | sort > $basedir/input/aed-files.txt || exit 1;
    
    python3 $basedir/aed.py $basedir/model/11model-194-0.6464-0.8788.tflite $basedir/input/aed-files.txt $basedir/output/aed-result.csv || exit 1;
fi

if [ $stage -le 2 ]; then
    ffmpeg -loglevel 8 -y -i $basedir/input/input.mp3 -acodec pcm_s16le -ac 1 -ar 48000 $basedir/input/input-48k.wav || exit 1;
    sox --i $basedir/input/input-48k.wav
fi

if [ $stage -le 3 ]; then
    python3 $basedir/asc-preprob.py $basedir/input/input-48k.wav $basedir/asc-files/ || exit 1;
    find $basedir/asc-files -name '*.wav' | sort > $basedir/input/asc-files.txt || exit 1;
    
    python3 $basedir/asc.py $basedir/model/3model-191-0.3737-0.9384.tflite $basedir/input/asc-files.txt $basedir/output/asc-result.csv || exit 1;
fi

rm input/input.wav input/input-16k.wav input/input-48k.wav input/aed-files.txt input/asc-files.txt
rm aed-files/* asc-files/*