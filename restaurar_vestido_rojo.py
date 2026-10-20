from PIL import Image,ImageDraw,ImageFilter,ImageEnhance
import numpy as np
src=Image.open(r'C:\Users\jcper\AppData\Local\Temp\codex-clipboard-54b0047f-ab52-4e14-af57-ce1318511c87.png').convert('RGB')
w,h=src.size
mask=Image.new('L',src.size)
ImageDraw.Draw(mask).ellipse((int(390*w/1280),int(260*h/1976),int(925*w/1280),int(770*h/1976)),fill=255)
a=np.asarray(src)
median=np.asarray(src.filter(ImageFilter.MedianFilter(5)))
core=np.asarray(mask)==255
delta=np.max(np.abs(a.astype(float)-median.astype(float)),axis=2)
spots=(delta>16)&~core
clean=a.copy();clean[spots]=median[spots]
edited=ImageEnhance.Contrast(Image.fromarray(clean)).enhance(1.055)
edited=edited.filter(ImageFilter.UnsharpMask(radius=1.05,percent=40,threshold=5))
soft=mask.filter(ImageFilter.MaxFilter(31)).filter(ImageFilter.GaussianBlur(9))
alpha=np.maximum(np.asarray(mask),np.asarray(soft))
result=Image.composite(src,edited,Image.fromarray(alpha))
assert np.array_equal(np.asarray(result)[core],a[core])
assert result.size==src.size
result.save(r'C:\Proyectos\instituto\retrato-vestido-rojo-restaurado.png')
print('Verificado: píxeles faciales originales y dimensiones conservadas:',src.size)
