#!/bin/bash

stage=$1
basedir=/home/hosung/diquest-demo
filename=$2
#threemodelname="smallfcnn-model-0.9618-quantized.tflite"
threemodelname="3model-059-0.4510-0.8757.tflite"

if [ $stage -eq 0 ]; then
    ffmpeg -loglevel 8 -y -i $basedir/input/$filename -acodec pcm_s16le -ac 1 -ar 16000 $basedir/input/input.wav || exit 1;
    sox --i $basedir/input/input.wav
fi

if [ $stage -eq 1 ]; then
    python3 $basedir/aed-preprob.py $basedir/input/input.wav $basedir/aed-files/ || exit 1;
    find $basedir/aed-files -name '*.wav' | sort > $basedir/input/aed-files.txt || exit 1;
    
    python3 $basedir/aed.py $basedir/model/11model-194-0.6464-0.8788.tflite $basedir/input/aed-files.txt $basedir/output/aed-result.csv || exit 1;
fi

if [ $stage -eq 2 ]; then
    python3 $basedir/asc-preprob.py $basedir/input/input.wav $basedir/asc-files/ || exit 1;
    find $basedir/asc-files -name '*.wav' | sort > $basedir/input/asc-files.txt || exit 1;
    
    python3 $basedir/asc.py $basedir/model/$threemodelname $basedir/input/asc-files.txt $basedir/output/aed-result.csv || exit 1;
	rm input/input.wav input/aed-files.txt input/asc-files.txt
	rm aed-files/* asc-files/*
fi


