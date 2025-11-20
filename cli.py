"""
Interface en ligne de commande pour Audio Enhancer
"""

import argparse
import sys
import os
from audio_enhancer import AudioEnhancer


def parse_arguments():
    """Parse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(
        description='Audio Enhancer - Améliore et normalise les fichiers audio',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  %(prog)s input.wav output.wav
  %(prog)s input.mp3 output.mp3 --target-level -18
  %(prog)s input.wav output.wav --compression-ratio 6 --target-level -16
        """
    )
    
    parser.add_argument(
        'input_file',
        help='Fichier audio d\'entrée (WAV, MP3, FLAC, etc.)'
    )
    
    parser.add_argument(
        'output_file',
        help='Fichier audio de sortie'
    )
    
    parser.add_argument(
        '-t', '--target-level',
        type=float,
        default=-20.0,
        help='Niveau cible en dB pour la normalisation (défaut: -20.0 dB)'
    )
    
    parser.add_argument(
        '-c', '--compression-ratio',
        type=float,
        default=4.0,
        help='Ratio de compression dynamique (défaut: 4.0, plage: 1.0-10.0)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Mode verbeux avec plus de détails'
    )
    
    return parser.parse_args()


def validate_inputs(args):
    """Valide les arguments d'entrée."""
    # Vérifier que le fichier d'entrée existe
    if not os.path.exists(args.input_file):
        print(f"❌ Erreur: Le fichier '{args.input_file}' n'existe pas.")
        sys.exit(1)
    
    # Vérifier que le fichier d'entrée est lisible
    if not os.path.isfile(args.input_file):
        print(f"❌ Erreur: '{args.input_file}' n'est pas un fichier valide.")
        sys.exit(1)
    
    # Vérifier les paramètres
    if args.target_level > 0:
        print(f"⚠️  Avertissement: Le niveau cible ({args.target_level} dB) est positif.")
        print("   Cela peut causer du clipping. Recommandation: utiliser une valeur négative (ex: -20 dB)")
    
    if args.compression_ratio < 1.0 or args.compression_ratio > 10.0:
        print(f"❌ Erreur: Le ratio de compression doit être entre 1.0 et 10.0")
        sys.exit(1)
    
    # Vérifier que le dossier de sortie existe
    output_dir = os.path.dirname(args.output_file)
    if output_dir and not os.path.exists(output_dir):
        print(f"❌ Erreur: Le dossier de sortie '{output_dir}' n'existe pas.")
        sys.exit(1)


def main():
    """Fonction principale du CLI."""
    args = parse_arguments()
    
    # Valider les entrées
    validate_inputs(args)
    
    try:
        # Créer l'Audio Enhancer avec les paramètres spécifiés
        enhancer = AudioEnhancer(
            target_level_db=args.target_level,
            compression_ratio=args.compression_ratio
        )
        
        # Améliorer l'audio
        results = enhancer.enhance_audio(args.input_file, args.output_file)
        
        # Afficher le résumé
        if args.verbose:
            print("\n" + "=" * 60)
            print("📊 RÉSUMÉ DÉTAILLÉ")
            print("=" * 60)
            print("\nAudio original:")
            for key, value in results['original'].items():
                if isinstance(value, float):
                    print(f"  {key}: {value:.4f}")
                else:
                    print(f"  {key}: {value}")
            
            print("\nAudio amélioré:")
            for key, value in results['enhanced'].items():
                if isinstance(value, float):
                    print(f"  {key}: {value:.4f}")
                else:
                    print(f"  {key}: {value}")
        
        print("\n✨ Audio amélioré avec succès!")
        
    except FileNotFoundError as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur lors de l'amélioration de l'audio: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
