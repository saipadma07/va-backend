using UnityEngine;
using Live2D.Cubism.Core;

public class AutoIdleMovement : MonoBehaviour
{
    public CubismModel model;

    private CubismParameter angleX;
    private CubismParameter angleY;
    private CubismParameter bodyAngleX;

    void Start()
    {
        if (model == null)
            model = GetComponent<CubismModel>();

        foreach (var param in model.Parameters)
        {
            if (param.Id == "ParamAngleX")
                angleX = param;

            if (param.Id == "ParamAngleY")
                angleY = param;

            if (param.Id == "ParamBodyAngleX")
                bodyAngleX = param;
        }
    }

    void Update()
    {
        float time = Time.time;

        if (angleX != null)
            angleX.Value = Mathf.Sin(time * 0.5f) * 10f;

        if (angleY != null)
            angleY.Value = Mathf.Sin(time * 0.3f) * 5f;

        if (bodyAngleX != null)
            bodyAngleX.Value = Mathf.Sin(time * 0.4f) * 8f;

    }
}
