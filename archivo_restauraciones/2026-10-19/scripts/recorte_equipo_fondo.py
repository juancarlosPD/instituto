from PIL import Image,ImageDraw,ImageFilter
import numpy as np
src=Image.open(r'C:\Users\jcper\AppData\Local\Temp\codex-clipboard-1970e55d-286c-462f-b286-8e759dbf4c95.png').convert('RGB')
w,h=src.size
p=[(30,812),(60,765),(96,722),(132,694),(151,646),(176,596),(207,553),(244,511),(280,478),(313,451),(346,442),(387,449),(419,462),(447,477),(447,453),(429,425),(416,398),(405,370),(397,342),(390,309),(386,276),(384,246),(391,211),(399,174),(420,145),(449,122),(482,106),(515,94),(548,87),(580,87),(611,94),(642,107),(666,126),(685,153),(696,180),(701,216),(704,246),(704,279),(709,307),(701,342),(693,370),(678,405),(664,436),(658,472),(666,508),(683,533),(724,552),(765,577),(805,604),(846,632),(881,660),(900,681),(900,812)]
mask=Image.new('L',(w*3,h*3))
ImageDraw.Draw(mask).polygon([(round(x*w/900*3),round(y*h/812*3)) for x,y in p],fill=255)
mask=mask.resize(src.size,Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(.65))
y,x=np.indices((h,w));v=195-40*np.clip(((x-w*.58)/(w*.85))**2+((y-h*.34)/(h*.95))**2,0,1)
bg=Image.fromarray(np.stack((v+2,v,v-1),axis=2).astype('uint8'))
out=Image.composite(src,bg,mask)
inside=np.asarray(mask)==255
assert np.array_equal(np.asarray(out)[inside],np.asarray(src)[inside])
out.save(r'C:\Proyectos\instituto\retrato-equipo-fondo-gris.png')
