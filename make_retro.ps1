param(
  [string]$video = "imagination.mp4",
  [string]$frame = "retro-pc.png",
  [string]$out = "retro_banner.gif",
  [double]$left = 0.305,
  [double]$top = 0.194,
  [double]$width = 0.435,
  [double]$height = 0.314,
  [switch]$preview
)

Add-Type -AssemblyName System.Drawing
$img = [System.Drawing.Image]::FromFile((Resolve-Path $frame))
$fw = $img.Width
$fh = $img.Height
$img.Dispose()

$ox = [int]($fw * $left)
$oy = [int]($fh * $top)
$sw = [int]($fw * $width)
$sh = [int]($fh * $height)

$filter = "[1:v]crop=ih*${sw}/${sh}:ih,scale=${sw}:${sh}[v];[0:v][v]overlay=${ox}:${oy}:shortest=1"

if ($preview) {
  .\ffmpeg.exe -y -i $frame -i $video -filter_complex $filter -frames:v 1 preview.png
  Write-Host "Done: preview.png"
}
else {
  .\ffmpeg.exe -y -loop 1 -i $frame -i $video -filter_complex "$filter,scale=800:-1:flags=lanczos,fps=12,split[a][b];[a]palettegen=reserve_transparent=1[p];[b][p]paletteuse=alpha_threshold=128" -loop 0 $out
  Write-Host "Done: $out"
}