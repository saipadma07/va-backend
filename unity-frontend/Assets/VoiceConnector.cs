using UnityEngine;
using UnityEngine.Networking;
using System.Collections;

public class VoiceConnector : MonoBehaviour
{
    public string backendUrl = "http://192.168.1.106:8000/voice-chat";
    public AvatarController avatar;

    private AudioClip clip;
    private string device;
    private bool isProcessing = false;

    void Start()
    {
        if (Microphone.devices.Length == 0)
        {
            Debug.LogError("❌ No microphone found!");
            return;
        }

        device = Microphone.devices[0];
        Debug.Log("🎤 Using mic: " + device);
    }

    // 🎤 START RECORDING
    public void StartRecording()
    {
    Debug.Log("🎤 Recording START");

    // 🔥 IMPORTANT: reset mic first
    if (Microphone.IsRecording(device))
    {
        Microphone.End(device);
    }

    clip = Microphone.Start(device, false, 10, 44100);
    }

    // 🛑 STOP RECORDING
    public void StopRecording()
    {
    Debug.Log("🛑 Recording STOP");

    if (!Microphone.IsRecording(device))
    {
        Debug.LogWarning("⚠️ Mic already stopped");
        return;
    }

    Microphone.End(device);

    byte[] wavData = WavUtility.FromAudioClip(clip);

    StartCoroutine(SendAudio(wavData));
    }

    IEnumerator SendAudio(byte[] audioBytes)
    {
    // 🚫 Prevent multiple requests
    if (isProcessing)
    {
        Debug.LogWarning("⚠️ Already processing");
        yield break;
    }

    isProcessing = true;

    yield return new WaitForSeconds(0.5f);

    WWWForm form = new WWWForm();
    form.AddBinaryData("file", audioBytes, "audio.wav", "audio/wav");

    UnityWebRequest request = UnityWebRequest.Post(backendUrl, form);

    yield return request.SendWebRequest();

    if (request.result == UnityWebRequest.Result.Success)
    {
        Debug.Log("VOICE RESPONSE: " + request.downloadHandler.text);
       avatar.HandleResponse(request.downloadHandler.text);
    }
    else
    {
        Debug.LogError("❌ Voice Error: " + request.error);
    }

    isProcessing = false; // ✅ RESET HERE
    }
}