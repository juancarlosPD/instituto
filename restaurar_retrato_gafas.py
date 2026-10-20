from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
src=Image.open(r'C:\Users\jcper\AppData\Local\Temp\codex-clipboard-b203d1be-32d5-4d06-9430-5315479c2fa3.png').convert('RGB')
w,h=src.size
mask=Image.new('L',src.size)
ImageDraw.Draw(mask).ellipse((int(315*w/1437),int(260*h/1760),int(1180*w/1437),int(1090*h/1760)),fill=255)
original=np.asarray(src)
# Clean small isolated spots only in plain background, away from the head.
median=np.asarray(src.filter(ImageFilter.MedianFilter(5)))
yy,xx=np.indices((h,w))
background=((xx<w*0.20)&(yy<h*0.48))|((xx>w*0.88)&(yy<h*0.36))|(yy<h*0.03)
spots=(np.max(np.abs(original.astype(float)-median.astype(float)),axis=2)>10)&background
clean=original.copy()
clean[spots]=median[spots]
improved=ImageEnhance.Contrast(Image.fromarray(clean)).enhance(1.055)
improved=improved.filter(ImageFilter.UnsharpMask(radius=1.1,percent=40,threshold=5))
soft=mask.filter(ImageFilter.MaxFilter(31)).filter(ImageFilter.GaussianBlur(9))
alpha=np.maximum(np.asarray(mask),np.asarray(soft))
result=Image.composite(src,improved,Image.fromarray(alpha))
core=np.asarray(mask)==255
assert np.array_equal(np.asarray(result)[core],original[core])
result.save(r'C:\Proyectos\instituto\retrato-gafas-restaurado-rostro-intacto.png')
print('Verificado: zona facial idéntica al original; dimensiones:',src.size)
