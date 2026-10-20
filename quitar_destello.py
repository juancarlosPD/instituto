from PIL import Image, ImageDraw, ImageFilter
import numpy as np
src=Image.open(r'C:\Users\jcper\AppData\Local\Temp\codex-clipboard-f97a3966-73fa-421c-96d7-8f165ca13a88.png').convert('RGB')
edit=Image.open(r'C:\Users\jcper\.codex\generated_images\01a1549b-672c-72d2-b519-3e851e7cab33\exec-439641b6-e662-417c-b072-e96c702d6627.png').convert('RGB').resize(src.size,Image.Resampling.LANCZOS)
mask=Image.new('L',src.size)
ImageDraw.Draw(mask).ellipse((58,269,206,369),fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(9))
alpha=np.asarray(mask).copy()
alpha[alpha<3]=0
out=Image.composite(edit,src,Image.fromarray(alpha))
unchanged=alpha==0
assert np.array_equal(np.asarray(out)[unchanged],np.asarray(src)[unchanged])
out.save(r'C:\Proyectos\instituto\retrato-sin-destello.png')
print('Verificado: fuera de la zona del destello no cambia ningún píxel.')
