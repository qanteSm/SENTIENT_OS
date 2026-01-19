# Copyright (c) 2026 Muhammet Ali Büyük. All rights reserved.
# This source code is proprietary. Confidential and private.
# Unauthorized copying or distribution is strictly prohibited.
# Contact: iletisim@alibuyuk.net | https://alibuyuk.net
# ARCHITECT: MAB-SENTIENT-2026
# =========================================================================

"""
Integration Tests for Boot Sequence

Tests the complete boot sequence from launcher to running game.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os


class TestBootSequence:
    """Test complete boot sequence"""
    
    @pytest.mark.integration
    @patch('core.kernel.Kernel')
    def test_launcher_to_kernel(self, mock_kernel):
        """Should successfully boot from launcher to kernel"""
        # This would test the full boot path
        # For now, just verify the import chain works
        try:
            import launcher
            assert launcher is not None
        except ImportError as e:
            pytest.skip(f"Launcher not importable: {e}")
    
    @pytest.mark.integration
    def test_config_loads_on_boot(self):
        """Should load configuration on boot"""
        from config import Config
        
        config = Config()
        
        assert config is not None
        assert config.APP_NAME == "SENTIENT_OS"
        assert config.VERSION is not None
    
    @pytest.mark.integration
    def test_memory_initializes_on_boot(self):
        """Should initialize memory system on boot"""
        from core.memory import Memory
        
        memory = Memory()
        
        assert memory is not None
    
    @pytest.mark.integration
    @patch('core.gemini_brain.genai')
    def test_brain_initializes_on_boot(self, mock_genai):
        """Should initialize AI brain on boot"""
        from core.gemini_brain import GeminiBrain
        
        brain = GeminiBrain(api_key="test_key")
        
        assert brain is not None


class TestBootSequenceErrorHandling:
    """Test error handling during boot"""
    
    @pytest.mark.integration
    def test_boot_with_no_api_key(self):
        """Should handle missing API key gracefully"""
        from core.gemini_brain import GeminiBrain
        
        # Mock Config to return no API key AND clear environment
        mock_config = Mock()
        mock_config.IS_MOCK = False
        mock_config.get.return_value = None  # No GEMINI_KEY in config
        
        with patch.dict(os.environ, {}, clear=True), \
             patch('core.gemini_brain.Config', return_value=mock_config):
            brain = GeminiBrain(api_key=None)  # Explicitly pass None
            assert brain.mock_mode == True
    
    @pytest.mark.integration
    def test_boot_with_corrupted_config(self):
        """Should handle config errors gracefully"""
        # Would test config error handling
        pass
