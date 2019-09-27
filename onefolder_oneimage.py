
import cv2
import numpy as np
import os
import shutil
from numba import jit
@jit
def drawImgFonts(img, strContent):

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontSize = 3
    cv2.putText(img, strContent, (0, 200), font, fontSize, (0, 255, 0), 6)

    return img
@jit
def give_score(score,x,y,f):
    for i in range(x - 1):
        for j in range(y - 1):
            #score += np.abs(f[i + 1, j] - f[i, j]) * np.abs(f[i, j] - f[i, j + 1])
            score += np.abs(f[i + 1, j] - f[i, j]) * np.abs(f[i, j] - f[i, j + 1]) * np.abs(f[i, j] - f[i+1, j + 1]) * np.abs(f[i+1, j] - f[i, j + 1])
    return score

def SMD2Detection(root,curdir):
    max_score = 0
    out_image = None
    names = os.listdir(root + "/" + curdir)
    for imgname in names:
        if imgname.split('.')[-1] == "bmp":

            img = cv2.imread(root+"/"+curdir+"/"+imgname)
            width,height = img.shape[:2][::-1]
            img_resize = cv2.resize(img,(int(width*0.8),int(height*0.8)),interpolation=cv2.INTER_CUBIC)
            img2gray = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
            f = np.asmatrix(img2gray) / 255.0
            x, y = f.shape
            score = 0
            score = give_score(score,x,y,f)
            # for i in range(x - 1):
            #     for j in range(y - 1):
            #         score += np.abs(f[i + 1, j] - f[i, j]) * np.abs(f[i, j] - f[i, j + 1])
            #         #score += np.abs(f[i + 1, j] - f[i, j]) * np.abs(f[i, j] - f[i, j + 1]) * np.abs(f[i, j] - f[i+1, j + 1]) * np.abs(f[i+1, j] - f[i, j + 1])
            if score>max_score:
                out_image = imgname
                max_score = score
    if out_image:
        newImg = drawImgFonts(cv2.imread(root+"/"+curdir+"/"+out_image), str(score))

        newPath = root+'/' +curdir+"_w_"+imgname
        cv2.imwrite(newPath, newImg)  # 保存图片
    else:return 0
    return str(score)

if __name__ == "__main__":
    rw = r"/media/wangu/新加卷/荧光清晰度测试/"
    roots = os.listdir(rw)
    # for path in pathes:
    #     if path[-1] == "t":
    #         shutil.rmtree(root+'/'+path)
    # pathes = os.listdir(root)
    #对每个子文件夹
    for root in roots:
        pathes = os.listdir(rw+root)
        for path in pathes:
            print(path)
            if path[-1] != "t" :

                x = SMD2Detection(rw+root,path)
            # names = os.listdir(root+"/"+path)
            # print(names)
            # score = []
            # for imgname in names:
            #     if imgname.split('.')[-1]=="bmp":
            #         score.append(SMD2Detection(root,path,imgname))
            # filename = "res.txt"
            # if os.path.exists(root+'/'+path+'test/'+filename):
            #     os.remove(root+'/'+path+'test/'+filename)
            # fd = open(root+'/'+path+'test/'+filename, mode="w", encoding="utf-8")
            # fd.write("\n".join(i for i in score))
            # fd.close()





    # path = "bb/"
    # names = os.listdir(path)
    # print(names)
    # for imgname in names:
    #     SMD2Detection(path,imgname)





