from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np

src = Image.open(r'C:\Users\jcper\AppData\Local\Temp\codex-clipboard-3a593d5f-4d40-40b4-bab6-347f9863669b.png').convert('RGB')
w,h=src.size
sx,sy=w/1367,h/1823
mask=Image.new('L',src.size)
d=ImageDraw.Draw(mask)
paths=[
[(0,864),(98,900),(189,943),(287,955)],
[(0,1198),(68,1171),(145,1145),(250,1138),(326,1094),(405,1090),(464,1112),(502,1084),(559,1105),(611,1152),(703,1176),(778,1236),(818,1202),(858,1121),(920,1073),(1000,1061),(1105,1052)],
[(352,548),(406,553),(480,576),(536,579),(578,596),(625,627),(654,638),(671,671),(715,682),(786,688),(872,681),(920,656),(976,664),(1022,687)],
[(920,940),(941,874),(969,837),(1007,821),(1054,830),(1134,812),(1193,792)],
[(0,1054),(78,1046)],
[(0,1726),(72,1715),(133,1721)],
[(685,1585),(735,1511),(757,1437),(778,1372),(805,1314),(784,1264)],
[(392,984),(451,986)],
[(290,869),(352,857),(412,859)],
]
for p in paths:
    d.line([(int(x*sx),int(y*sy)) for x,y in p],fill=255,width=int(38*sx),joint='curve')
# Preserve every original pixel in the face, including its natural softness.
protect=Image.new('L',src.size)
pd=ImageDraw.Draw(protect)
pd.ellipse((int(444*sx),int(151*sy),int(800*sx),int(614*sy)),fill=255)
m=np.asarray(mask)>0
safe=np.asarray(protect)>0
m[safe]=False
a=np.asarray(src).astype(np.float32)
original=a.copy()
# Fill narrow damaged strips using only adjacent original image samples.
known=~m
for iteration in range(40):
    sums=np.zeros_like(a); count=np.zeros((h,w),np.float32)
    for dy,dx in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1)):
        k=np.roll(known,(dy,dx),(0,1))
        if dy<0:k[-1,:]=False
        if dy>0:k[0,:]=False
        if dx<0:k[:,-1]=False
        if dx>0:k[:,0]=False
        sums+=np.roll(a,(dy,dx),(0,1))*k[:,:,None]
        count+=k
    fill=(~known)&(count>0)
    if not fill.any():break
    a[fill]=sums[fill]/count[fill,None]
    known[fill]=True
# Harmonic relaxation removes seams in the interpolated strips.
ys,xs=np.where(m)
y0,y1=max(1,ys.min()),min(h-1,ys.max()+1)
x0,x1=max(1,xs.min()),min(w-1,xs.max()+1)
for iteration in range(240):
    avg=(a[y0-1:y1-1,x0:x1]+a[y0+1:y1+1,x0:x1]+a[y0:y1,x0-1:x1-1]+a[y0:y1,x0+1:x1+1])*0.25
    region=a[y0:y1,x0:x1]
    region[m[y0:y1,x0:x1]]=avg[m[y0:y1,x0:x1]]
base=Image.fromarray(np.clip(a,0,255).astype('uint8'))
enh=ImageEnhance.Contrast(base).enhance(1.045)
enh=enh.filter(ImageFilter.UnsharpMask(radius=1.0,percent=35,threshold=5))
out=np.asarray(enh).copy()
out[safe]=original[safe].astype('uint8')
assert np.array_equal(out[safe],np.asarray(src)[safe])
Image.fromarray(out).save(r'C:\Proyectos\instituto\retrato-restaurado-rostro-original.png')
print('Guardado. Verificado: píxeles del rostro idénticos al original. Tamaño:',src.size)
