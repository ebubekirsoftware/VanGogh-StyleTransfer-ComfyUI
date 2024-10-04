import argparse
import websocket  # NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
import requests
import random
from PIL import Image
import io
import os


# Argparse ile komut satırından parametreleri al
def parse_arguments():
    parser = argparse.ArgumentParser(description='ComfyUI Workflow Script')
    parser.add_argument('--image_path', type=str, required=True, help='Path to the input image.')
    parser.add_argument('--checkpoint_path', type=str, required=True, help='Path to the model checkpoint file.')
    parser.add_argument('--controlnet_path', type=str, required=True, help='Path to the controlnet model file.')
    parser.add_argument('--json_path', type=str, required=True, help='Path to the workflow JSON file.')

    return parser.parse_args()


# Sunucu adresi ve client ID
server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())


# Prompt kuyruğuna ekle
def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"http://{server_address}/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())


# Görüntüyü getir
def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(f"http://{server_address}/view?{url_values}") as response:
        return response.read()


# Geçmişi getir
def get_history(prompt_id):
    with urllib.request.urlopen(f"http://{server_address}/history/{prompt_id}") as response:
        return json.loads(response.read())


# Görüntüleri al
def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    vae_decode_node_id = None  # VAE Decode node id'yi kaydetmek için

    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    # İşlem tamamlandı, break
                    break
            elif message['type'] == 'output' and message['node'] == '8':  # '8' node, VAE Decode
                vae_decode_node_id = '8'  # Son aşamayı VAE Decode olarak işaretle
        else:
            continue  # previews are binary data

    # İşlem bittikten sonra history'den VAE Decode node'unu kontrol et
    if vae_decode_node_id:
        history = get_history(prompt_id)[prompt_id]
        if vae_decode_node_id in history['outputs']:
            node_output = history['outputs'][vae_decode_node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
                output_images[vae_decode_node_id] = images_output

    return output_images


# Dosya yükle
def upload_file(file, subfolder="", overwrite=False):
    try:
        body = {"image": file}
        data = {}

        if overwrite:
            data["overwrite"] = "true"

        if subfolder:
            data["subfolder"] = subfolder

        resp = requests.post(f"http://{server_address}/upload/image", files=body, data=data)

        if resp.status_code == 200:
            data = resp.json()
            path = data["name"]
            if "subfolder" in data and data["subfolder"] != "":
                path = data["subfolder"] + "/" + path

        else:
            print(f"{resp.status_code} - {resp.reason}")
    except Exception as error:
        print(error)
    return path


# Ana fonksiyon
def main():
    args = parse_arguments()

    # Resmi yükle
    with open(args.image_path, "rb") as f:
        comfyui_path_image = upload_file(f, "", True)

    # JSON dosyasını yükle
    with open(args.json_path, "r", encoding="utf-8") as f:
        workflow_data = f.read()

    workflow = json.loads(workflow_data)

    # Pozitif CLIPTextEncode için metin promptlarını ayarla
    workflow["6"]["inputs"][
        "text"] = "A painting in the style of Vincent van Gogh, with vivid brushstrokes, vivid colors, swirling patterns, bold colors, and heavy use of contrast. Thick paint application with dynamic composition and emotional depth."
    workflow["7"]["inputs"][
        "text"] = "blurry, low detail, cartoonish, 3D render, digital art, abstract, soft colors, pale colors, smooth textures, sharp edges, pixelated, deformed, distorted."

    # Rastgele tohum oluştur
    seed = random.randint(1, 1000000000)
    workflow["3"]["inputs"]["seed"] = seed

    # Yüklenen resmi iş akışına yerleştir (KSampler için)
    workflow["13"]["inputs"]["image"] = comfyui_path_image

    # Model kontrol noktalarını ayarla
    workflow["4"]["inputs"]["ckpt_name"] = args.checkpoint_path

    # ControlNet modelini ayarla
    workflow["31"]["inputs"]["control_net_name"] = args.controlnet_path

    # WebSocket bağlantısı kur ve görüntüleri al
    ws = websocket.WebSocket()
    ws.connect(f"ws://{server_address}/ws?clientId={client_id}")
    images = get_images(ws, workflow)

    # Çıktı klasörü yoksa oluştur
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Sadece son görüntüyü kaydet (VAE Decode'den gelen)
    for node_id in images:
        for image_data in images[node_id]:
            image = Image.open(io.BytesIO(image_data))
            output_path = os.path.join(output_folder, f"{node_id}-{seed}.png")
            image.save(output_path)
            print(f"Image saved to: {output_path}")


if __name__ == "__main__":
    main()
