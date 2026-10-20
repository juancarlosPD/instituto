from PIL import Image, ImageDraw, ImageFilter
import numpy as np
original=Image.open(r'C:\Users\jcper\AppData\Local\Temp\codex-clipboard-ecf0bbb5-cb44-4a33-8e06-10865bdc46d6.png').convert('RGB')
restored=Image.open(r'C:\Users\jcper\.codex\generated_images\01a1549b-672c-72d2-b519-3e851e7cab33\exec-f2666155-a23b-41cb-82a7-31edf5be4c3c.png').convert('RGB').resize(original.size,Image.Resampling.LANCZOS)
w,h=original.size
mask=Image.new('L',(w,h))
d=ImageDraw.Draw(mask)
points=[(320,335),(350,240),(440,120),(540,70),(674,70),(788,120),(875,230),(925,370),(927,520),(916,625),(882,696),(770,700),(746,648),(704,623),(625,623),(551,587),(486,580),(441,650),(358,636),(324,558)]
d.polygon([(round(x*w/1367),round(y*h/1823)) for x,y in points],fill=255)
# Feather only outside protected head; all pixels inside remain untouched.
feather=mask.filter(ImageFilter.MaxFilter(31)).filter(ImageFilter.GaussianBlur(8))
alpha=np.maximum(np.asarray(mask),np.asarray(feather))
result=Image.composite(original,restored,Image.fromarray(alpha))
protected=np.asarray(mask)==255
assert np.array_equal(np.asarray(result)[protected],np.asarray(original)[protected])
result.save(r'C:\Proyectos\instituto\fotografia-restaurada-cara-intacta.png')
print('Verificado: cabeza y rostro originales, sin cambios de píxeles. Tamaño:',result.size)
