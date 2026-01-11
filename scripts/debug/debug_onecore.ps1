try {
    # Load required types
    $null = [Windows.Media.SpeechSynthesis.SpeechSynthesizer, Windows.Media, ContentType=WindowsRuntime]
    $synth = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
    
    # List voices to confirm
    $voices = $synth.AllVoices
    "--- ALL VOICES ---"
    foreach ($v in $voices) {
        "$($v.DisplayName) (Lang: $($v.Language))"
    }
    
    # Try to find Tolga
    $tolga = $voices | Where-Object { $_.DisplayName -like "*Tolga*" }
    if ($tolga) {
        "Found Tolga: $($tolga.DisplayName)"
        $synth.Voice = $tolga
        
        # Test speak (requires a media player or saving to file)
        # For a quick test, we'll just confirm he's selectable.
        "Tolga selected successfully."
    } else {
        "Tolga NOT found in OneCore voices."
    }
} catch {
    "Error: $($_.Exception.Message)"
}
