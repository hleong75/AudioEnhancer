"""
Tests unitaires pour le module audio_enhancer
"""

import unittest
import numpy as np
import tempfile
import os
import soundfile as sf
from audio_enhancer import AudioEnhancer


class TestAudioEnhancer(unittest.TestCase):
    """Tests pour la classe AudioEnhancer"""
    
    def setUp(self):
        """Prépare les tests"""
        self.enhancer = AudioEnhancer(target_level_db=-20.0, compression_ratio=4.0)
        self.sample_rate = 44100
        self.duration = 2.0  # secondes
        
    def create_test_audio(self, amplitude=0.5, frequency=440):
        """Crée un fichier audio de test (sine wave)"""
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration))
        audio_data = amplitude * np.sin(2 * np.pi * frequency * t)
        return audio_data.astype(np.float32)
    
    def test_initialization(self):
        """Test de l'initialisation de l'enhancer"""
        self.assertEqual(self.enhancer.target_level_db, -20.0)
        self.assertEqual(self.enhancer.compression_ratio, 4.0)
        self.assertEqual(self.enhancer.analysis_results, {})
    
    def test_analyze_audio(self):
        """Test de l'analyse audio"""
        audio_data = self.create_test_audio(amplitude=0.5)
        results = self.enhancer.analyze_audio(audio_data, self.sample_rate)
        
        # Vérifier que les résultats contiennent les clés attendues
        self.assertIn('rms', results)
        self.assertIn('rms_db', results)
        self.assertIn('peak', results)
        self.assertIn('peak_db', results)
        self.assertIn('dynamic_range', results)
        self.assertIn('clipping_percentage', results)
        
        # Vérifier que les valeurs sont cohérentes
        self.assertGreater(results['rms'], 0)
        self.assertGreater(results['peak'], 0)
        self.assertLessEqual(results['peak'], 1.0)
    
    def test_normalize_audio(self):
        """Test de la normalisation"""
        audio_data = self.create_test_audio(amplitude=0.1)  # Audio très faible
        normalized = self.enhancer.normalize_audio(audio_data)
        
        # L'audio normalisé devrait avoir un RMS plus élevé
        original_rms = np.sqrt(np.mean(audio_data**2))
        normalized_rms = np.sqrt(np.mean(normalized**2))
        self.assertGreater(normalized_rms, original_rms)
    
    def test_compress_audio(self):
        """Test de la compression dynamique"""
        # Créer un audio avec des pics élevés
        audio_data = self.create_test_audio(amplitude=0.8)
        compressed = self.enhancer.compress_audio(audio_data, threshold_db=-10.0)
        
        # La compression devrait réduire les pics
        original_peak = np.max(np.abs(audio_data))
        compressed_peak = np.max(np.abs(compressed))
        self.assertLessEqual(compressed_peak, original_peak)
    
    def test_apply_limiter(self):
        """Test du limiteur"""
        # Créer un audio qui dépasse le ceiling
        audio_data = np.array([0.5, 0.8, 1.0, 0.99, -0.98])
        limited = self.enhancer.apply_limiter(audio_data, ceiling=0.95)
        
        # Vérifier que tous les samples sont dans les limites
        self.assertLessEqual(np.max(limited), 0.95)
        self.assertGreaterEqual(np.min(limited), -0.95)
    
    def test_enhance_audio_workflow(self):
        """Test du workflow complet d'amélioration"""
        # Créer un fichier audio temporaire
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_input:
            input_path = tmp_input.name
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_output:
            output_path = tmp_output.name
        
        try:
            # Créer et sauvegarder un audio de test
            audio_data = self.create_test_audio(amplitude=0.3)
            sf.write(input_path, audio_data, self.sample_rate)
            
            # Améliorer l'audio
            results = self.enhancer.enhance_audio(input_path, output_path)
            
            # Vérifier que le fichier de sortie existe
            self.assertTrue(os.path.exists(output_path))
            
            # Vérifier que les résultats contiennent les analyses
            self.assertIn('original', results)
            self.assertIn('enhanced', results)
            self.assertIn('output_file', results)
            
            # Charger l'audio amélioré et vérifier qu'il n'est pas vide
            enhanced_audio, sr = sf.read(output_path)
            self.assertEqual(len(enhanced_audio), len(audio_data))
            self.assertEqual(sr, self.sample_rate)
            
        finally:
            # Nettoyer les fichiers temporaires
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)
    
    def test_load_audio_file_not_found(self):
        """Test de chargement d'un fichier inexistant"""
        with self.assertRaises(FileNotFoundError):
            self.enhancer.load_audio('nonexistent_file.wav')
    
    def test_compression_ratio_effect(self):
        """Test de l'effet du ratio de compression"""
        audio_data = self.create_test_audio(amplitude=0.8)
        
        # Compression douce (ratio faible)
        enhancer_soft = AudioEnhancer(compression_ratio=2.0)
        compressed_soft = enhancer_soft.compress_audio(audio_data)
        
        # Compression forte (ratio élevé)
        enhancer_hard = AudioEnhancer(compression_ratio=8.0)
        compressed_hard = enhancer_hard.compress_audio(audio_data)
        
        # La compression forte devrait réduire davantage les pics
        peak_soft = np.max(np.abs(compressed_soft))
        peak_hard = np.max(np.abs(compressed_hard))
        self.assertLess(peak_hard, peak_soft)


if __name__ == '__main__':
    unittest.main()
