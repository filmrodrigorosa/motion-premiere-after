#!/bin/zsh
# Compõe um render do AE (PNG com alpha) sobre o quadro real do vídeo naquele tempo da timeline.
# uso: preview_sobre_video.sh <render.png> <tempo_timeline_s> <saida.png> <mapa.json> <video_fonte>
# mapa.json: [{"inicio": s_timeline, "in": s_midia, "dur": s}]
PNG=$1; T=$2; OUT=$3; MAPA=$4; VID=$5
SRC=$(python3 -c "
import json; t=$T
for c in json.load(open('$MAPA')):
    if c['inicio']<=t<c['inicio']+c['dur']: print(c['in']+t-c['inicio']); break")
[ -z "$SRC" ] && { echo "tempo $T fora da timeline"; exit 1; }
ffmpeg -loglevel error -y -ss $SRC -i "$VID" -i "$PNG" -frames:v 1 \
  -filter_complex "[1][0]scale2ref[o][v];[v][o]overlay,scale=1280:-1" "$OUT" && echo "$OUT"
