import streamlit as st
import graphviz
import time
import plotly.graph_objects as go
import numpy as np

# Clase para nodos del árbol Minimax
class MinimaxNode:
    def __init__(self, board, depth, is_maximizing, move=None):
        self.board = board.copy()
        self.depth = depth
        self.is_maximizing = is_maximizing
        self.move = move
        self.value = None
        self.children = []

# Inicializar estado de la sesión
if 'board' not in st.session_state:
    st.session_state.board = [0] * 9  # 0: vacío, 1: X (IA), -1: O (Humano)
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'minimax_tree' not in st.session_state:
    st.session_state.minimax_tree = None
if 'game_stats' not in st.session_state:
    st.session_state.game_stats = {'wins': 0, 'losses': 0, 'draws': 0}
if 'move_history' not in st.session_state:
    st.session_state.move_history = []
if 'ai_turn' not in st.session_state:
    st.session_state.ai_turn = True  # IA empieza primero
if 'game_started' not in st.session_state:
    st.session_state.game_started = False

# Configuración de la página
st.set_page_config(
    page_title="Tres en Raya - Minimax AI",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS mejorados
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .game-board {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    
    .stButton > button {
        width: 100%;
        height: 100px;
        font-size: 3rem;
        font-weight: bold;
        border-radius: 15px;
        border: 3px solid #e0e0e0;
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        color: #495057;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    
    .stButton > button:disabled {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        color: #6c757d;
        transform: none;
        cursor: not-allowed;
    }
    
    .btn-x {
        background: linear-gradient(145deg, #ff6b6b, #ee5a52) !important;
        color: white !important;
        border-color: #ff5252 !important;
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3) !important;
    }
    
    .btn-o {
        background: linear-gradient(145deg, #4ecdc4, #45b7aa) !important;
        color: white !important;
        border-color: #4ecdc4 !important;
        box-shadow: 0 5px 15px rgba(78, 205, 196, 0.3) !important;
    }
    
    .stats-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .stats-item {
        display: inline-block;
        margin: 0 1rem;
        text-align: center;
    }
    
    .stats-number {
        font-size: 2rem;
        font-weight: 700;
        display: block;
    }
    
    .stats-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .tree-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        border: 1px solid #e0e0e0;
        min-height: 600px;
        max-height: 800px;
        overflow: auto;
    }
    
    .success-message {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    .error-message {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    .warning-message {
        background: linear-gradient(135deg, #fdbb2d 0%, #22c1c3 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    .sidebar .element-container {
        background: rgba(103, 126, 234, 0.05);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    .move-history {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
    
    .tree-legend {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid #17a2b8;
    }
    
    .legend-item {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .legend-color {
        width: 20px;
        height: 20px;
        border-radius: 4px;
        margin-right: 10px;
    }
    
    .tree-controls {
        background: #e3f2fd;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .player-config {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
    }
    
    .config-section {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .turn-indicator {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: #333;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        margin: 1rem 0;
        border: 2px solid #ff6b9d;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🎮 Tres en Raya - Minimax AI</h1>
    <p>La IA (MAX) empieza primero, el Humano (MIN) responde</p>
</div>
""", unsafe_allow_html=True)

# Configuración de jugadores
st.markdown("""
<div class="player-config">
    <h3>⚙️ Configuración de Jugadores</h3>
    <div class="config-section">
        <h4>🤖 IA (MAX) - Juega Primero</h4>
        <ul>
            <li>Juega con 'X' y <strong>empieza la partida</strong></li>
            <li>Quiere <strong>maximizar</strong> su utilidad</li>
            <li>Busca el mejor movimiento para ganar o empatar</li>
        </ul>
    </div>
    <div class="config-section">
        <h4>👤 Humano (MIN) - Responde</h4>
        <ul>
            <li>Juega con 'O' después de la IA</li>
            <li>Desde la perspectiva de la IA, el humano <strong>minimiza</strong> la utilidad de MAX</li>
            <li>Se asume que el humano juega óptimamente</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

# Función para imprimir el tablero mejorado
def print_board():
    st.markdown('<div class="game-board">', unsafe_allow_html=True)
    
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            i = row * 3 + col
            with cols[col]:
                if st.session_state.board[i] == 0:
                    # Solo permitir clics si es turno del humano y el juego no ha terminado
                    disabled = st.session_state.game_over or st.session_state.ai_turn
                    if st.button(" ", key=f"btn_{i}", disabled=disabled) and not disabled:
                        make_human_move(i)
                elif st.session_state.board[i] == 1:  # IA juega con X
                    st.button("X", key=f"btn_{i}_x", disabled=True)
                else:  # Humano juega con O
                    st.button("O", key=f"btn_{i}_o", disabled=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Movimiento del humano (MIN)
def make_human_move(position):
    st.session_state.board[position] = -1  # Humano juega con O (-1)
    st.session_state.move_history.append(f"👤 Humano (MIN): Posición {position} - juega 'O'")
    st.session_state.ai_turn = True  # Ahora es turno de la IA
    
    # Verificar si el juego terminó después del movimiento humano
    if check_game_status():
        st.session_state.game_over = True
        st.rerun()
    else:
        # Si el juego no terminó, la IA hace su movimiento
        time.sleep(0.5)
        ai_move()
        st.session_state.ai_turn = False  # Después del movimiento de IA, turno del humano
        st.session_state.game_over = check_game_status()
        st.rerun()

# ALGORITMO MINIMAX CLARIFICADO
def minimax(node, depth, is_maximizing_turn, max_depth=9):
    """
    Algoritmo Minimax clarificado:
    - MAX (IA): Busca maximizar su utilidad (mejores valores)
    - MIN (Humano): Desde perspectiva de IA, minimiza utilidad de MAX
    """
    score = evaluate_for_max_player(node.board)
    
    # Condiciones terminales
    if score != 0 or is_board_full(node.board) or depth >= max_depth:
        node.value = score
        return score

    if is_maximizing_turn:  # Turno de MAX (IA con X)
        best_value = float('-inf')
        for i in range(9):
            if node.board[i] == 0:
                new_board = node.board.copy()
                new_board[i] = 1  # IA (MAX) juega con X (1)
                child = MinimaxNode(new_board, depth+1, False, move=i)
                node.children.append(child)
                
                current_value = minimax(child, depth+1, False, max_depth)
                best_value = max(best_value, current_value)
        
        node.value = best_value
        return best_value
    else:  # Turno de MIN (Humano con O)
        best_value = float('inf')
        for i in range(9):
            if node.board[i] == 0:
                new_board = node.board.copy()
                new_board[i] = -1  # Humano (MIN) juega con O (-1)
                child = MinimaxNode(new_board, depth+1, True, move=i)
                node.children.append(child)
                
                current_value = minimax(child, depth+1, True, max_depth)
                best_value = min(best_value, current_value)
        
        node.value = best_value
        return best_value

# Movimiento de la IA (MAX)
def ai_move():
    """IA (MAX) busca maximizar su utilidad"""
    root = MinimaxNode(st.session_state.board, 0, True)  # IA empieza como MAX
    minimax(root, 0, True, max_depth=9)
    st.session_state.minimax_tree = root
    
    # MAX elige el movimiento con el MAYOR valor
    if root.children:
        best_move_node = max(root.children, key=lambda x: x.value if x.value is not None else float('-inf'))
        best_move = best_move_node.move
        st.session_state.board[best_move] = 1  # IA juega con X
        st.session_state.move_history.append(f"🤖 IA (MAX): Posición {best_move} - juega 'X' (Valor: {best_move_node.value})")

# Funciones de evaluación
def is_winner(board, player):
    win_patterns = [
        [0,1,2], [3,4,5], [6,7,8],  # Filas
        [0,3,6], [1,4,7], [2,5,8],  # Columnas
        [0,4,8], [2,4,6]            # Diagonales
    ]
    return any(all(board[i] == player for i in pattern) for pattern in win_patterns)

def is_board_full(board):
    return all(cell != 0 for cell in board)

# Función de evaluación desde la perspectiva de MAX (IA)
def evaluate_for_max_player(board):
    """
    Evaluación desde la perspectiva de MAX (IA):
    - MAX gana: +10 (bueno para MAX)
    - MIN gana: -10 (malo para MAX)  
    - Empate: 0 (neutro)
    """
    if is_winner(board, 1):  # MAX (IA con X) gana
        return 10  # Valor POSITIVO para MAX
    elif is_winner(board, -1):  # MIN (Humano con O) gana
        return -10  # Valor NEGATIVO para MAX
    else:
        return 0  # Empate

# Función optimizada para visualizar el árbol Minimax
def visualize_minimax_tree_compact(node, max_depth=3):
    if not node:
        st.warning("No hay datos del árbol para mostrar")
        return

    def format_board(board):
        symbols = {0: " ", 1: "X", -1: "O"}
        lines = []
        for row in range(3):
            line = f"{symbols[board[row*3]]}|{symbols[board[row*3+1]]}|{symbols[board[row*3+2]]}"
            lines.append(line)
        return "\n".join(lines)

    dot = graphviz.Digraph(graph_attr={'rankdir': 'LR'})

    # Nodo raíz
    root_label = f"{format_board(node.board)}\nValor: {node.value}\nMAX (IA - busca maximizar)"
    dot.node("root", label=root_label, shape="box", fontfamily="monospace",
             style="filled", color="#FFD700", fillcolor="#fffacd")

    # Nivel 1 - Movimientos de MAX (IA)
    if node.children and node.depth < 2:
        for idx, child in enumerate(node.children):
            child_id = f"level1_{idx}"
            child_label = f"{format_board(child.board)}\nValor: {child.value}\nMIN (Humano - minimiza MAX)\nMov: {child.move}"
            
            # Colorear el mejor movimiento para MAX
            is_best = child.value == max(c.value for c in node.children if c.value is not None)
            color = "#32CD32" if is_best else "#8A2BE2"
            fillcolor = "#f0fff0" if is_best else "#f5e6fa"
            
            dot.node(child_id, label=child_label, shape="box", fontfamily="monospace",
                     style="filled", color=color, fillcolor=fillcolor)
            
            edge_color = "green" if is_best else "black"
            edge_style = "bold" if is_best else "solid"
            dot.edge("root", child_id, color=edge_color, style=edge_style)
            
            # Nivel 2 - Respuestas de MIN (Humano)
            if child.children and child.depth < 2:
                for idx2, grandchild in enumerate(child.children[:3]):
                    grandchild_id = f"level2_{idx}_{idx2}"
                    grandchild_label = f"{format_board(grandchild.board)}\nVal: {grandchild.value}\nMAX (busca max)\nMov: {grandchild.move}"
                    
                    dot.node(grandchild_id, label=grandchild_label, shape="box", fontfamily="monospace",
                             style="filled", color="#FF6347", fillcolor="#ffe4e1")
                    dot.edge(child_id, grandchild_id)

    return dot

# Verificar estado del juego
def check_game_status():
    if is_winner(st.session_state.board, 1):  # IA (X) gana
        st.session_state.game_stats['losses'] += 1  # Derrota para humano
        return True
    elif is_winner(st.session_state.board, -1):  # Humano (O) gana
        st.session_state.game_stats['wins'] += 1  # Victoria para humano
        return True
    elif is_board_full(st.session_state.board):
        st.session_state.game_stats['draws'] += 1
        return True
    return False

# Función para reiniciar el juego
def reset_game():
    st.session_state.board = [0] * 9
    st.session_state.game_over = False
    st.session_state.minimax_tree = None
    st.session_state.move_history = []
    st.session_state.ai_turn = True  # IA empieza primero
    st.session_state.game_started = False
    st.rerun()

# Función para que la IA haga el primer movimiento
def start_game():
    if not st.session_state.game_started:
        st.session_state.game_started = True
        ai_move()  # IA hace el primer movimiento
        st.session_state.ai_turn = False  # Después del primer movimiento, turno del humano
        st.rerun()

# Sidebar con información del juego
with st.sidebar:
    st.markdown("### 📊 Estadísticas del Juego")
    stats = st.session_state.game_stats
    total_games = stats['wins'] + stats['losses'] + stats['draws']
    
    if total_games > 0:
        win_rate = (stats['wins'] / total_games) * 100
        ai_win_rate = (stats['losses'] / total_games) * 100
        st.markdown(f"""
        <div class="stats-container">
            <div class="stats-item">
                <span class="stats-number">{stats['wins']}</span>
                <span class="stats-label">Humano (MIN) Gana</span>
            </div>
            <div class="stats-item">
                <span class="stats-number">{stats['losses']}</span>
                <span class="stats-label">IA (MAX) Gana</span>
            </div>
            <div class="stats-item">
                <span class="stats-number">{stats['draws']}</span>
                <span class="stats-label">Empates</span>
            </div>
        </div>
        <p style="text-align: center; font-weight: 600;">
            📈 MIN: {win_rate:.1f}% | 🤖 MAX: {ai_win_rate:.1f}%
        </p>
        """, unsafe_allow_html=True)
    else:
        st.info("🎯 ¡Juega tu primera partida!")
    
    st.markdown("### 🎯 Configuración")
    if st.button("🔄 Reiniciar Juego", key="reset_game"):
        reset_game()
    
    if st.button("📊 Limpiar Estadísticas"):
        st.session_state.game_stats = {'wins': 0, 'losses': 0, 'draws': 0}
        st.rerun()
    
    st.markdown("### 📝 Historial de Movimientos")
    if st.session_state.move_history:
        st.markdown('<div class="move-history">', unsafe_allow_html=True)
        for i, move in enumerate(st.session_state.move_history[-10:], 1):
            st.write(f"{i}. {move}")
        if len(st.session_state.move_history) > 10:
            st.caption("Mostrando últimos 10 movimientos")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No hay movimientos aún")

# Layout principal
col1, col2 = st.columns([1.2, 1.8])

with col1:
    st.markdown("### 🎯 Tablero de Juego")
    
    # Botón para iniciar el juego si no ha empezado
    if not st.session_state.game_started and all(cell == 0 for cell in st.session_state.board):
        if st.button("🚀 ¡Empezar Juego! (IA hace primer movimiento)", key="start_game"):
            start_game()
        st.info("🤖 La IA (MAX) hará el primer movimiento cuando presiones el botón")
    
    # Indicador de turno
    if st.session_state.game_started and not st.session_state.game_over:
        if st.session_state.ai_turn:
            st.markdown('<div class="turn-indicator">🤖 Turno de la IA (MAX) - Procesando...</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="turn-indicator">👤 Tu turno (MIN) - Elige tu movimiento</div>', unsafe_allow_html=True)
    
    # Mostrar estado del juego
    if st.session_state.game_over:
        if is_winner(st.session_state.board, -1):  # Humano (O) gana
            st.markdown('<div class="success-message">🎉 ¡Humano (MIN) ha ganado! ¡Lograste minimizar la utilidad de MAX!</div>', unsafe_allow_html=True)
        elif is_winner(st.session_state.board, 1):  # IA (X) gana
            st.markdown('<div class="error-message">🤖 ¡IA (MAX) ha ganado! MAX maximizó su utilidad exitosamente</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-message">⚖️ ¡Empate! Ambos jugadores jugaron óptimamente</div>', unsafe_allow_html=True)
    
    print_board()

with col2:
    if st.session_state.minimax_tree:
        try:
            tree_graph = visualize_minimax_tree_compact(st.session_state.minimax_tree, max_depth=2)
            if tree_graph:
                st.subheader("🧩 Árbol Minimax: MAX vs MIN")
                st.graphviz_chart(tree_graph, use_container_width=True)
            else:
                st.warning("⚠️ No se pudo generar el árbol de decisiones")
        except Exception as e:
            st.error(f"❌ Error al generar el árbol: {str(e)}")
        
        # Información del último movimiento
        if st.session_state.minimax_tree.children:
            best_child = max(st.session_state.minimax_tree.children, key=lambda x: x.value if x.value is not None else float('-inf'))
            st.info(f"🎯 **MAX eligió:** Posición {best_child.move} con valor {best_child.value} (maximizando utilidad)")
            
            # Mostrar análisis de opciones
            st.markdown("### 📋 Análisis de Opciones de MAX")
            options_data = []
            for child in st.session_state.minimax_tree.children:
                strategy = "ELEGIDO" if child == best_child else "DESCARTADO"
                reason = "Mayor valor" if child == best_child else "Menor valor"
                options_data.append({
                    'Posición': child.move,
                    'Valor': child.value,
                    'Estrategia MAX': strategy,
                    'Razón': reason
                })
            
            if options_data:
                import pandas as pd
                df = pd.DataFrame(options_data)
                st.dataframe(df, use_container_width=True)
    else:
        st.info("🔍 El árbol de decisiones aparecerá después del primer movimiento de la IA")

# Sección de información expandible
with st.expander("📚 Flujo del Juego: IA Primero", expanded=False):
    st.markdown("""
    ### 🔄 **Secuencia de Juego**
    
    1. **🤖 IA (MAX) inicia**: Hace el primer movimiento con 'X'
    2. **👤 Humano (MIN) responde**: Elige posición para 'O' 
    3. **🔁 Alternancia**: Continúan alternando hasta terminar
    
    ### 🎯 **Ventajas de que IA empiece primero:**
    - Permite observar la estrategia de MAX desde el inicio
    - El árbol Minimax se visualiza desde la primera jugada
    - Demuestra cómo MAX evalúa todas las posibilidades iniciales
    
    ### 🧠 **Algoritmo en Acción:**
    - **MAX (IA)**: Evalúa todas las posiciones vacías y elige la de mayor valor
    - **MIN (Humano)**: La IA simula tus mejores respuestas (menor valor para MAX)
    - **Resultado**: Juego perfecto siempre termina en empate cuando ambos juegan óptimamente
    """)

with st.expander("📚 Algoritmo Minimax: MAX vs MIN", expanded=False):
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown("""
        ### 🤖 **Jugador MAX (IA)**
        
        **🎯 Objetivo:** Maximizar utilidad
        
        **🔧 Estrategia:**
        - Busca valores más altos (+10)
        - Evita valores bajos (-10)
        - Usa `max()` para elegir
        
        **⚡ En cada turno:**
        ```python
        best_value = float('-inf')
        for movimiento in movimientos_posibles:
            valor = minimax(movimiento)
            best_value = max(best_value, valor)
        ```
        
        **🏆 Meta:** Ganar (+10) o empatar (0)
        """)
    
    with col_info2:
        st.markdown("""
        ### 👤 **Jugador MIN (Humano)**
        
        **🎯 Objetivo:** Minimizar utilidad de MAX
        
        **🔧 Estrategia:**
        - Busca valores más bajos para MAX
        - Prefiere que MAX obtenga -10
        - IA usa `min()` para simular jugadas de MIN
        
        **⚡ Simulación de MIN:**
        ```python
        best_value = float('inf')
        for movimiento in movimientos_posibles:
            valor = minimax(movimiento)
            best_value = min(best_value, valor)
        ```
        
        **🏆 Meta:** Ganar (-10 para MAX) o empatar (0)
        """)

st.markdown("""
### 🚀 **Cómo funciona MAX vs MIN**

1. **🤖 MAX (IA con X)**: Siempre busca el **valor más alto** para maximizar su beneficio
2. **👤 MIN (Humano con O)**: La IA simula que juegas óptimamente, **minimizando su beneficio**
3. **🔄 Alternancia**: El algoritmo alterna entre MAX y MIN en cada nivel del árbol
4. **📊 Propagación**: Los valores se propagan hacia arriba según la estrategia de cada jugador

**🎯 Resultado:** 
- MAX elige movimientos que le den la **mayor ventaja**
- MIN (simulado) elige movimientos que le den la **menor ventaja a MAX**
- ¡El juego perfecto siempre termina en empate! 🤝

¡Observa cómo MAX siempre busca maximizar mientras asume que MIN jugará óptimamente! 🧠
""")