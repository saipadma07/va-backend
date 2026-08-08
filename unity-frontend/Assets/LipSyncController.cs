using UnityEngine;
using Live2D.Cubism.Core;

public class LipSyncController : MonoBehaviour
{
    public AudioSource audioSource;
    private CubismParameter mouthParam;

    public float sensitivity = 500f;

    void Start()
    {
        var parameters = GetComponentsInChildren<CubismParameter>();

        foreach (var p in parameters)
        {
            if (p.Id.Contains("MouthOpenY"))
            {
                mouthParam = p;
                Debug.Log("✅ Mouth Found: " + p.Id);
                break;
            }
        }
    }

    void LateUpdate() // 🔥 IMPORTANT
    {
        if (audioSource == null || mouthParam == null)
            return;

        if (!audioSource.isPlaying)
        {
            mouthParam.Value = 0f;
            return;
        }

        float[] samples = new float[256];
        audioSource.GetOutputData(samples, 0);

        float volume = 0f;
        foreach (float s in samples)
            volume += Mathf.Abs(s);

        volume /= samples.Length;

        float target = Mathf.Clamp01(volume * sensitivity);

        // 🔥 FORCE override AFTER everything else
        mouthParam.Value = target;

        Debug.Log("Volume: " + volume + " → " + target);
    }
}