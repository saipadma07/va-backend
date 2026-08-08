using UnityEngine;
using Live2D.Cubism.Core;

public class SimpleBreathing : MonoBehaviour
{
    public CubismModel Model;
    public float BreathingSpeed = 2f;
    public float BreathingAmount = 0.3f;

    private CubismParameter bodyAngleY;
    private CubismParameter breathParam;

    void Start()
    {
        if (Model == null) return;

        var parameters = Model.Parameters;

        foreach (var p in parameters)
        {
            if (p.Id == "ParamBodyAngleY")
                bodyAngleY = p;

            if (p.Id == "ParamBreath")
                breathParam = p;
        }
    }

    void LateUpdate()
    {
        if (Model == null) return;

        float breathe = Mathf.Sin(Time.time * BreathingSpeed) * BreathingAmount;

        if (bodyAngleY != null)
            bodyAngleY.Value = breathe * 10f;

        if (breathParam != null)
            breathParam.Value = breathe;
    }
}
