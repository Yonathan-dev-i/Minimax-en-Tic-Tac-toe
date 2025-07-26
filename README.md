

🔧 Instalación
Clona el repositorio:

bash
git clone https://github.com/tu-usuario/tres-en-raya-minimax.git
cd tres-en-raya-minimax
Crea y activa un entorno virtual (recomendado):

bash
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
.\venv\Scripts\activate
Instala las dependencias:

bash
pip install -r requirements.txt
🏃 Ejecución
bash
streamlit run app.py
La aplicación estará disponible en: http://localhost:8501

🎮 Cómo Jugar
La IA (🤖 MAX) siempre juega primero con X

Tú (👤 MIN) juegas con O

Haz clic en cualquier celda vacía durante tu turno

Observa cómo la IA evalúa todas las posibilidades

¡Intenta vencer a la IA o forzar un empate!

🌳 Visualización del Árbol Minimax
La aplicación muestra:

Nodos MAX (IA) y MIN (Humano)

Valores propagados hacia arriba

Movimientos óptimos vs. descartados

Estrategia de decisión en cada nivel

Profundidad limitada para mejor rendimiento

📂 Estructura del Proyecto
text
tres-en-raya-minimax/
│
├── app.py                # Lógica principal
├── README.md             # Este archivo
├── requirements.txt      # Dependencias
├── assets/               # Recursos
│   ├── images/           # Capturas
│   └── demo.gif          # Demostración
└── .gitignore            # Archivos excluidos
🤖 Algoritmo Minimax
python
def minimax(node, depth, is_maximizing, alpha=-float('inf'), beta=float('inf')):
    if node.is_terminal() or depth == 0:
        return node.evaluate()
    
    if is_maximizing:
        value = -float('inf')
        for child in node.children:
            value = max(value, minimax(child, depth-1, False, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta: break  # Poda beta
        return value
    else:
        value = float('inf')
        for child in node.children:
            value = min(value, minimax(child, depth-1, True, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta: break  # Poda alpha
        return value
⚠️ Notas Importantes
La IA juega perfectamente (nunca pierde)

Las estadísticas persisten durante la sesión

El árbol se limita a profundidad 3 por rendimiento

Versión optimizada con alpha-beta pruning
