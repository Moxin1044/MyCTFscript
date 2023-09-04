import ffmpeg

# 设置RTMP服务器地址和串流密钥
rtmp_url = "rtmp://live-push.bilivideo.com/live-bvc/"
stream_key = "?streamname="

# 设置图片和音频文件路径
image_path = "output.jpg"

# 创建FFmpeg输入流
input_video = ffmpeg.input(image_path, loop=1, re=None, framerate=30)

# 创建FFmpeg输出流
output_stream = ffmpeg.output(input_video['v'], f"{rtmp_url}/{stream_key}", vcodec='libx264', acodec='aac', format='flv')
output_stream.run()
