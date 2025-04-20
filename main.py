import schedule
import time
from noticias.gnews_api import buscar_noticias
from wordpress.wordpress_api import publicar_post, obter_ids_tags
from conteudo.gerador_conteudo import gerar_conteudo_blog, gerar_titulo

def automatizar_postagem():
    noticias = buscar_noticias(limit=5)

    if not noticias:
        print("⚠️ Nenhuma notícia encontrada.")
        return

    conteudo = gerar_conteudo_blog(noticias)
    titulo = gerar_titulo(conteudo)

    categorias = [1]  
    nomes_tags = ["inteligência artificial", "tecnologia", "notícias"]
    tags_ids = obter_ids_tags(nomes_tags)

    publicar_post(titulo, conteudo, categorias, tags_ids)


if __name__ == "__main__":
    automatizar_postagem()
