#!/usr/bin/env python3
"""
Evolance AI Production Deployment Script
Handles model loading, initialization, and production setup
"""

import os
import sys
import time
import logging
import argparse
from pathlib import Path
import subprocess
import json

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_core.config import config
from ai_core.semantic_network import CoreSemanticNetwork
from ai_core.emotion_detector import EmotionDetector
from ai_core.memory_manager import MemoryManager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('evolance_ai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EvolanceAIDeployer:
    """Handles deployment and initialization of Evolance AI system"""
    
    def __init__(self, production_mode: bool = False):
        self.production_mode = production_mode
        self.models_loaded = False
        self.services_started = False
        
        # Create necessary directories
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories for the AI system"""
        directories = [
            "data/memory",
            "data/models",
            "data/logs",
            "data/cache",
            "data/embeddings"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
    
    def check_dependencies(self) -> bool:
        """Check if all required dependencies are installed"""
        logger.info("Checking dependencies...")
        
        required_packages = [
            "torch", "transformers", "sentence_transformers",
            "chromadb", "networkx", "numpy", "fastapi"
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                logger.info(f"✓ {package} is available")
            except ImportError:
                missing_packages.append(package)
                logger.error(f"✗ {package} is missing")
        
        if missing_packages:
            logger.error(f"Missing packages: {missing_packages}")
            logger.info("Install missing packages with: pip install -r requirements_ai.txt")
            return False
        
        logger.info("All dependencies are available")
        return True
    
    def download_models(self):
        """Download required AI models"""
        logger.info("Downloading AI models...")
        
        models_to_download = [
            {
                "name": "emotion-classifier",
                "model": "j-hartmann/emotion-english-distilroberta-base",
                "type": "transformers"
            },
            {
                "name": "sentiment-analyzer",
                "model": "cardiffnlp/twitter-roberta-base-sentiment-latest",
                "type": "transformers"
            },
            {
                "name": "sentence-embeddings",
                "model": "sentence-transformers/all-MiniLM-L6-v2",
                "type": "sentence_transformers"
            }
        ]
        
        for model_info in models_to_download:
            try:
                logger.info(f"Downloading {model_info['name']}...")
                
                if model_info["type"] == "transformers":
                    from transformers import AutoTokenizer, AutoModelForSequenceClassification
                    
                    tokenizer = AutoTokenizer.from_pretrained(model_info["model"])
                    model = AutoModelForSequenceClassification.from_pretrained(model_info["model"])
                    
                    # Save to local directory
                    model_path = f"data/models/{model_info['name']}"
                    tokenizer.save_pretrained(model_path)
                    model.save_pretrained(model_path)
                    
                elif model_info["type"] == "sentence_transformers":
                    from sentence_transformers import SentenceTransformer
                    
                    model = SentenceTransformer(model_info["model"])
                    model_path = f"data/models/{model_info['name']}"
                    model.save(model_path)
                
                logger.info(f"✓ Downloaded {model_info['name']}")
                
            except Exception as e:
                logger.error(f"✗ Failed to download {model_info['name']}: {e}")
                if self.production_mode:
                    raise
    
    def initialize_core_system(self):
        """Initialize the core AI system components"""
        logger.info("Initializing core AI system...")
        
        try:
            # Initialize core semantic network
            logger.info("Loading core semantic network...")
            core_network = CoreSemanticNetwork()
            logger.info(f"✓ Core network loaded with {len(core_network.emotion_nodes)} emotions")
            
            # Initialize emotion detector
            logger.info("Loading emotion detector...")
            emotion_detector = EmotionDetector()
            logger.info("✓ Emotion detector initialized")
            
            # Test emotion detection
            test_text = "I'm feeling really happy today!"
            result = emotion_detector.detect_emotions(test_text)
            logger.info(f"✓ Emotion detection test: {result.primary_emotion} ({result.confidence:.2f})")
            
            self.models_loaded = True
            logger.info("✓ Core AI system initialized successfully")
            
        except Exception as e:
            logger.error(f"✗ Failed to initialize core system: {e}")
            if self.production_mode:
                raise
    
    def setup_database(self):
        """Setup and initialize databases"""
        logger.info("Setting up databases...")
        
        try:
            # Initialize ChromaDB
            import chromadb
            from chromadb.config import Settings
            
            client = chromadb.PersistentClient(
                path="./data/memory",
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Test collection creation
            test_collection = client.create_collection(
                name="test_collection",
                metadata={"test": True}
            )
            
            # Clean up test collection
            client.delete_collection("test_collection")
            
            logger.info("✓ ChromaDB initialized successfully")
            
        except Exception as e:
            logger.error(f"✗ Failed to setup ChromaDB: {e}")
            if self.production_mode:
                raise
    
    def run_health_check(self) -> bool:
        """Run comprehensive health check"""
        logger.info("Running health check...")
        
        checks_passed = 0
        total_checks = 4
        
        # Check 1: Core network
        try:
            from ai_core.semantic_network import core_network
            emotions = core_network.get_emotion_info("joy")
            if emotions:
                logger.info("✓ Core semantic network: OK")
                checks_passed += 1
            else:
                logger.error("✗ Core semantic network: FAILED")
        except Exception as e:
            logger.error(f"✗ Core semantic network: ERROR - {e}")
        
        # Check 2: Emotion detection
        try:
            from ai_core.emotion_detector import emotion_detector
            result = emotion_detector.detect_emotions("I am happy")
            if result.primary_emotion:
                logger.info("✓ Emotion detection: OK")
                checks_passed += 1
            else:
                logger.error("✗ Emotion detection: FAILED")
        except Exception as e:
            logger.error(f"✗ Emotion detection: ERROR - {e}")
        
        # Check 3: Memory management
        try:
            memory_manager = MemoryManager("test_user")
            context = memory_manager.get_memory_context("test message", None)
            logger.info("✓ Memory management: OK")
            checks_passed += 1
        except Exception as e:
            logger.error(f"✗ Memory management: ERROR - {e}")
        
        # Check 4: Configuration
        try:
            if config.validate():
                logger.info("✓ Configuration: OK")
                checks_passed += 1
            else:
                logger.error("✗ Configuration: FAILED")
        except Exception as e:
            logger.error(f"✗ Configuration: ERROR - {e}")
        
        logger.info(f"Health check results: {checks_passed}/{total_checks} passed")
        
        if checks_passed == total_checks:
            logger.info("✓ All health checks passed")
            return True
        else:
            logger.error("✗ Some health checks failed")
            return False
    
    def start_services(self):
        """Start production services"""
        logger.info("Starting production services...")
        
        try:
            # Start FastAPI server
            logger.info("Starting FastAPI server...")
            subprocess.Popen([
                "uvicorn", "server:app",
                "--host", "0.0.0.0",
                "--port", "8001",
                "--workers", "4" if self.production_mode else "1"
            ])
            
            # Start Redis if needed
            if config.scaling.enable_redis_cache:
                logger.info("Starting Redis cache...")
                # This would start Redis server
                pass
            
            self.services_started = True
            logger.info("✓ Production services started")
            
        except Exception as e:
            logger.error(f"✗ Failed to start services: {e}")
            if self.production_mode:
                raise
    
    def deploy(self):
        """Complete deployment process"""
        logger.info("Starting Evolance AI deployment...")
        
        # Step 1: Check dependencies
        if not self.check_dependencies():
            logger.error("Deployment failed: Missing dependencies")
            return False
        
        # Step 2: Download models
        self.download_models()
        
        # Step 3: Initialize core system
        self.initialize_core_system()
        
        # Step 4: Setup database
        self.setup_database()
        
        # Step 5: Health check
        if not self.run_health_check():
            logger.error("Deployment failed: Health check failed")
            return False
        
        # Step 6: Start services (if production)
        if self.production_mode:
            self.start_services()
        
        logger.info("✓ Evolance AI deployment completed successfully")
        return True
    
    def generate_config(self):
        """Generate production configuration"""
        logger.info("Generating production configuration...")
        
        config_data = {
            "model": {
                "model_size": "7B",
                "max_context_length": 8192,
                "temperature": 0.7
            },
            "memory": {
                "vector_db_type": "chromadb",
                "similarity_threshold": 0.75
            },
            "privacy": {
                "encryption_enabled": True,
                "anonymize_personal_data": True
            },
            "scaling": {
                "enable_load_balancing": True,
                "max_concurrent_users": 10000
            }
        }
        
        config_path = "evolance_config.json"
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        logger.info(f"✓ Configuration saved to {config_path}")

def main():
    parser = argparse.ArgumentParser(description="Evolance AI Deployment Script")
    parser.add_argument("--production", action="store_true", help="Deploy in production mode")
    parser.add_argument("--check-only", action="store_true", help="Only run health check")
    parser.add_argument("--download-models", action="store_true", help="Only download models")
    parser.add_argument("--generate-config", action="store_true", help="Generate configuration")
    
    args = parser.parse_args()
    
    deployer = EvolanceAIDeployer(production_mode=args.production)
    
    if args.check_only:
        success = deployer.run_health_check()
        sys.exit(0 if success else 1)
    
    elif args.download_models:
        deployer.download_models()
        sys.exit(0)
    
    elif args.generate_config:
        deployer.generate_config()
        sys.exit(0)
    
    else:
        success = deployer.deploy()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 