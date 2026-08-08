using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using TMPro;
using System.Collections.Generic;

[System.Serializable]
public class AIResponse
{
    public string description;
    public string answer;
    public string audio;
}

public class AvatarController : MonoBehaviour
{
    public AudioSource audioSource;
    public TextMeshProUGUI textUI;

    private Coroutine subtitleRoutine;

    // ============================
    // 🧠 HANDLE RESPONSE
    // ============================
    public void HandleResponse(string json)
    {
        StopAllCoroutines();
        audioSource.Stop();

        AIResponse res = JsonUtility.FromJson<AIResponse>(json);

        if (!string.IsNullOrEmpty(res.audio))
        {
            StartCoroutine(PlayAudio("http://192.168.1.106:8000" + res.audio, res.answer));
        }
        else if (!string.IsNullOrEmpty(res.answer))
        {
            StartSubtitles(res.answer, 5f);
        }
    }

    // ============================
    // 🔊 AUDIO
    // ============================
    IEnumerator PlayAudio(string url, string subtitleText)
    {
        UnityWebRequest www = UnityWebRequestMultimedia.GetAudioClip(url, AudioType.MPEG);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.LogError("Audio error: " + www.error);
            yield break;
        }

        AudioClip clip = DownloadHandlerAudioClip.GetContent(www);

        Debug.Log("Audio Length: " + clip.length);

        audioSource.clip = clip;
        audioSource.Play();

        if (!string.IsNullOrEmpty(subtitleText))
        {
            StartSubtitles(subtitleText, clip.length);
        }
    }

    // ============================
    // 🎤 SUBTITLES
    // ============================
    void StartSubtitles(string fullText, float duration)
    {
        if (subtitleRoutine != null)
            StopCoroutine(subtitleRoutine);

        subtitleRoutine = StartCoroutine(TypeSubtitles(fullText, duration));
    }

    IEnumerator TypeSubtitles(string text, float duration)
    {
        textUI.text = "";

        string[] words = text.Split(' ');
        float delay = duration / Mathf.Max(words.Length, 1);

        string currentText = "";

        int maxWordsPerLine = 8;
        int maxLines = 3;

        List<string> lines = new List<string>();

        for (int i = 0; i < words.Length; i++)
        {
            currentText += words[i] + " ";

            if ((i + 1) % maxWordsPerLine == 0)
            {
                lines.Add(currentText);
                currentText = "";

                if (lines.Count > maxLines)
                    lines.RemoveAt(0);

                textUI.text = string.Join("\n", lines);
            }

            yield return new WaitForSeconds(delay);
        }

        if (!string.IsNullOrEmpty(currentText))
        {
            lines.Add(currentText);

            if (lines.Count > maxLines)
                lines.RemoveAt(0);

            textUI.text = string.Join("\n", lines);
        }

        yield return new WaitForSeconds(1f);
        textUI.text = "";
    }
}