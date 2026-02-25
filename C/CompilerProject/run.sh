clear
gcc main.c -o main
./main test.tc out.txt
rm main
echo
echo "---compiled output---"
cat out.txt
echo
echo "---Tree Script interperted output---"
python3 ~/Programming/Personal_projects/Python/Working/Tree_script/interperter_v2/code/main.py out.txt
