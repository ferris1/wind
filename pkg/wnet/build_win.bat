go build -o wnet.dll -buildmode=c-shared ./
xcopy ./wnet.dll ../builds
pause