from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np

source=r'C:\Users\jcper\AppData\Local\Temp\codex-clipboard-1e54f128-e336-468d-869f-5398512c14eb.png'
dest=r'C:\Proyectos\instituto\retrato-panuelo-rostro-intacto.png'
im=Image.open(source).convert('RGB')
a=np.asarray(im)
protected=Image.new('L',im.size)
ImageDraw.Draw(protected).ellipse((85,65,462,450),fill=255)
core=np.asarray(protected)==255
# Remove isolated print specks only in the plain background.
median=np.asarray(im.filter(ImageFilter.MedianFilter(5)))
yy,xx=np.indices(a.shape[:2])
background=((yy<65)|((xx<85)&(yy<440))|((xx>470)&(xx<530)&(yy<420)))
specks=(np.max(np.abs(a.astype(float)-median.astype(float)),axis=2)>12)&background&~core
clean=a.copy()
clean[specks]=median[specks]
improved=ImageEnhance.Contrast(Image.fromarray(clean)).enhance(1.07)
improved=improved.filter(ImageFilter.UnsharpMask(radius=0.85,percent=45,threshold=4))
# Smooth transition outside protected area, with no change inside it.
feather=protected.filter(ImageFilter.MaxFilter(21)).filter(ImageFilter.GaussianBlur(6))
mask=np.maximum(np.asarray(protected),np.asarray(feather))
result=Image.composite(im,improved,Image.fromarray(mask))
assert np.array_equal(np.asarray(result)[core],a[core])
assert result.size==im.size
result.save(dest)
print('Verificado: píxeles de cabeza y rostro idénticos al original; tamaño conservado.')
