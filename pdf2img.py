import os
import glob
from pdf2image import convert_from_path
from tqdm import tqdm
import shutil

if __name__ == "__main__":
    # target_path : pdf 문서가 있는 경로
    target_path = "./pdf/*.pdf" 
    
    # 파일 list 가져오기
    file_list = glob.glob(target_path)
    for file in tqdm(file_list):
        # PDF 문서에서 Image 추출하기
        f = os.path.basename(file)
        filenm = os.path.splitext(f)[0]  # 파일명만 추출 (확장자 제외)
        subdir = os.path.basename(os.path.dirname(file))  # 상위 디렉토리명 추출
        # new_path = os.path.join("./images", subdir)  # 운영체제에 맞는 경로 생성
        new_path = os.path.join("./pdf", filenm)
        print(filenm)
        print(subdir)
        # print(new_path)
        
        os.makedirs(new_path, exist_ok=True)
        
        try:
            images = convert_from_path(file, 300)# 300 -> dpi / fmt='jpg', output_folder=new_path
        except Exception as e:#간혹 empty stream Document가 있을 경우 대비
            print("%s:%s"%(file, e))
            continue
            
        for idx, image in enumerate(images, start=1):
            f_nm = os.path.splitext(filenm)[0]
            ext = os.path.splitext(filenm)[1]
            #print("Saved Image:%s"%f_nm+"_"+str(idx)+ext)
            image.save(new_path + f'/{f_nm}-{idx}.jpg', 'JPEG')
            
        src = os.path.join("./pdf", f)
        dst = os.path.join(new_path, f)
        shutil.move(src, dst)