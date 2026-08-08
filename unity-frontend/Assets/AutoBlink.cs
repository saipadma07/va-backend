using UnityEngine;
using Live2D.Cubism.Framework;

public class AutoBlink : MonoBehaviour
{
    public CubismEyeBlinkController eyeBlinkController;

    public float blinkInterval = 3f;
    private float timer = 0f;
    private bool isBlinking = false;

    void Update()
    {
        if (eyeBlinkController == null)
            return;

        timer += Time.deltaTime;

        if (!isBlinking && timer >= blinkInterval)
        {
            StartCoroutine(Blink());
            timer = 0f;
        }
    }

    System.Collections.IEnumerator Blink()
    {
        isBlinking = true;

        eyeBlinkController.EyeOpening = 0f; // Close eyes
        yield return new WaitForSeconds(0.1f);

        eyeBlinkController.EyeOpening = 1f; // Open eyes
        isBlinking = false;
    }
}
