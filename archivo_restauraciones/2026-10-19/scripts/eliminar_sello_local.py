from PIL import Image,ImageFilter
import numpy as np
src=Image.open(r'C:\Users\jcper\AppData\Local\Temp\codex-clipboard-1d16c07c-9393-47c3-9ea3-ba05f0905762.png').convert('RGB')
edit=Image.open(r'C:\Users\jcper\.codex\generated_images\01a1549b-672c-72d2-b519-3e851e7cab33\exec-2a9251e1-d281-4f16-bf7e-ed9b38c7c1a2.png').convert('RGB').resize(src.size,Image.Resampling.LANCZOS)
a=np.asarray(src).astype(float)
yy,xx=np.indices(a.shape[:2])
ink=(a[:,:,2]>a[:,:,0]-5)&(a[:,:,2]>a[:,:,1]+3)&(yy>src.height*0.395)
alpha=np.broadcast_to(np.clip((yy[:,0]-src.height*0.386)/(src.height*0.025),0,1)[:,None],yy.shape)
alpha=(alpha*255).astype('uint8')
result=Image.composite(edit,src,Image.fromarray(alpha))
safe=alpha==0
assert np.array_equal(np.asarray(result)[safe],np.asarray(src)[safe])
result.save(r'C:\Proyectos\instituto\retrato-sin-sello.png')
print('Guardado; áreas fuera de la máscara conservadas exactamente.')
