# Tres en Raya con Algoritmo Minimax - IA vs Humano

## Tabla de Contenidos
- [Características Principales](#-características-principales)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Ejecución](#-ejecución)
- [Cómo Jugar](#-cómo-jugar)
- [Visualización del Árbol Minimax](#-visualización-del-árbol-minimax)
- [Estructura del Código](#-estructura-del-código)
- [Algoritmo Minimax](#-algoritmo-minimax)
- [Notas Importantes](#-notas-importantes)
- [Recursos Adicionales](#-recursos-adicionales)
- [Personalización](#-personalización)
- [Contribuciones](#-contribuciones)

## 🚀 Características Principales
- **🤖 IA con Minimax**: Implementación clara del algoritmo Minimax
- **🌳 Visualización del Árbol**: Muestra el árbol de decisiones de la IA
- **🎮 Interfaz Intuitiva**: Diseño moderno y responsive
- **📊 Estadísticas**: Seguimiento de victorias, derrotas y empates
- **📝 Historial de Movimientos**: Registro detallado de cada partida

## 📦 Requisitos
- Python 3.8+
- Streamlit
- Graphviz
- Plotly
- Numpy

## 🔧 Instalación
1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/tres-en-raya-minimax.git
cd tres-en-raya-minimax

## Crea y activa un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

## Instala las dependencias:
```bash
pip install -r requirements.txt

## Ejecución
```bash
streamlit run app.py

Para iniciar la aplicación:
```bash
streamlit run app.py

## 🎮 Cómo Jugar
La IA (MAX) siempre juega primero con 'X'
El humano (MIN) juega con 'O'
Haz clic en cualquier celda vacía durante tu turno
Observa cómo la IA evalúa todas las posibilidades
¡Intenta vencer a la IA o forzar un empate!

## 📊 Visualización del Árbol Minimax
La aplicación muestra:
Nodos MAX (IA) y MIN (Humano)
Valores propagados hacia arriba
Movimientos elegidos y descartados
Estrategia de decisión en cada nivel
