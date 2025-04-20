import requests
import json
import os
from PIL import Image
from io import BytesIO
import openai
from dotenv import load_dotenv
import datetime
import re



# Carregar variáveis do ambiente
load_dotenv()

# Carregar o token do WordPress do arquivo .env
WORDPRESS_URL = "https://rafaelaltomare.com.br/wp-json/wp/v2/posts"  # Substitua com a URL do seu WordPress


# Função para gerar conteúdo utilizando a API do OpenAI
def gerar_conteudo_blog(noticias):
    import openai

    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Cria um texto com base nas notícias
    noticias_formatadas = "\n".join([f"Título: {n['titulo']}\nDescrição: {n['descricao']}\nLink: {n['url']}" for n in noticias])

    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-4",  # ou gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "Você é um redator de blog especializado em tecnologia."},
                {"role": "user", "content": f"Escreva um artigo de blog em português-br baseado na melhor notícia que você achar ser a mais importante e atual:\n\n{noticias_formatadas}"}
            ],
            max_tokens=1200,
            temperature=0.7
        )

        return resposta.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ Erro ao gerar conteúdo: {e}")
        return "Erro ao gerar conteúdo."


def gerar_titulo(conteudo_gerado):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um redator especializado em títulos de blog em português. Crie títulos curtos, atrativos, em português e que resumam bem o conteúdo."
                },
                {
                    "role": "user",
                    "content": (
                        "Com base no texto abaixo, escreva um título breve, atrativo e em português. "
                        "Evite títulos longos, e foque na ideia principal do conteúdo:\n\n"
                        f"{conteudo_gerado}"
                    )
                }
            ],
            max_tokens=60,
            temperature=0.7
        )

        titulo_bruto = resposta.choices[0].message.content.strip()
        # Remove aspas simples e duplas do início e fim, se existirem
        titulo_limpo = titulo_bruto.strip('"').strip("'")
        return titulo_limpo

    except Exception as e:
        print(f"❌ Erro ao gerar título: {e}")
        return "Notícias sobre Inteligência Artificial – Semana"



def gerar_imagem(titulo_post):
    import openai
    import base64

    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = f"Imagem moderna e minimalista em preto e branco que represente: {titulo_post}"

    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format="b64_json"
    )

    imagem_b64 = response["data"][0]["b64_json"]

    # Criar nome do arquivo a partir do título
    slug = re.sub(r'\W+', '-', titulo_post.lower())[:50]
    data = datetime.datetime.now().strftime("%Y%m%d%H%M")
    nome_arquivo = f"imagem_{slug}_{data}.png"

    with open(nome_arquivo, "wb") as f:
        f.write(base64.b64decode(imagem_b64))

    print("✅ Imagem gerada com sucesso.")
    return nome_arquivo
