from poc.similarities import dup_files

pictures = dup_files("/shared/FotosVarias/DearMathImNot.jpg")

hash_groups = pictures.HashGroups()
print(f"{len(hash_groups)=}")
for k,v in hash_groups.items():
    last_k = k
    if len(v) > 1:
        print(k, len(v))

print(len(k))        
print(len(last_k))