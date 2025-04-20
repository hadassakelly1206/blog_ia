import requests
import os
from dotenv import load_dotenv
from conteudo.gerador_conteudo import gerar_imagem


load_dotenv()

WP_URL = os.getenv("WP_URL")
WP_USER = os.getenv("WP_USER")
WP_PASS = os.getenv("WP_PASS")

def gerar_token():
    url = f"{WP_URL}/wp-json/jwt-auth/v1/token"
    payload = {
        "username": WP_USER,
        "password": WP_PASS
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        token = response.json()["token"]
        print("✅ Token JWT gerado com sucesso.")
        return token
    else:
        print("❌ Erro ao gerar token:", response.text)
        return None

def enviar_imagem_para_wordpress(caminho_imagem, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Disposition": f"attachment; filename=imagem_post.png",
        "Content-Type": "image/png"
    }

    url = f"{WP_URL}/wp-json/wp/v2/media"

    with open(caminho_imagem, "rb") as img:
        response = requests.post(url, headers=headers, data=img)

    if response.status_code == 201:
        media_id = response.json()["id"]
        print("✅ Imagem enviada com sucesso.")
        return media_id
    else:
        print("❌ Erro ao enviar imagem:", response.text)
        return None


def publicar_post(titulo, conteudo, categorias=[], tags=[], imagem_id=None):
    token = gerar_token()
    if not token:
        return

    caminho_imagem = gerar_imagem(titulo)
    imagem_id = enviar_imagem_para_wordpress(caminho_imagem, token)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    post_data = {
        "title": titulo,
        "content": conteudo,
        "status": "publish",
        "categories": categorias,
        "tags": tags,
        "featured_media": imagem_id
    }

    url = f"{WP_URL}/wp-json/wp/v2/posts"
    response = requests.post(url, json=post_data, headers=headers)

    if response.status_code == 201:
        print("✅ Post publicado com sucesso!")
    else:
        print("❌ Erro ao publicar post:", response.text)

    # 🧹 Limpar imagem local depois de publicar
    try:
        os.remove(caminho_imagem)
        print(f"🧼 Imagem local '{caminho_imagem}' removida.")
    except Exception as e:
        print(f"⚠️ Erro ao tentar remover a imagem local: {e}")

def obter_ids_tags(tags):
    url = f"{WP_URL}/wp-json/wp/v2/tags?search="
    ids = []

    for tag in tags:
        response = requests.get(url + tag)
        if response.status_code == 200:
            tags_data = response.json()
            if tags_data:
                ids.append(tags_data[0]["id"])
            else:
                print(f"⚠️ Tag '{tag}' não encontrada no WordPress.")
        else:
            print(f"❌ Erro ao buscar tag '{tag}': {response.text}")

    return ids
