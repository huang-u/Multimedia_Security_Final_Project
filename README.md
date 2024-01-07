# Multimedia_Security_Final_Project
## LSB
使用最低有效位（LSB）在數字數據的二進制表示中嵌入額外的信息，這樣的技術可以用來隱藏訊息，而不引起人眼或人耳的感知變化。<br>
直接跑main.py即可
<p>
請選擇功能：<br>
1.隱寫<br>
將watermark的高三位信息替換掉background的低三位信息<br>
<img src='Multimedia_Security/LSB/image/Marked.jpg' width='200'> <img src='Multimedia_Security/LSB/image/WaterMark.jpg' width='200'><br>
  
2.攻擊<br>
attacks = ['no_attack', 'gaussian_noise', 'salt_and_pepper_noise', 'mean_filter', 'median_filter', 'high_pass_filter', 'rotate_image']<br>
利用以上攻擊方法，攻擊"image\Marked.jpg"，<br>
並產生統計圖("result\Marked_Attack\all_results.jpg")及數據("result\Marked_Attack\attack_results.txt")及攻擊後的個別圖片("image\Attack_result\\{attacks_name}.png")<br>
<!--![all_results](https://github.com/huang-u/Multimedia_Security_Final_Project/assets/81971590/2482891b-c2cb-4dda-b2c4-550e478a38f7)>-->
<img src='Multimedia_Security/LSB/result/Marked_Attack/all_attack_results.jpg' width=70%><br>

Attack Results for LSB<br>

Attack Type: no_attack<br>
PSNR: inf, SSIM: 1.00<br><br>

Attack Type: gaussian_noise<br>
PSNR: 20.228239685521036, SSIM: 0.29<br><br>

Attack Type: salt_and_pepper_noise<br>
PSNR: 19.4810084430014, SSIM: 0.39<br><br>

Attack Type: mean_filter<br>
PSNR: 35.64094299879962, SSIM: 0.95<br><br>

Attack Type: median_filter<br>
PSNR: 37.77993611415274, SSIM: 0.96<br><br>

Attack Type: high_pass_filter<br>
PSNR: 6.456283796642342, SSIM: 0.12<br><br>

Attack Type: rotate_image<br>
PSNR: 10.574410910655256, SSIM: 0.28<br><br>

3.提取<br>
從被攻擊的圖中取出浮水印，並對其計算SSIM。("result\Attack_Extract\ssim.txt")<br>

Extract Results for LSB<br>

Attack Type: no_attack<br>
SSIM: 0.015352597439659377<br><br>

Attack Type: gaussian_noise<br>
SSIM: 0.008494161093138454<br><br>

Attack Type: salt_and_pepper_noise<br>
SSIM: 0.0071360329227082705<br><br>

Attack Type: mean_filter<br>
SSIM: 0.006409435783714635<br><br>

Attack Type: median_filter<br>
SSIM: 0.011256819544516978<br><br>

Attack Type: high_pass_filter<br>
SSIM: 0.010998056046992786<br><br>

Attack Type: rotate_image<br>
SSIM: 0.0039900751036624086<br><br>

4.退出<br>
結束應用<br>
![image](https://github.com/huang-u/Multimedia_Security_Final_Project/assets/81971590/aa5948d4-4ee3-44c3-981c-e2b0b09bb790)

</p>

## Shift-Histogram
使用直方圖的位移中嵌入額外的信息，這樣的技術可以用來隱藏訊息，而不引起人眼或人耳的感知變化。<br>
直接跑Reversible_Data_Hiding.py即可
<p>

請選擇功能：<br>
1.隱寫<br>
使用Key(random)加密明文("image\lena.bmp")，生成密文("image\Marked_Image.png")<br>
<!--![all_image_results](https://github.com/huang-u/Multimedia_Security_Final_Project/assets/81971590/3ed5e015-516f-4a44-a21b-b7c2f9cf9b81)-->
<img src='Multimedia_Security/LSB/image/Marked.jpg' width='200'><br>

2.攻擊<br>
attacks = ['no_attack', 'gaussian_noise', 'salt_and_pepper_noise', 'mean_filter', 'median_filter', 'high_pass_filter', 'rotate_image']<br>
利用以上攻擊方法，攻擊"image\Marked.png"，<br>
並產生統計圖("result\Marked_Attack\all_attack_results.png")及數據("result\Marked_Attack\attack_results.txt")及攻擊後的個別圖片("image\Attack_result\\{attacks_name}.jpg")<br>
<!--![all_attack_results](https://github.com/huang-u/Multimedia_Security_Final_Project/assets/81971590/cd3156cf-ee6b-4eac-b1f2-76a928fcf2cf)-->
<img src='Multimedia_Security/Shift-Histogram/result/Marked_Attack/all_attack_results.png' width=70%><br>

3.提取<br>
從被攻擊的圖中取出浮水印，並對其計算BER。("result\Attack_Extract\ber.txt")<br>
<!--![secret](https://github.com/huang-u/Multimedia_Security_Final_Project/assets/81971590/013fa2d2-83ea-445c-bbbb-b77076fe0b59)-->

4.退出<br>
結束應用<br>
![image](https://github.com/huang-u/Multimedia_Security_Final_Project/assets/81971590/e394e658-287a-4df6-8daf-0aa790ba7c28)

</p>
