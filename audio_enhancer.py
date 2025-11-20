"""
Audio Enhancer - Analyse et améliore les fichiers audio
Normalise les niveaux sonores pour éviter les sons très bas ou très hauts
"""

import numpy as np
import librosa
import soundfile as sf
from scipy import signal
from typing import Tuple, Optional
import os


class AudioEnhancer:
    """
    Classe principale pour l'amélioration audio.
    Analyse et améliore les fichiers audio en normalisant les niveaux sonores.
    """
    
    def __init__(self, target_level_db: float = -20.0, compression_ratio: float = 4.0):
        """
        Initialise l'Audio Enhancer.
        
        Args:
            target_level_db: Niveau cible en dB pour la normalisation (-20dB par défaut)
            compression_ratio: Ratio de compression pour limiter les pics (4:1 par défaut)
        """
        self.target_level_db = target_level_db
        self.compression_ratio = compression_ratio
        self.analysis_results = {}
    
    def load_audio(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        Charge un fichier audio.
        
        Args:
            file_path: Chemin du fichier audio
            
        Returns:
            Tuple contenant les données audio et le taux d'échantillonnage
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")
        
        audio_data, sample_rate = librosa.load(file_path, sr=None, mono=False)
        print(f"✓ Audio chargé: {file_path}")
        print(f"  - Taux d'échantillonnage: {sample_rate} Hz")
        print(f"  - Durée: {len(audio_data) / sample_rate:.2f} secondes")
        
        return audio_data, sample_rate
    
    def analyze_audio(self, audio_data: np.ndarray, sample_rate: int) -> dict:
        """
        Analyse l'audio pour déterminer les améliorations nécessaires.
        
        Args:
            audio_data: Données audio
            sample_rate: Taux d'échantillonnage
            
        Returns:
            Dictionnaire contenant les résultats de l'analyse
        """
        print("\n🔍 Analyse de l'audio en cours...")
        
        # Calculer les statistiques de niveau
        rms = np.sqrt(np.mean(audio_data**2))
        peak = np.max(np.abs(audio_data))
        
        # Calculer le niveau en dB
        rms_db = 20 * np.log10(rms) if rms > 0 else -np.inf
        peak_db = 20 * np.log10(peak) if peak > 0 else -np.inf
        
        # Calculer le dynamic range
        dynamic_range = peak_db - rms_db
        
        # Détecter les clipping
        clipping_samples = np.sum(np.abs(audio_data) >= 0.99)
        clipping_percentage = (clipping_samples / len(audio_data)) * 100
        
        # Analyser le contenu fréquentiel
        spectral_centroid = librosa.feature.spectral_centroid(y=audio_data, sr=sample_rate)[0]
        avg_spectral_centroid = np.mean(spectral_centroid)
        
        self.analysis_results = {
            'rms': rms,
            'rms_db': rms_db,
            'peak': peak,
            'peak_db': peak_db,
            'dynamic_range': dynamic_range,
            'clipping_percentage': clipping_percentage,
            'spectral_centroid': avg_spectral_centroid,
            'sample_rate': sample_rate,
            'duration': len(audio_data) / sample_rate
        }
        
        print(f"  ✓ RMS: {rms:.4f} ({rms_db:.2f} dB)")
        print(f"  ✓ Peak: {peak:.4f} ({peak_db:.2f} dB)")
        print(f"  ✓ Dynamic Range: {dynamic_range:.2f} dB")
        print(f"  ✓ Clipping: {clipping_percentage:.2f}%")
        print(f"  ✓ Centroïde spectral moyen: {avg_spectral_centroid:.2f} Hz")
        
        return self.analysis_results
    
    def normalize_audio(self, audio_data: np.ndarray) -> np.ndarray:
        """
        Normalise l'audio au niveau cible.
        
        Args:
            audio_data: Données audio
            
        Returns:
            Audio normalisé
        """
        print("\n🎚️  Normalisation de l'audio...")
        
        # Calculer le RMS actuel
        current_rms = np.sqrt(np.mean(audio_data**2))
        current_rms_db = 20 * np.log10(current_rms) if current_rms > 0 else -np.inf
        
        # Calculer le gain nécessaire
        gain_db = self.target_level_db - current_rms_db
        gain_linear = 10 ** (gain_db / 20)
        
        # Appliquer le gain
        normalized_audio = audio_data * gain_linear
        
        print(f"  ✓ Gain appliqué: {gain_db:.2f} dB")
        
        return normalized_audio
    
    def compress_audio(self, audio_data: np.ndarray, threshold_db: float = -10.0) -> np.ndarray:
        """
        Applique une compression dynamique pour réduire les variations d'amplitude.
        
        Args:
            audio_data: Données audio
            threshold_db: Seuil de compression en dB
            
        Returns:
            Audio compressé
        """
        print("\n🗜️  Compression dynamique...")
        
        # Convertir le seuil en linéaire
        threshold_linear = 10 ** (threshold_db / 20)
        
        # Appliquer la compression
        compressed_audio = np.copy(audio_data)
        mask = np.abs(audio_data) > threshold_linear
        
        # Pour les samples au-dessus du seuil, appliquer la compression
        excess = np.abs(audio_data[mask]) - threshold_linear
        compressed_excess = excess / self.compression_ratio
        compressed_audio[mask] = np.sign(audio_data[mask]) * (threshold_linear + compressed_excess)
        
        reduction_db = 20 * np.log10(np.max(np.abs(compressed_audio)) / np.max(np.abs(audio_data)))
        print(f"  ✓ Réduction des pics: {-reduction_db:.2f} dB")
        print(f"  ✓ Ratio de compression: {self.compression_ratio}:1")
        
        return compressed_audio
    
    def apply_limiter(self, audio_data: np.ndarray, ceiling: float = 0.95) -> np.ndarray:
        """
        Applique un limiteur pour éviter le clipping.
        
        Args:
            audio_data: Données audio
            ceiling: Plafond maximum (0.95 par défaut pour éviter le clipping)
            
        Returns:
            Audio limité
        """
        print("\n🚫 Application du limiteur...")
        
        limited_audio = np.clip(audio_data, -ceiling, ceiling)
        
        clipped_samples = np.sum(np.abs(audio_data) > ceiling)
        if clipped_samples > 0:
            print(f"  ✓ {clipped_samples} samples limités")
        else:
            print(f"  ✓ Aucun sample limité (audio dans les limites)")
        
        return limited_audio
    
    def enhance_audio(self, input_path: str, output_path: str) -> dict:
        """
        Améliore un fichier audio complet: analyse, normalisation, compression et limitation.
        
        Args:
            input_path: Chemin du fichier audio d'entrée
            output_path: Chemin du fichier audio de sortie
            
        Returns:
            Dictionnaire contenant les résultats de l'amélioration
        """
        print("=" * 60)
        print("🎵 Audio Enhancer - Amélioration de l'audio")
        print("=" * 60)
        
        # 1. Charger l'audio
        audio_data, sample_rate = self.load_audio(input_path)
        
        # 2. Analyser l'audio
        analysis = self.analyze_audio(audio_data, sample_rate)
        
        # 3. Améliorer l'audio
        print("\n🔧 Amélioration de l'audio...")
        
        # Normaliser
        enhanced_audio = self.normalize_audio(audio_data)
        
        # Compresser pour équilibrer les niveaux
        enhanced_audio = self.compress_audio(enhanced_audio)
        
        # Appliquer le limiteur pour éviter le clipping
        enhanced_audio = self.apply_limiter(enhanced_audio)
        
        # 4. Sauvegarder l'audio amélioré
        print(f"\n💾 Sauvegarde de l'audio amélioré...")
        sf.write(output_path, enhanced_audio, sample_rate)
        print(f"  ✓ Fichier sauvegardé: {output_path}")
        
        # 5. Analyser l'audio amélioré pour comparaison
        print("\n📊 Analyse de l'audio amélioré:")
        enhanced_analysis = self.analyze_audio(enhanced_audio, sample_rate)
        
        print("\n" + "=" * 60)
        print("✅ Amélioration terminée avec succès!")
        print("=" * 60)
        
        return {
            'original': analysis,
            'enhanced': enhanced_analysis,
            'output_file': output_path
        }


def main():
    """Fonction principale pour tester l'Audio Enhancer."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python audio_enhancer.py <input_file> <output_file>")
        print("Exemple: python audio_enhancer.py input.wav output.wav")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Créer l'enhancer avec paramètres par défaut
    enhancer = AudioEnhancer(target_level_db=-20.0, compression_ratio=4.0)
    
    # Améliorer l'audio
    results = enhancer.enhance_audio(input_file, output_file)
    
    print("\n📈 Comparaison avant/après:")
    print(f"  RMS: {results['original']['rms_db']:.2f} dB → {results['enhanced']['rms_db']:.2f} dB")
    print(f"  Peak: {results['original']['peak_db']:.2f} dB → {results['enhanced']['peak_db']:.2f} dB")
    print(f"  Dynamic Range: {results['original']['dynamic_range']:.2f} dB → {results['enhanced']['dynamic_range']:.2f} dB")


if __name__ == "__main__":
    main()
