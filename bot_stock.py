import discord
from discord.ext import tasks
import requests

TOKEN = 'MTQ3Njc5ODI1NTg0ODM2MjA3OA.GC14wf.vaIIoAykJNVZ50e6qFoUgtyw1dRmJnSHYG5rEs'
CHANNEL_ID = 1234567890 # Thay bằng ID kênh của bạn
API_URL = 'https://gagapi.onrender.com/seeds'

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@tasks.loop(minutes=5)
async def task_check_stock():
    channel = client.get_channel(CHANNEL_ID)
    if not channel: return
    try:
        # Gọi API
        r = requests.get(API_URL)
        if r.status_code == 200:
            data = r.json()
            
            # Kiểm tra xem data có phải là danh sách không
            if not data or len(data) == 0:
                print("API trả về danh sách trống.")
                return # Nếu trống thật thì không nhắn tin để tránh spam

            embed = discord.Embed(
                title="🌱 GARDEN HORIZON STOCK UPDATE", 
                description="Danh sách hạt giống mới nhất:",
                color=0x2ecc71
            )
            
            msg = ""
            for item in data:
                # Chỉnh sửa 'name' và 'price' theo đúng tên cột trong API của bạn
                name = item.get('name') or item.get('seed_name') or "Vật phẩm"
                price = item.get('price') or item.get('cost') or "Liên hệ"
                msg += f"✅ **{name}**: `{price}` 💰\n"
            
            embed.description = msg
            await channel.send(embed=embed)
        else:
            print(f"Lỗi kết nối API: {r.status_code}")
    except Exception as e:
        print(f"Lỗi hệ thống: {e}")

@client.event
async def on_ready():
    print(f'Bot {client.user} đã sẵn sàng!')
    task_check_stock.start()

client.run(TOKEN)
