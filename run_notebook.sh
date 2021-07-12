#!/bin/bash

stage=$1
basedir=/home/hosung/diquest-demo
filename=$2
#threemodelname="smallfcnn-model-0.9618-quantized.tflite"
threemodelname="3model-183-0.3535-0.9388.tflite"
aedmodelname="11model-035-0.6208-0.8758.tflite"

if [ $stage -eq 0 ]; then
    ffmpeg -loglevel 8 -y -i $basedir/input/$filename -acodec pcm_s16le -ac 1 -ar 16000 $basedir/input/input-16k.wav || exit 1;
    sox --i $basedir/input/input-16k.wav
fi

if [ $stage -eq 1 ]; then
    python3 $basedir/aed-preprob.py $basedir/input/input-16k.wav $basedir/aed-files/ || exit 1;
    find $basedir/aed-files -name '*.wav' | sort > $basedir/input/aed-files.txt || exit 1;
    
    python3 $basedir/aed.py $basedir/model/$aedmodelname $basedir/input/aed-files.txt $basedir/output/aed-result.csv || exit 1;
fi

if [ $stage -eq 2 ]; then
    ffmpeg -loglevel 8 -y -i $basedir/input/$filename -acodec pcm_s16le -ac 1 -ar 48000 $basedir/input/input-48k.wav || exit 1;
    sox --i $basedir/input/input-48k.wav
fi

if [ $stage -eq 3 ]; then
    python3 -W ignore $basedir/asc-preprob.py $basedir/input/input-48k.wav $basedir/asc-files/ || exit 1;
    find $basedir/asc-files -name '*.wav' | sort > $basedir/input/asc-files.txt || exit 1;
    
    python3 -W ignore $basedir/asc.py $basedir/model/$threemodelname $basedir/input/asc-files.txt $basedir/output/aed-result.csv || exit 1;
	rm input/input.wav input/aed-files.txt input/asc-files.txt
	rm aed-files/* asc-files/*
fi


