from PIL import Image

SUPPORTED_EXTENSIONS = { ex for ex, _ in Image.registered_extensions().items()}

max = 0
min = 2**32
for x in SUPPORTED_EXTENSIONS:
    if len(x) < min:
        min = len(x)
        shortest = x

    if len(x) > max:
        max = len(x)
        longest = x

print(min, max)
print(shortest, longest)
