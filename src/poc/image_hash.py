from PIL import Image
import imagehash

original = Image.open('images/sources/Flecha.png')
original.save("images/output/original.png", "PNG")
#original.show("original")
original_color_hash = imagehash.colorhash(original, 18)
print(f"original_color_hash:         {str(original_color_hash)}")
original_phash = imagehash.phash(original,16)
print(f"original_phash:              {str(original_phash)}")

flip_left_right = original.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
flip_left_right.save("images/output/flip_left_right.png", "PNG")
#flip_left_right.show("flip_left_right")
flip_left_right_color_hash = imagehash.colorhash(flip_left_right, 18)
print(f"flip_left_right_color_hash:  {str(flip_left_right_color_hash)}")
flip_left_right_phash = imagehash.phash(flip_left_right,16)
print(f"flip_left_right_phash:       {str(flip_left_right_phash)}")

flip_top_bottom = original.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
flip_top_bottom.save("images/output/flip_top_bottom.png", "PNG")
#flip_top_bottom.show("flip_top_bottom")
flip_top_bottom_color_hash = imagehash.colorhash(flip_top_bottom, 18)
print(f"flip_top_bottom_color_hash:  {str(flip_top_bottom_color_hash)}")
flip_top_bottom_phash = imagehash.phash(flip_top_bottom,16)
print(f"flip_top_bottom_phash:       {str(flip_top_bottom_phash)}")

rotate_90 = original.transpose(Image.Transpose.ROTATE_90)
rotate_90.save("images/output/rotate_90.png", "PNG")
#rotate_90.show(rotate_90)
rotate_90_color_hash =  imagehash.colorhash(rotate_90, 18)
print(rotate_90_color_hash)

rotate_180 = original.transpose(Image.Transpose.ROTATE_180)
rotate_180.save("images/output/rotate_180.png", "PNG")
#rotate_180.show("rotate_180")
rotate_180_color_hash =  imagehash.colorhash(rotate_180, 18)
print(rotate_180_color_hash)

rotate_270 = original.transpose(Image.Transpose.ROTATE_270)
rotate_270.save("images/output/rotate_270.png", "PNG")
#rotate_270.show("rotate_270")
rotate_270_color_hash =  imagehash.colorhash(rotate_270, 18)
print(rotate_270_color_hash)

transverse = original.transpose(Image.Transpose.TRANSVERSE)
transverse.save("images/output/transverse.png", "PNG")
#transverse.show("transverse")
transverse_color_hash =  imagehash.colorhash(transverse, 18)
print(transverse_color_hash)

print(f"flip_top_bottom_color_hash:  len={len(str(flip_top_bottom_color_hash))}")
print(f"flip_top_bottom_phash:       len={len(str(flip_top_bottom_phash))}")
