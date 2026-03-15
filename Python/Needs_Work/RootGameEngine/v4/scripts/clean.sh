# everything in the main file
rm -rf __pycache__/ render/
rm out.mp4
rm test_texture.bmp
# inside the Engine folder
cd Engine
rm -rf __pycache__/ build/
rm Rasterizer.c*
# inside the Logic folder
cd ../Logic
rm -rf __pycache__/
