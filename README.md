# 🎮 Tres en Raya con Algoritmo Minimax - IA vs Humano

![Demo del Juego](demo.gif)

## 📋 Tabla de Contenidos
- [🚀 Características](#-características-principales)
- [📦 Requisitos](#-requisitos)
- [🔧 Instalación](#-instalación)
- [🏃 Ejecución](#-ejecución)
- [🎮 Cómo Jugar](#-cómo-jugar)
- [🌳 Visualización](#-visualización-del-árbol-minimax)
- [📂 Estructura](#-estructura-del-código)
- [🤖 Algoritmo](#-algoritmo-minimax)
- [⚠️ Notas](#-notas-importantes)
- [📚 Recursos](#-recursos-adicionales)
- [🎨 Personalización](#-personalización)
- [🤝 Contribuciones](#-contribuciones)

## 🚀 Características Principales
- 🤖 **IA con Minimax**: Implementación completa con poda alpha-beta
- 🌳 **Visualización interactiva**: Árbol de decisiones en tiempo real
- 🎨 **Interfaz intuitiva**: Diseño moderno con Streamlit
- 📊 **Estadísticas**: Seguimiento de victorias, derrotas y empates
- 📝 **Historial**: Registro detallado de todos los movimientos
- ⚡ **Optimizado**: Alto rendimiento incluso en dispositivos móviles

## 📦 Requisitos
Python 3.8+
Streamlit >= 1.22
Graphviz >= 0.20
Plotly >= 5.11
Numpy >= 1.24

## 🔧 Instalación
Clona el repositorio:

- git clone https://github.com/tu-usuario/tres-en-raya-minimax.git
- cd tres-en-raya-minimax
- Crea y activa un entorno virtual (recomendado):

python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
- .\venv\Scripts\activate
Instala las dependencias:
- pip install -r requirements.txt

## 🏃 Ejecución
streamlit run app.py
La aplicación estará disponible en: http://localhost:8501

## 🎮 Cómo Jugar
La IA (🤖 MAX) siempre juega primero con X
Tú (👤 MIN) juegas con O
Haz clic en cualquier celda vacía durante tu turno
Observa cómo la IA evalúa todas las posibilidades
¡Intenta vencer a la IA o forzar un empate!

## 🌳 Visualización del Árbol Minimax
La aplicación muestra:
- Nodos MAX (IA) y MIN (Humano)
- Valores propagados hacia arriba
- Movimientos óptimos vs. descartados
- Estrategia de decisión en cada nivel
- Profundidad limitada para mejor rendimiento

## 📂 Estructura del Proyecto

```bash
tres-en-raya-minimax/
│
├── app.py                # Lógica principal del juego
├── README.md             # Documentación del proyecto
├── requirements.txt      # Lista de dependencias
├── assets/               # Directorio de recursos
│   ├── images/           # Capturas de pantalla
│   └── demo.gif          # GIF demostrativo
└── .gitignore            # Archivos excluidos de Git


## ⚠️ Notas Importantes
- La IA juega perfectamente (nunca pierde)
- Las estadísticas persisten durante la sesión
- El árbol se limita a profundidad 3 por rendimiento
