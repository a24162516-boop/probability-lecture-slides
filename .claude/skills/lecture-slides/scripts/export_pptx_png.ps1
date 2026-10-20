# PowerPoint로 .pptx의 모든 슬라이드를 PNG로 내보내기 (렌더링 확인용)
# 사용: powershell -ExecutionPolicy Bypass -File export_pptx_png.ps1 <pptx경로> <출력폴더>
param([Parameter(Mandatory)][string]$Pptx, [Parameter(Mandatory)][string]$OutDir)

$Pptx = (Resolve-Path $Pptx).Path
New-Item -ItemType Directory -Force $OutDir | Out-Null
$OutDir = (Resolve-Path $OutDir).Path
$ppt = New-Object -ComObject PowerPoint.Application
try {
    $pres = $ppt.Presentations.Open($Pptx, $true, $false, $false)
    $i = 0
    foreach ($sl in $pres.Slides) {
        $i++
        $sl.Export((Join-Path $OutDir ("slide{0:D2}.png" -f $i)), "PNG", 1280, 720)
    }
    $pres.Close()
    "exported $i slides -> $OutDir"
} finally {
    $ppt.Quit()
}
