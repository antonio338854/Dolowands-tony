import streamlit as st
import yt_dlp
import os
import time

# Configuração da Página
st.set_page_config(page_title="Tony Downloads", page_icon="🎬", layout="centered")

# Estilo Cirúrgico
st.markdown("""
    <style>
    .stButton>button {
        background-color: #FF0000;
        color: white;
        font-size: 20px;
        border-radius: 10px;
        width: 100%;
    }
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #FFF;
    }
    .footer {
        text-align: center;
        font-size: 14px;
        margin-top: 50px;
        color: #888;
    }
    </style>
    """, unsafe_allow_html=True)

# Título e Créditos
st.markdown('<div class="title">TONY DOWNLOADS 🎬</div>', unsafe_allow_html=True)
st.write("### Baixe vídeos em qualidade MÁXIMA (YouTube, TikTok, Insta...)")

# Entrada de Dados
url = st.text_input("Cole o Link do Vídeo aqui:")
quality = st.selectbox("Selecione a Qualidade:", ["Melhor Possível (Até 4K)", "1080p (Full HD)", "720p (HD)", "Áudio MP3 (Apenas Som)"])

# Função de Download Cirúrgica
def download_video(url, quality_setting):
    
    # Definição de Formatos para o yt-dlp
    if quality_setting == "Melhor Possível (Até 4K)":
        format_str = 'bestvideo+bestaudio/best' # Tenta juntar o melhor vídeo com o melhor áudio
    elif quality_setting == "1080p (Full HD)":
        format_str = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
    elif quality_setting == "720p (HD)":
        format_str = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
    else: # MP3
        format_str = 'bestaudio/best'

    # Nome do arquivo de saída temporário
    output_template = '%(title)s.%(ext)s'

    ydl_opts = {
        'format': format_str,
        'outtmpl': output_template,
        'noplaylist': True,
        'quiet': True,
        # IMPORTANTE: Isso funde áudio e vídeo para o 4K funcionar
        'merge_output_format': 'mp4', 
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }] if quality_setting != "Áudio MP3 (Apenas Som)" else [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with st.spinner(f'O Tony está processando o vídeo em {quality_setting}... Aguarde, a mágica demora um pouco no 4K.'):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                # Ajuste de extensão para MP3 ou Vídeo Mesclado
                if quality_setting == "Áudio MP3 (Apenas Som)":
                    final_filename = filename.rsplit('.', 1)[0] + '.mp3'
                else:
                    # Se for vídeo, o yt-dlp pode ter salvo como mkv antes de converter, ou mp4
                    # Vamos garantir que pegamos o arquivo que foi gerado
                    final_filename = filename.rsplit('.', 1)[0] + '.mp4'
                    if not os.path.exists(final_filename):
                        final_filename = filename # Fallback

                return final_filename, info.get('title', 'video')
    except Exception as e:
        st.error(f"Erro no download: {e}")
        return None, None

# Botão de Ação
if st.button("BAIXAR AGORA"):
    if url:
        file_path, title = download_video(url, quality)
        
        if file_path and os.path.exists(file_path):
            # Ler o arquivo para disponibilizar o download
            with open(file_path, "rb") as file:
                file_bytes = file.read()
            
            st.success("Download Concluído pelo Sistema Tony!")
            
            st.download_button(
                label=f"📥 Clique para Salvar: {title}",
                data=file_bytes,
                file_name=os.path.basename(file_path),
                mime="video/mp4" if "mp3" not in file_path else "audio/mpeg"
            )
            
            # Limpeza cirúrgica (apaga o arquivo do servidor para não encher)
            os.remove(file_path)
    else:
        st.warning("Cole um link primeiro, chefia!")

st.markdown('<div class="footer">Desenvolvido com precisão cirúrgica | Créditos ao Tony</div>', unsafe_allow_html=True)
