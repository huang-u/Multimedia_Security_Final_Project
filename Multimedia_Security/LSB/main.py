import numpy as np
import matplotlib.pyplot as plt
import cv2
import Attack
import os
from skimage import metrics

# =====================================
# 計算圖像品質
# =====================================
def PSNR(img1, img2, data_range=255):
    PSNR = metrics.peak_signal_noise_ratio(img1, img2, data_range=data_range)
    return PSNR

def SSIM(img1, img2):
    # 將影像轉換為灰度
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    SSIM = metrics.structural_similarity(img1, img2, full=True, win_size=7)
    return SSIM[0]

# =====================================
# 進行彩色浮水印的嵌入
# =====================================
class LSB_Embed():
    def __init__(self):
        pass

    @staticmethod
    def get_bitPlane(img):
        """
        獲取彩色圖像的8個位平面
        :param img: 彩色圖像
        :return: 8個位平面的張量shape=(h, w, 8, c)
        """
        # w, h, c = img.shape
        h, w, c = img.shape
        bitPlane = np.zeros(shape=(h, w, 8, c))
        for c_id in range(c):
            flag = 0b00000001
            for bit_i in range(bitPlane.shape[-2]):
                bitplane = img[..., c_id] & flag  # 獲取圖像的某一位，從最後一位开始處理
                bitplane[bitplane != 0] = 1  # 阈值處理 非0即1
                bitPlane[..., bit_i, c_id] = bitplane  # 處理後的數據載入到某個位平面
                flag <<= 1  # 獲取下一個位的信息
        return bitPlane.astype(np.uint8)

    @staticmethod
    def lsb_embed(background, watermark, embed_bit=1):
        """
        在background的低三位進行嵌入浮水印，具體為將watermark的高三位信息替換掉background的低三位信息
        :param background: 背景圖像（彩色）
        :param watermark: 浮水印圖像（彩色）
        :return: 嵌入浮水印的圖像
        """
        # 1. 判断是否满足可嵌入的条件
        w_h, w_w,w_c = watermark.shape
        b_h,b_w, b_c = background.shape
        assert w_w < b_w and w_h < b_h, "請保證watermark尺寸小於background尺寸\r\n當前尺寸watermark:{}, background:{}".format(
            watermark.shape, background.shape)

        # 2. 獲取位平面
        bitPlane_background = lsb.get_bitPlane(
            background)  # 獲取的平面顺序是從低位到高位的 [（0 1 2 3 4 5 6 7）,（0 1 2 3 4 5 6 7）,（0 1 2 3 4 5 6 7）]
        bitPlane_watermark = lsb.get_bitPlane(watermark)

        # 3. 在位平面嵌入信息
        for c_i in range(b_c):
            for i in range(embed_bit):
                # 信息主要集中在高位，此處將watermark的高三位信息 放置在 background低三位信息中
                bitPlane_background[0:w_h, 0:w_w, i, c_i] = bitPlane_watermark[0:w_h, 0:w_w, (8 - embed_bit) + i, c_i]

        # 4. 得到watermark_img 浮水印嵌入圖像
        synthesis = np.zeros_like(background)
        for c_i in range(b_c):
            for i in range(8):
                synthesis[..., c_i] += bitPlane_background[..., i, c_i] * np.power(2, i)
        return synthesis.astype(np.uint8)

    @staticmethod
    def lsb_extract(synthesis, embed_bit=3):
        bitPlane_synthesis = lsb.get_bitPlane(synthesis)
        extract_watermark = np.zeros_like(synthesis)
        extract_background = np.zeros_like(synthesis)
        for c_i in range(3):
            for i in range(8):
                if i < embed_bit:
                    extract_watermark[..., c_i] += bitPlane_synthesis[..., i, c_i] * np.power(2, (8 - embed_bit) + i)
                else:
                    extract_background[..., c_i] += bitPlane_synthesis[..., i, c_i] * np.power(2, i)
        return extract_watermark.astype(np.uint8), extract_background.astype(np.uint8)


if __name__ == '__main__':
    while True:
        choice = input("請選擇功能：1.隱寫 2.攻擊 3.提取 4.退出 ：")
        if choice=='1':
            lsb = LSB_Embed()
            # 1. 獲取背景和浮水印
            background = cv2.imread('LSB/image/lena.bmp')
            watermark = cv2.imread('LSB/image/WaterMark.jpg')

            background = cv2.cvtColor(background, cv2.COLOR_BGR2RGB)
            watermark = cv2.cvtColor(watermark, cv2.COLOR_BGR2RGB)
            background_backup = background.copy()
            watermark_backup = watermark.copy()
            # 2. 進行浮水印嵌入
            embed_bit = 2
            synthesis = lsb.lsb_embed(background, watermark, embed_bit)
            # print(synthesis)
            cv2.imwrite('LSB/image/Marked.jpg', synthesis)
            print("已生成，位於LSB\image\Marked.jpg\n")
        elif choice=='2':
            Attack.main()
            print('攻擊並保存攻擊後的圖，位於LSB\image\Attack_result\n')
        elif choice=='3':
            # 3. 進行浮水印提取
            attacks = ['no_attack', 'gaussian_noise', 'salt_and_pepper_noise', 'mean_filter',
                       'median_filter', 'high_pass_filter', 'rotate_image']
            
            with open('LSB/result/Attack_Extract/ssim.txt', 'w') as file:
                file.write('Extract Results for LSB\n\n')
                for i in attacks:
                    synthesis_path = f'LSB/image/Attack_result/{i}.jpg'
                    synthesis = cv2.imread(synthesis_path)

                    # 保存攻擊後的圖像
                    extract_watermark, extract_background = lsb.lsb_extract(synthesis, embed_bit)
                    extract_watermark = extract_watermark[:260, :260, :]

                    # 保存攻擊後的圖像
                    attacked_image_filename = f'{i}.jpg'
                    attacked_image_path = os.path.join('LSB/image/Extract_watermark', attacked_image_filename)
                    cv2.imwrite(attacked_image_path, extract_watermark)

                    # 計算SSIM
                    ssim = SSIM(watermark, extract_watermark)
                    file.write(f'Attack Type: {i}\n')
                    file.write(f'SSIM: {ssim}\n\n')

            print('已儲存SSIM，位於LSB\image\Attack_result\ssim_results.txt\n')
        else:
            print("請查看資料夾! bye~")
            break