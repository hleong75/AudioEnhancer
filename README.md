# AudioEnhancer 🎵

Un programme intelligent d'amélioration audio qui analyse et améliore automatiquement vos fichiers audio en normalisant les niveaux sonores.

## 🎯 Fonctionnalités

- **Analyse intelligente de l'audio** : Le programme analyse automatiquement l'audio pour déterminer les améliorations nécessaires
- **Normalisation des niveaux** : Équilibre les niveaux sonores pour éviter les sons très bas ou très hauts
- **Compression dynamique** : Réduit les variations extrêmes d'amplitude tout en préservant la dynamique
- **Limitation anti-clipping** : Empêche la distorsion en limitant les pics
- **Support multi-formats** : WAV, MP3, FLAC, OGG, et plus encore

## 📋 Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

## 🚀 Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/hleong75/AudioEnhancer.git
cd AudioEnhancer
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## 💻 Utilisation

### Utilisation de base

```bash
python cli.py input.wav output.wav
```

### Options avancées

```bash
# Spécifier le niveau cible de normalisation (-18 dB)
python cli.py input.mp3 output.mp3 --target-level -18

# Ajuster le ratio de compression (6:1)
python cli.py input.wav output.wav --compression-ratio 6

# Mode verbeux pour plus de détails
python cli.py input.wav output.wav --verbose

# Combiner plusieurs options
python cli.py input.wav output.wav -t -16 -c 5 -v
```

### Utilisation en tant que module Python

```python
from audio_enhancer import AudioEnhancer

# Créer l'enhancer
enhancer = AudioEnhancer(
    target_level_db=-20.0,  # Niveau cible en dB
    compression_ratio=4.0   # Ratio de compression
)

# Améliorer l'audio
results = enhancer.enhance_audio('input.wav', 'output.wav')

# Accéder aux résultats de l'analyse
print(f"RMS original: {results['original']['rms_db']:.2f} dB")
print(f"RMS amélioré: {results['enhanced']['rms_db']:.2f} dB")
```

## 🔧 Paramètres

| Paramètre | Option | Défaut | Description |
|-----------|--------|--------|-------------|
| Niveau cible | `--target-level` ou `-t` | -20.0 dB | Niveau RMS cible pour la normalisation |
| Ratio de compression | `--compression-ratio` ou `-c` | 4.0 | Ratio de compression dynamique (1.0-10.0) |
| Mode verbeux | `--verbose` ou `-v` | False | Affiche plus de détails sur le traitement |

## 📊 Comment ça marche ?

1. **Analyse** : Le programme analyse l'audio pour identifier :
   - Le niveau RMS (Root Mean Square)
   - Les pics d'amplitude
   - La plage dynamique
   - Le contenu fréquentiel
   - Les problèmes de clipping

2. **Normalisation** : Ajuste le niveau global de l'audio au niveau cible spécifié

3. **Compression dynamique** : Réduit les pics excessifs tout en préservant les parties plus douces

4. **Limitation** : Empêche le clipping en limitant les valeurs maximales à un plafond sûr

## 🎓 Exemples de résultats

### Avant amélioration
```
RMS: -28.5 dB
Peak: -2.1 dB
Dynamic Range: 26.4 dB
Clipping: 2.3%
```

### Après amélioration
```
RMS: -20.0 dB
Peak: -1.2 dB
Dynamic Range: 18.8 dB
Clipping: 0.0%
```

## 🛠️ Développement

### Structure du projet

```
AudioEnhancer/
├── audio_enhancer.py   # Module principal d'amélioration audio
├── cli.py              # Interface en ligne de commande
├── requirements.txt    # Dépendances Python
├── tests/              # Tests unitaires
└── README.md          # Ce fichier
```

### Exécuter les tests

```bash
pytest tests/
```

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.