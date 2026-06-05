import streamlit as st
import streamlit.components.v1 as components

# Configuração da página para o jogo ocupar a tela direitinho
st.set_page_config(page_title="Ina Game", layout="centered")

# Ocultar menus padrões do Streamlit para parecer um app nativo
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# Bloco do Jogo em HTML5 / JavaScript
game_html = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #111;
            color: #fff;
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }
        #game-container {
            width: 800px;
            height: 600px;
            background-color: #000;
            position: relative;
            border: 4px solid #333;
            box-shadow: 0 0 20px rgba(0,0,0,0.8);
        }
        .screen {
            width: 100%;
            height: 100%;
            position: absolute;
            top: 0;
            left: 0;
            display: none;
            background-size: cover;
            background-position: center;
        }
        .active {
            display: block;
        }
        /* Estilos do Menu */
        #menu-screen {
            background-image: url('Capa.png');
            text-align: center;
        }
        .btn-game {
            padding: 12px 24px;
            font-size: 18px;
            cursor: pointer;
            background-color: #8b0000;
            color: white;
            border: 2px solid #fff;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            transition: 0.3s;
            box-shadow: 0 4px 8px rgba(0,0,0,0.5);
        }
        .btn-game:hover {
            background-color: #ff0000;
            transform: scale(1.05);
        }
        #start-btn {
            position: absolute;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%);
        }
        /* Caixa de Diálogo */
        .dialogue-box {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 740px;
            height: 140px;
            background: rgba(0, 0, 0, 0.85);
            border: 3px solid #8b0000;
            border-radius: 8px;
            padding: 15px;
            box-sizing: border-box;
        }
        .dialogue-text {
            font-size: 18px;
            line-height: 1.4;
            margin-bottom: 10px;
        }
        .options-container {
            display: flex;
            gap: 10px;
            position: absolute;
            bottom: 15px;
            right: 15px;
        }
        .btn-option {
            background: #222;
            color: #fff;
            border: 1px solid #8b0000;
            padding: 6px 12px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-size: 14px;
        }
        .btn-option:hover {
            background: #8b0000;
        }
    </style>
</head>
<body>

    <div id="game-container">
        <div id="menu-screen" class="screen active">
            <button id="start-btn" class="btn-game" onclick="startGame()">INICIAR JOGO</button>
        </div>

        <div id="game-screen" class="screen">
            <div class="dialogue-box">
                <div id="text-box" class="dialogue-text">Carregando história...</div>
                <div id="options" class="options-container"></div>
            </div>
        </div>
    </div>

    <script>
        // Sons usando a Web Audio API nativa (Beeps Estilo Retro de 8-bits)
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

        function playBeep(type, frequency, duration) {
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
            const oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();

            oscillator.type = type; // 'sine', 'square', 'sawtooth', 'triangle'
            oscillator.frequency.setValueAtTime(frequency, audioCtx.currentTime);
            
            gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.00001, audioCtx.currentTime + duration);

            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);

            oscillator.start();
            oscillator.stop(audioCtx.currentTime + duration);
        }

        function playTextSound() {
            playBeep('sine', 300, 0.05);
        }

        function playCombatSound() {
            // Efeito Tchim Tchim de lâminas se batendo
            playBeep('sawtooth', 800, 0.08);
            setTimeout(() => playBeep('sawtooth', 1200, 0.1), 80);
        }

        // Variáveis de Estado do Jogo
        let currentStage = "intro";
        const gameScreen = document.getElementById('game-screen');
        const menuScreen = document.getElementById('menu-screen');
        const textBox = document.getElementById('text-box');
        const optionsBox = document.getElementById('options');

        const story = {
            intro: {
                text: "Você acorda sob uma névoa densa. À sua frente está a entrada de uma masmorra gótica esquecida pelo tempo. Um frio cortante atravessa sua espinha.",
                bg: "Cenário 1.png",
                sound: "text",
                options: [
                    { text: "Entrar na masmorra", next: "sala_principal" },
                    { text: "Olhar ao redor", next: "olhar_redor" }
                ]
            },
            olhar_redor: {
                text: "Rachaduras no chão revelam raízes escuras e runas antigas entalhadas na pedra que brilham fracamente em um tom carmesim. Não há escapatória além da porta.",
                bg: "Cenário 1.png",
                sound: "text",
                options: [
                    { text: "Dar um passo à frente e entrar", next: "sala_principal" }
                ]
            },
            sala_principal: {
                text: "Lá dentro, tochas se acendem sozinhas com chamas azuis. No centro do salão, duas figuras esqueléticas guardam um baú acorrentado.",
                bg: "Cenário 2.png",
                sound: "text",
                options: [
                    { text: "Sacar sua adaga e atacar", next: "combate" },
                    { text: "Tentar passar furtivamente", next: "furtivo" }
                ]
            },
            combate: {
                text: "Com um movimento rápido, você avança! O som de metal contra os ossos ecoa pelas paredes de pedra! *TCHIM! TCHIM!*",
                bg: "Cenário 3.png",
                sound: "combat",
                options: [
                    { text: "Continuar golpeando", next: "vitoria" }
                ]
            },
            furtivo: {
                text: "Você pisa em falso em um osso seco. O estalo reverbera pelo salão vazio e os esqueletos viram suas órbitas vazias em sua direção de forma ameaçadora!",
                bg: "Cenário 2.png",
                sound: "text",
                options: [
                    { text: "Não há escolha: Lutar!", next: "combate" }
                ]
            },
            vitoria: {
                text: "Os esqueletos se desfazem em poeira de ossos. O baú se abre revelando a relíquia perdida que você buscou por eras. Você venceu o desafio das sombras!",
                bg: "Cenário 4.png",
                sound: "text",
                options: [
                    { text: "Voltar ao Menu", next: "menu" }
                ]
            }
        };

        function startGame() {
            menuScreen.classList.remove('active');
            gameScreen.classList.add('active');
            goToStage("intro");
        }

        function goToStage(stageKey) {
            if (stageKey === "menu") {
                gameScreen.classList.remove('active');
                menuScreen.classList.add('active');
                return;
            }

            currentStage = stageKey;
            const stage = story[stageKey];

            // Troca o plano de fundo dinamicamente
            gameScreen.style.backgroundImage = `url('${stage.bg}')`;

            // Executa os beeps retro correspondentes à ação
            if (stage.sound === "combat") {
                playCombatSound();
            } else {
                playTextSound();
            }

            // Exibe o texto
            textBox.innerText = stage.text;

            // Renderiza os botões de escolha
            optionsBox.innerHTML = "";
            stage.options.forEach(opt => {
                const btn = document.createElement('button');
                btn.className = "btn-option";
                btn.innerText = opt.text;
                btn.onclick = () => goToStage(opt.next);
                optionsBox.appendChild(btn);
            });
        }
    </script>
</body>
</html>
"""

# Renderiza o componente HTML em tela cheia na interface do Streamlit
components.html(game_html, width=800, height=600)
