import pytest
import os
import sys
from unittest.mock import MagicMock, patch

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../SENTIENT_OS")))

from core.dynamic_difficulty import DynamicDifficulty
from core.streamer_mode import StreamerMode
from core.file_awareness import FileSystemAwareness
from core.privacy_filter import PrivacyFilter

class TestPhase3Features:
    
    @pytest.fixture
    def mock_mem_story(self):
        memory = MagicMock()
        memory.data = {"user_profile": {"behavior_stats": {"swear_count": 0}}}
        story_manager = MagicMock()
        story_manager.ambient_horror = MagicMock()
        return memory, story_manager

    def test_dynamic_difficulty_scaling(self, mock_mem_story):
        memory, story = mock_mem_story
        diff = DynamicDifficulty(memory, story)
        
        # Test low skill (slow typing)
        diff.report_typing(10, 60) # 2 WPM
        diff._recalculate_difficulty()
        # Low skill/defiance should lead to high fear_score and high target intensity (to provoke/scare)
        assert diff.skill_score < 50
        # Check if intensity was set
        assert story.ambient_horror.set_intensity.called

    def test_streamer_mode_aliasing(self):
        sm = StreamerMode.singleton()
        sm.enabled = True
        
        name = "MySecrets"
        alias1 = sm.get_alias(name)
        alias2 = sm.get_alias(name)
        
        assert alias1 != name
        assert alias1 == alias2 # Must be deterministic
        assert "_" in alias1 # Format check

    def test_file_awareness_scoring(self):
        score_pas = FileSystemAwareness.score_file("passwords.txt")
        score_fam = FileSystemAwareness.score_file("family_photo.jpg")
        score_ran = FileSystemAwareness.score_file("notes.txt")
        
        assert score_pas >= 90
        assert score_fam >= 60
        assert score_ran >= 30
        assert FileSystemAwareness.score_file("random.bin") == 0

    def test_privacy_filter_enhanced(self):
        pf = PrivacyFilter.singleton()
        with patch.object(pf, 'username', 'Betul'):
            input_text = "C:\\Users\\Betul\\Desktop\\Secret.txt and %APPDATA%"
            scrubbed = pf.scrub(input_text)
            
            assert "Betul" not in scrubbed
            assert "%APPDATA%" not in scrubbed
            assert "<ENV_VAR>" in scrubbed or "<USER_DIR>" in scrubbed

    def test_streamer_mode_path_masking(self):
        sm = StreamerMode.singleton()
        sm.enabled = True
        path = "C:/Users/Betul/Documents/Secret"
        masked = sm.mask_path(path)
        
        assert "Betul" not in masked
        assert "Documents" not in masked
        assert "/" in masked
