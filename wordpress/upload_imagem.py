import requests
import os

def enviar_imagem_para_wordpress(caminho_imagem, token):
    if not caminho_imagem or not os.path.exists(caminho_imagem):
        print("⚠️ Caminho de imagem inválido.")
        return None

    nome_arquivo = os.path.basename(caminho_imagem)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Disposition": f"attachment; filename={nome_arquivo}",
        "Content-Type": "image/png"
    }

    with open(caminho_imagem, "rb") as img:
        url = os.getenv("WP_URL") + "/wp-json/wp/v2/media"
        response = requests.post(url, headers=headers, data=img)

    if response.status_code == 201:
        imagem_id = response.json().get("id")
        print(f"✅ Imagem enviada com sucesso. ID: {imagem_id}")
        return imagem_id
    else:
        print(f"❌ Erro ao enviar imagem: {response.status_code} - {response.text}")
        return None