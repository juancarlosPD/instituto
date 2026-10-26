from PIL import Image,ImageDraw,ImageFilter
import numpy as np
src=Image.open(r'C:\Users\jcper\AppData\Local\Temp\codex-clipboard-7226152f-cf69-4140-87c1-383845c8fa9d.png').convert('RGB')
w,h=src.size
points=[(0,461),(30,429),(58,403),(88,381),(111,372),(149,377),(174,389),(210,391),(223,379),(217,356),(204,329),(194,300),(184,266),(166,239),(158,208),(161,169),(171,139),(190,106),(215,83),(239,67),(269,53),(298,47),(327,48),(349,53),(369,55),(396,66),(418,74),(436,98),(447,125),(451,158),(454,192),(450,222),(456,248),(453,276),(445,303),(433,332),(425,360),(422,395),(431,425),(454,448),(488,469),(524,490),(560,510),(589,534),(589,614),(0,614)]
mask=Image.new('L',(w*3,h*3))
ImageDraw.Draw(mask).polygon([(round(x*w/589*3),round(y*h/614*3)) for x,y in points],fill=255)
mask=mask.resize((w,h),Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(0.65))
y,x=np.indices((h,w))
light=190-37*np.clip(((x-w*.48)/(w*.8))**2+((y-h*.37)/(h*.9))**2,0,1)
bg=np.stack([light+3,light+1,light],axis=2).clip(0,255).astype('uint8')
sharp=src.filter(ImageFilter.UnsharpMask(radius=1.35,percent=90,threshold=4))
out=Image.composite(sharp,Image.fromarray(bg),mask)
out.save(r'C:\Proyectos\instituto\retrato-fondo-gris-rostro-original.png')
print('Guardado con recorte original y enfoque convencional:',out.size)

