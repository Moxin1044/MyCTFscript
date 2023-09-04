import ffmpeg

# 设置RTMP服务器地址和串流密钥
rtmp_url = "rtmp://live-push.bilivideo.com/live-bvc/"
stream_key = "?streamname="

# 设置输入流
input_stream = ffmpeg.input("output.mp4")

# 创建输出流
output_stream = ffmpeg.output(input_stream, f"{rtmp_url}/{stream_key}", vcodec='libx264', acodec='aac', format='flv')
output_stream.run()
