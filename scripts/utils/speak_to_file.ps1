try {
    $text = "Merhaba, ben Tolga. Seninle tanıştığıma memnun oldun."
    $filePath = "c:\Users\Betül Büyük\Downloads\megasentito\v8\SENTIENT_OS\test_speech.wav"
    
    # Use modern SpeechSynthesizer
    $synth = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
    
    # Find Tolga
    $tolga = $synth.AllVoices | Where-Object { $_.DisplayName -like "*Tolga*" }
    if (-not $tolga) {
        "Tolga not found."
        exit 1
    }
    
    $synth.Voice = $tolga
    $stream = $synth.SynthesizeTextToStreamAsync($text).GetResults()
    
    # Save stream to file
    $fileStream = [System.IO.File]::Create($filePath)
    $stream.AsStreamForRead().CopyTo($fileStream)
    $fileStream.Close()
    
    "SUCCESS: Saved speech to $filePath"
} catch {
    "Error: $($_.Exception.Message)"
}
