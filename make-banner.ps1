param(
  [string]$video = "imagination.mp4",
  [string]$out = "tv_banner.gif"
)

.\ffmpeg.exe -y -loop 1 -i tv.png -i $video -filter_complex "[1:v]crop=ih*246/188:ih,scale=246:188[v];[0:v][v]overlay=138:308:shortest=1,fps=15,split[a][b];[a]palettegen=reserve_transparent=1[p];[b][p]paletteuse=alpha_threshold=128" -loop 0 $out

Write-Host "Done: $out"