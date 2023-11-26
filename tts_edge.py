import edge_tts
import asyncio
import playsound
import concurrent.futures
# with open ('1.txt','rb') as f:
#     data = f.read()
#     TEXT = data.decode('utf-8')
#     print(TEXT)
voice = 'zh-CN-XiaoxiaoNeural'
rate = '-4%'
volume = '+0%'

async def tts_response_async(text, file_path, voice):
    response = edge_tts.Communicate(text = text,voice = voice,rate = rate,volume=volume)
    await response.save(file_path)
    playsound.playsound(file_path)
    
def tts_response(text, file_path="./speech/speech.mp3", voice = voice):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(asyncio.run, tts_response_async(text, file_path, voice))
        future.result()


if __name__ == "__main__":
    voice_list = [
    'zh-CN-XiaoyiNeural',
    'zh-CN-XiaoxiaoNeural',
    'zh-TW-HsiaoChenNeural',
    'zh-TW-HsiaoChenNeural',
    'zh-CN-liaoning-XiaobeiNeural',
    ]
    _ = 0
    while True:
        TEXT = f'测试声音{_%5}号'
        tts_response(TEXT, voice = voice_list[_%5])
        _ += 1