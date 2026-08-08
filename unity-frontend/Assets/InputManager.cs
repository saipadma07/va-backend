using UnityEngine;

public class InputManager : MonoBehaviour
{
    public VoiceConnector voice;
    public VisionConnector vision;

    void Update()
    {
        // 🎤 Voice (keyboard)
        if (Input.GetKeyDown(KeyCode.Space))
        {
            voice.StartRecording();
        }

        if (Input.GetKeyUp(KeyCode.Space))
        {
            voice.StopRecording();
        }

        // 👁 Vision (keyboard)
        if (Input.GetKeyDown(KeyCode.V))
        {
            vision.CaptureAndSend();
        }

        // 🤖 BOTH (keyboard)
        if (Input.GetKeyDown(KeyCode.B))
        {
            voice.StartRecording();
            vision.CaptureAndSend();
        }

        if (Input.GetKeyUp(KeyCode.B))
        {
            voice.StopRecording();
        }
    }

    // ============================
    // 🔘 BUTTON FUNCTIONS
    // ============================

    // 🎤 Voice button
    public void StartVoiceFromButton()
    {
        Debug.Log("🎤 Voice Button Pressed");
        voice.StartRecording();
    }

    public void StopVoiceFromButton()
    {
        Debug.Log("🛑 Voice Button Released");
        voice.StopRecording();
    }

    // 👁 Vision button
    public void StartVisionFromButton()
    {
        Debug.Log("👁 Vision Button Pressed");
        vision.CaptureAndSend();
    }

    // 🤖 Smart Mode (Both)
    public void StartBothFromButton()
    {
        Debug.Log("🤖 Smart Mode Button Pressed");
        voice.StartRecording();
        vision.CaptureAndSend();
    }

    public void StopBothFromButton()
    {
        Debug.Log("🛑 Smart Mode Released");
        voice.StopRecording();
    }
}