import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance
import os
from datetime import datetime
#깃연동
#깃연동

def save_uploaded_file(directory,img):
    #디렉토리와 이미지를 주면 해당 디렉토리에 이미지를 처리하는함수
    #1. 디렉토리가 있는지 확인하여 없으면 만든다.
    if not os.path.exists(directory) :
        os.makedirs(directory)
    #2. 이제는 디렉토리가 있으니까 파일을 저장
    filename = datetime.now().isoformat().replace(':','-').replace('.','-')
    img.save(directory+'/'+filename+'.png')
    return st.success("Saved file : {} in {}".format(filename+'.png',directory))

def load_image(imgae_file):
    img=Image.open(imgae_file)
    return img

def main():
    datetime.now().isoformat()
    st.subheader("이미지파일 업로드")
    imgae_file = st.file_uploader("Upload Image",type=["png","jpg","jpeg"],accept_multiple_files=True)
    
    print(imgae_file)
    if imgae_file is not None :
        #2-1.모든 파일이 image_list에 이미지로 저장됨.
        image_list = []
        for img_file in imgae_file:

            img = load_image(img_file)
            image_list.append(img)
    
        #save_button = st.button('버튼을 누르면 저장됩니다.')                 
        #text_name = st.text_input('디렉토리 이름을 입력하세요')
        option_list = ['show Image','Rotate Image','Create Thumbnail','Crop Image','Merge Images',
        'Flip Image','Chage color','Filters - Sharpen','Filters - Edge Enhance','Contrast Image']
        option = st.selectbox('옵션을 선택하세요.',option_list)

        if option == 'show Image' :
            
            #3. 이미지를 화면에 확인해 본다.    
            for img in image_list:
                st.image(img)

            directory = st.text_input('파일 경로 입력')
            if st.button('파일 저장') :
                #3.파일 저장.
                for img in image_list :
                    save_uploaded_file(directory,img)    
                #if save_button:
                    #save_uploaded_file(text_name, img_file)
                    

                
        elif option == 'Rotate Image':
            #1.유저가 입력
            transformed_img_list = []
            number = st.number_input('각도 입력',0,360)
            #2.모든 이미지를 돌린다.
            for img in image_list:
                #img = load_image(img_file)
                rotated_img = img.rotate(number)
                st.image(rotated_img)
                transformed_img_list.append(rotated_img)
            
            directory = st.text_input('파일 경로 입력')
            if st.button('파일 저장') :
                #3.파일 저장.
                for img in transformed_img_list :
                    save_uploaded_file(directory,img)

            
        elif option == 'Create Thumbnail':
            #1. 이미지의 사이즈를 알아야겠다.
            
            size = st.number_input('가로 입력',1,100)
            size1 = st.number_input('세로 입력',1,100)
            size2=(size,size1)
            transformed_img_list=[]
            for img in image_list:
                img.thumbnail(size2)
                st.image(img)
                transformed_img_list.append(img)
            
            directory = st.text_input('파일 경로 입력')
            if st.button('파일 저장') :
                #3.파일 저장.
                for img in transformed_img_list :
                    save_uploaded_file(directory,img)



        elif option == 'Crop Image':
            size5 = st.number_input('statt x',0,img.size[0]-1)
            size6 = st.number_input('start y',0,img.size[1]-1)
            max_width = img.size[0] - size5
            max_height = img.size[1] - size6
            size7 = st.number_input('x',1,max_width)
            size8 = st.number_input('y',1,max_height)
            box = (size5,size6,size5+size7,size6+size8)  
            cropped_img = img.crop(box)
            st.image(cropped_img)
        
        elif option == 'Merge Images':
            merge_file = st.file_uploader("Upload Image",type=["png","jpg","jpeg"],key='merge')
            
            
            if merge_file is not None :
                log_img = Image.open(merge_file)
                start_x = st.number_input('시작 x 좌표',0,img.size[0])
                start_y = st.number_input('시작 y 좌표',0,img.size[1])
                position = (start_x,start_y)
                img.paste(log_img,position)
                st.image(img)
                
        elif option == 'Flip Image' :
            status = st.radio('플립을 선택하세요.',['FLIP_TOP_BOTTOM','FLIP_LEFT_RIGHT'])
            if status == 'FLIP_TOP_BOTTOM':
                transformed_img_list=[]
                for img in image_list:
                    flippen_img=img.transpose(Image.FLIP_TOP_BOTTOM)
                    st.image(flippen_img)
                    transformed_img_list.append(flippen_img)
            else :
                transformed_img_list=[]
                for img in image_list:
                    flippen_img=img.transpose(Image.FLIP_LEFT_RIGHT)
                    st.image(flippen_img)
                    transformed_img_list.append(flippen_img)

            directory = st.text_input('파일 경로 입력')
            if st.button('파일 저장') :
                #3.파일 저장.
                for img in transformed_img_list :
                    save_uploaded_file(directory,img)    

        
        elif option == 'Chage color' :
            option_list_selete = ['1','L','RGB']
            con_img=st.selectbox('컬러선택해주세요',option_list_selete)
            if con_img == '1' :
                bw = img.convert('1')
                st.image(bw)
            elif con_img == 'L' :
                bw = img.convert('L')
                st.image(bw)
            else :
                bw = img.convert('RGB')
                st.image(bw)
            # status = st.radio('색 변경',['Color','Gray Scale','Black & White'])

            # if status == 'Color':
            #     color = 'RGB'
            # elif status == 'Gray Scale':   
            #     color = 'L'
            # else :
            #     color = '1'

            # bw = img.convert(color)
            # st.image(bw)     





        elif option == 'Filters - Sharpen':
            sharp_img = img.filter(ImageFilter.SHARPEN)
            st.image(sharp_img)

        elif option == 'Filters - Edge Enhance':
            edge_img = img.filter(ImageFilter.EDGE_ENHANCE)
            st.image(edge_img)    

        elif option == 'Contrast Image' :
            contrast_img = ImageEnhance.Contrast(img).enhance(2)
            st.image(contrast_img)


     



if __name__ == '__main__' :
    main()       