"""
Script d'exemple pour démontrer l'utilisation de l'Audio Enhancer
Crée un fichier audio de test et l'améliore
"""

import numpy as np
import soundfile as sf
from audio_enhancer import AudioEnhancer
import os


def create_test_audio_file(output_path='test_input.wav'):
    """
    Crée un fichier audio de test avec des variations de volume.
    Simule un audio avec des sections douces et fortes.
    """
    sample_rate = 44100
    duration = 5.0  # 5 secondes
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Créer un signal avec des variations de volume
    # Partie 1: Son faible (0.1 amplitude)
    part1 = 0.1 * np.sin(2 * np.pi * 440 * t[:sample_rate])
    
    # Partie 2: Son moyen (0.3 amplitude)
    part2 = 0.3 * np.sin(2 * np.pi * 880 * t[:sample_rate])
    
    # Partie 3: Son fort (0.8 amplitude)
    part3 = 0.8 * np.sin(2 * np.pi * 1320 * t[:sample_rate])
    
    # Partie 4: Son avec pics (0.95 amplitude)
    part4 = 0.95 * np.sin(2 * np.pi * 660 * t[:sample_rate])
    
    # Partie 5: Son faible à nouveau (0.15 amplitude)
    part5 = 0.15 * np.sin(2 * np.pi * 550 * t[:len(t) - 4*sample_rate])
    
    # Combiner toutes les parties
    audio_data = np.concatenate([part1, part2, part3, part4, part5])
    
    # Sauvegarder le fichier
    sf.write(output_path, audio_data.astype(np.float32), sample_rate)
    print(f"✓ Fichier audio de test créé: {output_path}")
    print(f"  - Durée: {duration} secondes")
    print(f"  - Taux d'échantillonnage: {sample_rate} Hz")
    print(f"  - Caractéristiques: Variations de volume importantes (0.1 à 0.95)")
    
    return output_path


def main():
    """Fonction principale pour exécuter l'exemple."""
    print("=" * 60)
    print("🎵 Exemple d'utilisation de Audio Enhancer")
    print("=" * 60)
    print()
    
    # 1. Créer un fichier audio de test
    print("Étape 1: Création d'un fichier audio de test...")
    input_file = create_test_audio_file('example_input.wav')
    print()
    
    # 2. Configurer l'enhancer
    print("Étape 2: Configuration de l'Audio Enhancer...")
    enhancer = AudioEnhancer(
        target_level_db=-20.0,  # Normaliser à -20 dB
        compression_ratio=4.0   # Compression 4:1
    )
    print("  ✓ Niveau cible: -20.0 dB")
    print("  ✓ Ratio de compression: 4.0:1")
    print()
    
    # 3. Améliorer l'audio
    print("Étape 3: Amélioration de l'audio...")
    output_file = 'example_output.wav'
    results = enhancer.enhance_audio(input_file, output_file)
    print()
    
    # 4. Afficher les résultats
    print("=" * 60)
    print("📊 COMPARAISON AVANT/APRÈS")
    print("=" * 60)
    print()
    print("Audio original:")
    print(f"  • RMS: {results['original']['rms_db']:.2f} dB")
    print(f"  • Peak: {results['original']['peak_db']:.2f} dB")
    print(f"  • Dynamic Range: {results['original']['dynamic_range']:.2f} dB")
    print(f"  • Clipping: {results['original']['clipping_percentage']:.2f}%")
    print()
    print("Audio amélioré:")
    print(f"  • RMS: {results['enhanced']['rms_db']:.2f} dB")
    print(f"  • Peak: {results['enhanced']['peak_db']:.2f} dB")
    print(f"  • Dynamic Range: {results['enhanced']['dynamic_range']:.2f} dB")
    print(f"  • Clipping: {results['enhanced']['clipping_percentage']:.2f}%")
    print()
    print("Améliorations:")
    rms_change = results['enhanced']['rms_db'] - results['original']['rms_db']
    dr_change = results['enhanced']['dynamic_range'] - results['original']['dynamic_range']
    print(f"  • Changement de RMS: {rms_change:+.2f} dB")
    print(f"  • Changement de Dynamic Range: {dr_change:+.2f} dB")
    print(f"  • Réduction du clipping: {results['original']['clipping_percentage'] - results['enhanced']['clipping_percentage']:.2f}%")
    print()
    print("=" * 60)
    print("✨ Exemple terminé avec succès!")
    print("=" * 60)
    print()
    print("Fichiers créés:")
    print(f"  • Input: {input_file}")
    print(f"  • Output: {output_file}")
    print()
    print("Vous pouvez maintenant comparer les deux fichiers audio!")


if __name__ == "__main__":
    main()
