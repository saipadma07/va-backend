using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class VisionConnector : MonoBehaviour
{
    public string backendUrl = "http://192.168.1.106:8000/analyze";

    private WebCamTexture webcam;

    void Start()
    {
        Debug.Log("🔍 Checking cameras...");

        if (WebCamTexture.devices.Length == 0)
        {
            Debug.LogError("❌ No webcam detected!");
            return;
        }

        foreach (var device in WebCamTexture.devices)
        {
            Debug.Log("📷 Found: " + device.name);
        }

        webcam = new WebCamTexture(WebCamTexture.devices[0].name);
        webcam.Play();

        Debug.Log("✅ Webcam started");
    }

    public void CaptureAndSend()
    {
        if (webcam == null || !webcam.isPlaying)
        {
            Debug.LogError("❌ Webcam not running!");
            return;
        }

        StartCoroutine(CaptureRoutine());
    }

    IEnumerator CaptureRoutine()
    {
        yield return new WaitForEndOfFrame();

        Texture2D photo = new Texture2D(webcam.width, webcam.height);
        photo.SetPixels(webcam.GetPixels());
        photo.Apply();

        byte[] imageBytes = photo.EncodeToPNG();

        WWWForm form = new WWWForm();
        form.AddBinaryData("file", imageBytes, "image.png", "image/png");

        Debug.Log("📤 Sending image...");

        UnityWebRequest request = UnityWebRequest.Post(backendUrl, form);

        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
        {
            Debug.Log("✅ Vision Response: " + request.downloadHandler.text);
        }
        else
        {
            Debug.LogError("❌ Vision Error: " + request.error);
        }
    }
}