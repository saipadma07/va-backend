using UnityEngine;
using Live2D.Cubism.Core;
using Live2D.Cubism.Framework;

public class MouseHeadFollow : MonoBehaviour, ICubismUpdatable
{
    private CubismModel model;

    private CubismParameter angleX;
    private CubismParameter angleY;
    private CubismParameter bodyAngleX;
    private CubismParameter eyeBallX;
    private CubismParameter eyeBallY;

    private Vector2 dragStartPos;
    private bool isDragging = false;

    private float currentX = 0f;
    private float currentY = 0f;

    private float velocityX = 0f;
    private float velocityY = 0f;

    public int ExecutionOrder => 10000;
    public bool NeedsUpdateOnEditing => false;
    public bool HasUpdateController { get; set; }

    void Start()
    {
        model = GetComponent<CubismModel>();

        angleX = model.Parameters.FindById("ParamAngleX");
        angleY = model.Parameters.FindById("ParamAngleY");
        bodyAngleX = model.Parameters.FindById("ParamBodyAngleX");
        eyeBallX = model.Parameters.FindById("ParamEyeBallX");
        eyeBallY = model.Parameters.FindById("ParamEyeBallY");
    }

    public void OnLateUpdate()
    {
        if (model == null) return;

        if (Input.GetMouseButtonDown(0))
        {
            dragStartPos = Input.mousePosition;
            isDragging = true;
        }

        if (Input.GetMouseButtonUp(0))
        {
            isDragging = false;

            // Add extra momentum when released
            velocityX *= 2.5f;
            velocityY *= 2.5f;
        }

        if (isDragging)
        {
            Vector2 currentPos = Input.mousePosition;
            Vector2 delta = currentPos - dragStartPos;

            float offsetX = Mathf.Clamp(delta.x / 180f, -1f, 1f);
            float offsetY = Mathf.Clamp(delta.y / 180f, -1f, 1f);

            ApplyMovement(offsetX, offsetY);
        }
        else
        {
            ApplyMovement(0f, 0f);
        }
    }

    private void ApplyMovement(float offsetX, float offsetY)
    {
        float targetX = offsetX * 50f;
        float targetY = offsetY * 50f;

        currentX = Mathf.SmoothDamp(currentX, targetX, ref velocityX, 0.18f);
        currentY = Mathf.SmoothDamp(currentY, targetY, ref velocityY, 0.18f);

        if (angleX != null)
            angleX.Value = currentX;

        if (angleY != null)
            angleY.Value = currentY;

        if (bodyAngleX != null)
            bodyAngleX.Value = currentX * 0.6f;

        if (eyeBallX != null)
            eyeBallX.Value = currentX / 25f;

        if (eyeBallY != null)
            eyeBallY.Value = currentY / 25f;
    }
}
