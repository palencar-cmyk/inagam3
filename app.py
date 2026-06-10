import streamlit as st
import streamlit.components.v1 as components
import os
import base64
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Ina Game", layout="centered")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div.block-container {padding-top: 1rem;}
    body {background-color: #0a0a0a;}
    </style>
""", unsafe_allow_html=True)

def carregar_imagem_base64(nome_arquivo):
    if os.path.exists(nome_arquivo):
        try:
            img = Image.open(nome_arquivo)
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            return "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode()
        except Exception:
            return ""
    return ""

# Carregamento de todos os assets solicitados
img_capa = carregar_imagem_base64("Capa.png")
img_cena1 = carregar_imagem_base64("Cenário 1.png")
img_cena2 = carregar_imagem_base64("Cenário 2.png")
img_inara = carregar_imagem_base64("inara.png")
img_queen = carregar_imagem_base64("queenofbones.png")
img_faca = carregar_imagem_base64("knife.jpg")
img_folha = carregar_imagem_base64("weed.jpg")
img_esqueleto = carregar_imagem_base64("skeleton.jpg")

game_html = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Creepster&family=MedievalSharp&display=swap" rel="stylesheet">
    <style>
        body {{ margin: 0; padding: 0; background-color: #0a0a0a; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; user-select: none; }}
        #game-window {{ width: 800px; height: 600px; position: relative; border: 4px solid #4a0000; border-radius: 10px; box-shadow: 0 0 40px rgba(139, 0, 0, 0.6); overflow: hidden; background-color: #000; }}
        .screen {{ width: 100%; height: 100%; position: absolute; top: 0; left: 0; display: none; }}
        .active {{ display: block; }}
        
        #menu-screen {{ background-image: url('{img_capa}'); background-size: cover; background-position: center; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
        .menu-box {{ background: rgba(0, 0, 0, 0.85); padding: 40px 60px; border: 2px solid #8b0000; border-radius: 10px; text-align: center; box-shadow: 0 0 30px #000; }}
        h1 {{ font-family: 'Creepster', cursive; font-size: 70px; color: #ff1a1a; text-shadow: 3px 3px 0 #000, 0 0 20px #ff0000; margin: 0 0 30px 0; letter-spacing: 5px; }}
        .btn-start {{ font-family: 'MedievalSharp', cursive; font-size: 28px; padding: 15px 40px; background: #4a0000; color: #fff; border: 2px solid #ff1a1a; cursor: pointer; border-radius: 5px; transition: 0.3s; box-shadow: 0 0 15px rgba(255,0,0,0.5); }}
        .btn-start:hover {{ background: #8b0000; transform: scale(1.05); }}

        #game-screen {{ background-image: url('{img_cena1}'); background-size: cover; background-position: center; transition: background-image 1s ease-in-out; }}
        #floor {{ position: absolute; bottom: 0; width: 100%; height: 60px; background: rgba(0, 0, 0, 0.6); border-top: 2px solid #333; }}
        
        #ui-layer {{ position: absolute; top: 20px; left: 20px; z-index: 100; font-family: 'MedievalSharp', cursive; font-size: 24px; color: #fff; text-shadow: 2px 2px 4px #000; }}
        #hearts-container {{ display: flex; gap: 5px; margin-bottom: 10px; font-size: 30px; }}
        #score-display {{ color: #ff1a1a; font-weight: bold; }}
        #stage-banner {{ position: absolute; top: 150px; width: 100%; text-align: center; font-family: 'Creepster', cursive; font-size: 40px; color: #ff00ff; text-shadow: 2px 2px 0 #000; display: none; z-index: 100; }}
        
        /* Personagens e Inimigos */
        #player-inara {{ width: 70px; height: 110px; background-image: url('{img_inara}'); background-size: contain; background-repeat: no-repeat; background-position: bottom; position: absolute; bottom: 60px; z-index: 21; transition: filter 0.2s; }}
        #player-queen {{ width: 70px; height: 110px; background-image: url('{img_queen}'); background-size: contain; background-repeat: no-repeat; background-position: bottom; position: absolute; bottom: 60px; z-index: 20; display: none; transition: filter 0.2s; }}
        
        .skeleton {{ width: 65px; height: 95px; background-image: url('{img_esqueleto}'); background-size: contain; background-repeat: no-repeat; background-position: bottom; position: absolute; bottom: 60px; z-index: 15; }}
        
        /* Projéteis */
        .knife {{ width: 40px; height: 15px; background-image: url('{img_faca}'); background-size: cover; position: absolute; z-index: 25; border-radius: 2px; box-shadow: 0 0 5px #fff; }}
        .leaf {{ width: 30px; height: 30px; background-image: url('{img_folha}'); background-size: cover; position: absolute; z-index: 25; border-radius: 50%; box-shadow: 0 0 8px #0f0; }}
        
        /* Botão de ataque na tela */
        #action-btn-container {{ position: absolute; bottom: 20px; right: 20px; z-index: 100; }}
        #attack-btn {{ font-family: 'MedievalSharp', cursive; font-size: 22px; padding: 15px 30px; background: linear-gradient(135deg, #4a0000, #1a0000); color: #fff; border: 2px solid #ff1a1a; border-radius: 50px; cursor: pointer; box-shadow: 0 0 15px rgba(255,0,0,0.8); user-select: none; transition: transform 0.1s; }}
        #attack-btn:active {{ transform: scale(0.9); }}

        #game-over {{ display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 200; flex-direction: column; align-items: center; justify-content: center; }}
    </style>
</head>
<body>
    <div id="game-window">
        <div id="menu-screen" class="screen active">
            <div class="menu-box">
                <h1>INA GAME</h1>
                <button class="btn-start" onclick="initGame()">INICIAR DUELO</button>
            </div>
        </div>

        <div id="game-screen" class="screen">
            <div id="ui-layer">
                <div id="hearts-container"></div>
                <div id="score-display">Esqueletos Derrotados: <span id="score">0</span></div>
            </div>
            
            <div id="stage-banner">QUEEN OF BONES SE JUNTA À BATALHA!</div>
            
            <div id="player-queen"></div>
            <div id="player-inara"></div>
            
            <div id="action-btn-container">
                <button id="attack-btn" onmousedown="throwWeapons()" ontouchstart="throwWeapons()">⚔️ GOLPEAR</button>
            </div>
            
            <div id="floor"></div>
            <div id="game-over">
                <h1>FIM DE JOGO</h1>
                <button class="btn-start" onclick="location.reload()">TENTAR NOVAMENTE</button>
            </div>
        </div>
    </div>

    <script>
        // --- SISTEMA DE ÁUDIO ---
        const actx = new (window.AudioContext || window.webkitAudioContext)();
        let bgmInterval;

        function playTone(freq, type, duration, vol) {{
            if(actx.state === 'suspended') actx.resume();
            const osc = actx.createOscillator();
            const gain = actx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, actx.currentTime);
            gain.gain.setValueAtTime(vol, actx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, actx.currentTime + duration);
            osc.connect(gain);
            gain.connect(actx.destination);
            osc.start();
            osc.stop(actx.currentTime + duration);
        }}

        function playThrowSound() {{ playTone(600, 'square', 0.1, 0.1); }}
        function playHitSound() {{ playTone(150, 'sawtooth', 0.2, 0.2); }}
        function playDamageSound() {{ playTone(100, 'square', 0.4, 0.3); playTone(80, 'sawtooth', 0.5, 0.3); }}
        
        function startBGM() {{
            const notes = [220, 246, 261, 293, 329, 261, 293, 220];
            let step = 0;
            bgmInterval = setInterval(() => {{
                playTone(notes[step], 'triangle', 0.3, 0.05);
                step = (step + 1) % notes.length;
            }}, 400);
        }}

        // --- LÓGICA DO JOGO ---
        let stage = 1;
        let pX = 150, pY = 60, pVelocityY = 0, isJumping = false;
        let hp = 10; // 5 corações inteiros
        let score = 0;
        let isInvincible = false;
        let gameLoop, spawnIntervalTime = 2000, skeletonSpawner;
        
        const inaraEl = document.getElementById('player-inara');
        const queenEl = document.getElementById('player-queen');
        const gameScreen = document.getElementById('game-screen');
        const heartsContainer = document.getElementById('hearts-container');
        
        let skeletons = [];
        let projectiles = [];

        function initGame() {{
            document.getElementById('menu-screen').classList.remove('active');
            gameScreen.classList.add('active');
            startBGM();
            updateHearts();
            updatePlayerPositions();
            
            gameLoop = setInterval(update, 30);
            scheduleSpawn();
        }}

        function updateHearts() {{
            heartsContainer.innerHTML = '';
            let fullHearts = Math.floor(hp / 2);
            let halfHeart = hp % 2 !== 0;
            let emptyHearts = 5 - Math.ceil(hp / 2);

            for(let i=0; i<fullHearts; i++) heartsContainer.innerHTML += '❤️';
            if(halfHeart) heartsContainer.innerHTML += '💔';
            for(let i=0; i<emptyHearts; i++) heartsContainer.innerHTML += '🖤';

            if(hp <= 0) gameOver();
        }}

        // Controles apenas pelas setas e espaço
        window.addEventListener('keydown', (e) => {{
            if(hp <= 0) return;
            if(e.code === 'ArrowLeft') {{ pX -= 30; if(pX < 50) pX = 50; }} // Limite para caber a Queen atrás
            if(e.code === 'ArrowRight') {{ pX += 30; if(pX > 730) pX = 730; }}
            if(e.code === 'ArrowUp' && !isJumping) {{ isJumping = true; pVelocityY = 20; }}
            if(e.code === 'Space') {{ e.preventDefault(); throwWeapons(); }}
        }});

        function throwWeapons() {{
            if(hp <= 0) return;
            playThrowSound();
            
            // Faca da Inara
            const knife = document.createElement('div');
            knife.className = 'knife';
            knife.style.left = (pX + 50) + 'px';
            knife.style.bottom = (pY + 40) + 'px';
            gameScreen.appendChild(knife);
            projectiles.push({{ el: knife, x: pX + 50, y: pY + 40 }});

            // Folha da Queen of Bones (Apenas na Fase 2)
            if(stage === 2) {{
                const leaf = document.createElement('div');
                leaf.className = 'leaf';
                leaf.style.left = (pX) + 'px'; // Atira um pouco atrás da Inara
                leaf.style.bottom = (pY + 65) + 'px'; // Um pouco mais alto
                gameScreen.appendChild(leaf);
                projectiles.push({{ el: leaf, x: pX, y: pY + 65 }});
            }}
        }}

        function scheduleSpawn() {{
            skeletonSpawner = setTimeout(() => {{
                spawnSkeleton();
                if(stage === 1 && spawnIntervalTime > 800) spawnIntervalTime -= 50; 
                scheduleSpawn();
            }}, spawnIntervalTime);
        }}

        function spawnSkeleton() {{
            const skel = document.createElement('div');
            skel.className = 'skeleton';
            skel.style.left = '800px';
            gameScreen.appendChild(skel);
            skeletons.push({{ el: skel, x: 800 }});
        }}

        function checkStageTransition() {{
            if(score >= 10 && stage === 1) {{
                stage = 2;
                gameScreen.style.backgroundImage = "url('{img_cena2}')";
                queenEl.style.display = 'block';
                spawnIntervalTime = 600; // Dobra a quantidade de inimigos
                
                const banner = document.getElementById('stage-banner');
                banner.style.display = 'block';
                setTimeout(() => banner.style.display = 'none', 3000);
            }}
        }}

        function updatePlayerPositions() {{
            inaraEl.style.left = pX + 'px';
            inaraEl.style.bottom = pY + 'px';
            
            if(stage === 2) {{
                // Queen of Bones segue a Inara um pouco atrás
                queenEl.style.left = (pX - 60) + 'px'; 
                queenEl.style.bottom = pY + 'px';
            }}
        }}

        function update() {{
            if(isJumping) {{
                pY += pVelocityY;
                pVelocityY -= 1.5; 
                if(pY <= 60) {{ pY = 60; isJumping = false; pVelocityY = 0; }}
            }}
            updatePlayerPositions();
            checkStageTransition();

            // Atualiza Projéteis (Facas e Folhas)
            for(let i = projectiles.length - 1; i >= 0; i--) {{
                let p = projectiles[i];
                p.x += 15; 
                p.el.style.left = p.x + 'px';
                
                if(p.x > 800) {{ p.el.remove(); projectiles.splice(i, 1); continue; }}
                
                for(let j = skeletons.length - 1; j >= 0; j--) {{
                    let s = skeletons[j];
                    if(Math.abs(p.x - s.x) < 40 && Math.abs(p.y - 60) < 60) {{
                        playHitSound();
                        s.el.remove();
                        skeletons.splice(j, 1);
                        p.el.remove();
                        projectiles.splice(i, 1);
                        score++;
                        document.getElementById('score').innerText = score;
                        break;
                    }}
                }}
            }}

            // Atualiza Esqueletos
            for(let i = skeletons.length - 1; i >= 0; i--) {{
                let s = skeletons[i];
                if(s.x > Math.max(10, skeletons.indexOf(s) * 30)) {{
                    s.x -= (stage === 2 ? 4 : 3); // Esqueletos ficam mais rápidos na fase 2
                }}
                s.el.style.left = s.x + 'px';

                if(!isInvincible && Math.abs(pX - s.x) < 40 && pY < 120) {{
                    takeDamage();
                }}
            }}
        }}

        function takeDamage() {{
            hp -= 1; 
            updateHearts();
            playDamageSound();
            isInvincible = true;
            
            inaraEl.style.filter = 'brightness(2) sepia(1) hue-rotate(300deg)';
            if(stage === 2) queenEl.style.filter = 'brightness(2) sepia(1) hue-rotate(300deg)';
            
            pX -= 60; if(pX < 60) pX = 60;

            setTimeout(() => {{
                isInvincible = false;
                inaraEl.style.filter = 'none';
                queenEl.style.filter = 'none';
            }}, 1000); 
        }}

        function gameOver() {{
            clearInterval(gameLoop);
            clearTimeout(skeletonSpawner);
            clearInterval(bgmInterval);
            document.getElementById('game-over').style.display = 'flex';
        }}
    </script>
</body>
</html>
"""

components.html(game_html, width=800, height=600)
