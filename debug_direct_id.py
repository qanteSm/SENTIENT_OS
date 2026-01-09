import win32com.client

try:
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    # THE EXPERIMENT: Use the full registry path of a OneCore voice as an ID
    onecore_id = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens\MSTTS_V110_trTR_Tolga"
    
    print(f"Attempting to set voice to: {onecore_id}")
    try:
        # Try to find voice by full ID
        v = speaker.GetVoices(f"Id={onecore_id}")
        if v.Count > 0:
            print("SUCCESS: Found voice by direct OneCore ID!")
            speaker.Voice = v.Item(0)
            speaker.Speak("Merhaba, ben Tolga. Seninle konuşabiliyorum!")
        else:
            print("Direct ID search returned 0 voices.")
    except Exception as e:
        print(f"Direct ID error: {e}")

except Exception as e:
    print(f"SAPI error: {e}")
