from PIL import Image

import os, ffmpeg


# Compress input.mp4 to 50MB and save as output.mp4


class Main:
    def __init__(self):
        self.imagesPath = 'D:\\programming\\ABC_my_python_files\\files 4\\WINDOWS\\mediaCompressor\\myPHotosTest'
        self.saveIn = 'D:\\programming\\ABC_my_python_files\\files 4\\WINDOWS\\mediaCompressor\\compressed'
    def compressorEngine(self,image):
        # Open the image
        directory, filename = os.path.split(image)
        input_image = Image.open(image)

        print(input_image)
        # Define the compression quality (1-95, 95 being the best)
        compression_quality = 20

        # Save the compressed image
        input_image.save(f"{filename}", quality=compression_quality)
        print(filename)

        # Close the image file
        input_image.close()

    def compress_video(self,video_full_path, output_file_name, target_size):
    # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
        min_audio_bitrate = 32000
        max_audio_bitrate = 256000

        probe = ffmpeg.probe('D:\\programming\\ABC_my_python_files\\files 4\\WINDOWS\\mediaCompressor\\compressed\\VID_20230819_153215.mp4')
        # Video duration, in s.
        duration = float(probe['format']['duration'])
        # Audio bitrate, in bps.
        audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
        # Target total bitrate, in bps.
        target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

        # Target audio bitrate, in bps
        if 10 * audio_bitrate > target_total_bitrate:
            audio_bitrate = target_total_bitrate / 10
            if audio_bitrate < min_audio_bitrate < target_total_bitrate:
                audio_bitrate = min_audio_bitrate
            elif audio_bitrate > max_audio_bitrate:
                audio_bitrate = max_audio_bitrate
        # Target video bitrate, in bps.
        video_bitrate = target_total_bitrate - audio_bitrate

        i = ffmpeg.input(video_full_path)
        ffmpeg.output(i, os.devnull,
                    **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                    ).overwrite_output().run()
        ffmpeg.output(i, output_file_name,
                    **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                    ).overwrite_output().run()

    def main(self):
        os.chdir(self.saveIn)
        # error in compress video
        self.compress_video('C:\\Users\\RAMEZ MALAK\\Desktop\\VID_20230819_153215.mp4', 'output.mp4', 50 * 1000)
    
      
        # file_names = os.listdir(self.imagesPath)

        # for file_name in file_names:
        #     print(file_name)

        #     self.compressorEngine(f"{self.imagesPath}\\{file_name}")


if __name__ == "__main__":
    variable = Main()

    variable.main()

