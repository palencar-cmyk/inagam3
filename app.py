import streamlit as st
import streamlit.components.v1 as components
import os
import base64

# Configuração da página para o jogo ocupar o espaço correto
st.set_page_config(page_title="Ina Bros Game", layout="centered")

# Ocultar cabeçalhos e menus do Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div.block-container {padding-top: 2rem;}
    </style>
""", unsafe_allow_html=True)

# Função inteligente para converter as imagens locais do seu GitHub em formato legível pelo HTML
def get_image_base64(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded_string}"
    return ""

# Carregando as suas imagens direto da pasta do repositório
img_capa = get_image_base64("Capa.png")
img_cenario = get_image_base64("Cenário 1.png")

# --- CÓDIGO DO JOGO EM ESTILO MARIO BROS (PLATAFORMA) ---
game_html = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #222;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            font-family: 'Arial', sans-serif;
        }}
        #game-container {{
            width: 800px;
            height: 600px;
            background-color: #5c94fc; /* Azul céu padrão do Mario */
            position: relative;
            border: 4px solid #fff;
            overflow: hidden;
        }}
        .screen {{
            width: 100%;
            height: 100%;
            position: absolute;
            top: 0;
            left: 0;
            display: none;
            background-size: 100% 100%;
            background-repeat: no-repeat;
        }}
        .active {{
            display: block;
        }}
        
        /* Tela de Menu com a sua Capa.png */
        #menu-screen {{
            background-image: url('{img_capa}');
            background-color: #000;
        }}
        #start-btn {{
            position: absolute;
            bottom: 60px;
            left: 50%;
            transform: translateX(-50%);
            padding: 15px 40px;
            font-size: 22px;
            font-weight: bold;
            cursor: pointer;
            background-color: #e52521; /* Vermelho Mario */
            color: white;
            border: 3px solid #fff;
            border-radius: 8px;
            box-shadow: 0 5px 0 #a31411;
        }}
        #start-btn:active {{
            transform: translate(-50%, 4px);
            box-shadow: 0 1px 0 #a31411;
        }}

        /* Tela de Jogo com o seu Cenário 1.png */
        #game-screen {{
            background-image: url('{img_cenario}');
        }}

        /* Personagem (Estilo Bloco do Mario) */
        #player {{
            width: 40px;
            height: 60px;
            background-color: #e52521;
            border: 2px solid #000;
            position: absolute;
            bottom: 60px; /* Acima do chão */
            left: 100px;
            border-radius: 4px;
            transition: background 0.2s;
        }}

        /* Chão Falso do Jogo */
        #floor {{
            width: 100%;
            height: 60px;
            background-color: #73c740; /* Verde grama */
            border-top: 4px solid #4da22b;
            position: absolute;
            bottom: 0;
            left: 0;
        }}

        /* Plataforma para Pular */
        .platform {{
            width: 150px;
            height: 30px;
            background-color: #fcb443; /* Bloco de tijolo amarelo */
            border: 3px solid #6b4000;
            position: absolute;
            bottom: 220px;
            left: 350px;
            text-align: center;
            line-height: 30px;
            font-weight: bold;
            color: #6b4000;
        }}

        /* Botões de controle na tela */
        .controls-container {{
            position: absolute;
            top: 20px;
            left: 20px;
            display: flex;
            gap: 15px;
            background: rgba(0, 0, 0, 0.6);
            padding: 10px;
            border-radius: 8px;
        }}
        .control-btn {{
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            background: #fff;
            border: 2px solid #000;
            cursor: pointer;
            border-radius: 5px;
        }}
        .control-btn:active {{
            background: #ddd;
        }}
    </style>
</head>
<body>

    <div id="game-container">
        <div id="menu-screen" class="screen active">
            <button id="start-btn" onclick="startGame()">JOGAR</button>
        </div>

        <div id="game-screen" class="screen">
            <div class="controls-container">
                <button class="control-btn" onclick="movePlayer(-30)">⬅️ CORRER ESQ</button>
                <button class="control-btn" onclick="jumpPlayer()">⬆️ PULAR</button>
                <button class="control-btn" onclick="movePlayer(30)">CORRER DIR ➡️</button>
            </div>

            <div id="player"></div>
            <div class="platform">BLOCO</div>
            <div id="floor"></div>
        </div>
    </div>

    <script>
        let playerX = 100;
        let playerY = 60; // Altura em relação à base do container (sobre o chão)
        let isJumping = false;
        const player = document.getElementById('player');

        function startGame() {{
            document.getElementById('menu-screen').classList.remove('active');
            document.getElementById('game-screen').classList.add('active');
        }}

        function movePlayer(offset) {{
            playerX += offset;
            // Impede o boneco de sair das bordas da tela
            if (playerX < 0) playerX = 0;
            if (playerX > 760) playerX = 760;
            player.style.left = playerX + 'px';
            
            // Checagem simples se caiu ou subiu na plataforma
            checkPlatform();
        }}

        function jumpPlayer() {{
            if (isJumping) return;
            isJumping = true;
            
            let baseFloor = playerY; 
            let targetHeight = baseFloor + 160;

            // Subida do pulo
            let upInterval = setInterval(() => {{
                playerY += 8;
                player.style.bottom = playerY + 'px';
                
                if (playerY >= targetHeight) {{
                    clearInterval(upInterval);
                    
                    // Queda da gravidade
                    let downInterval = setInterval(() => {{
                        playerY -= 8;
                        player.style.bottom = playerY + 'px';
                        
                        // Checa pouso no Bloco do meio do caminho
                        if (playerX >= 310 && playerX <= 480 && playerY <= 250 && playerY >= 240) {{
                            clearInterval(downInterval);
                            playerY = 250; // Fica em cima do bloco
                            player.style.bottom = playerY + 'px';
                            isJumping = false;
                        }}
                        // Se voltar pro chão normal
                        else if (playerY <= 60) {{
                            clearInterval(downInterval);
                            playerY = 60;
                            player.style.bottom = playerY + 'px';
                            isJumping = false;
                        }}
                    }}, 15);
                }}
            }}, 15);
        }}

        function checkPlatform() {{
            // Se o boneco andar para fora do Bloco Amarelo, ele cai de volta pro chão
            if (playerY === 250 && (playerX < 310 || playerX > 480)) {{
                let fallInterval = setInterval(() => {{
                    playerY -= 8;
                    player.style.bottom = playerY + 'px';
                    if (playerY <= 60) {{
                        clearInterval(fallInterval);
                        playerY = 60;
                        player.style.bottom = playerY + 'px';
                    }}
                }}, 15);
            }}
        }}
    </script>
</body>
</html>
"""

# Inicializa o componente de exibição do jogo
components.html(game_html, width=800, height=600)
