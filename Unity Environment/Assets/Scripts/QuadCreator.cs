using UnityEngine;
using System.IO;

public class QuadCreator : MonoBehaviour
{
    public float width = 1;
    public float height = 1;
    public string name = "";
    //enum Cubeside { BOTTOM, TOP, LEFT, RIGHT, FRONT, BACK };

    public void Start()
    {
        Block new_b = new Block();
        new_b.CreateQuad("bottom", width, height, name);
        new_b.CreateQuad("left", width, height, name);
        new_b.CreateQuad("right", width, height, name);
        new_b.CreateQuad("top", width, height, name);
        new_b.CreateQuad("center", width, height, name);
    }
}

public class Block
{
    public void CreateQuad(string side, float width, float height, string name)
    {
        //MeshRenderer meshRenderer = gameObject.AddComponent<MeshRenderer>();
        //meshRenderer.sharedMaterial = new Material(Shader.Find("Standard"));

        //MeshFilter meshFilter = gameObject.AddComponent<MeshFilter>();

        Mesh mesh = new Mesh();

        Vector3 p0 = new Vector3(0, 0, 0);
        Vector3 p1 = new Vector3(width, 0, 0);
        Vector3 p2 = new Vector3(0, 0, height);
        Vector3 p3 = new Vector3(width, 0, height);
        Vector3 p4 = new Vector3(width, width, 0);
        Vector3 p5 = new Vector3(width, width, height);
        Vector3 p6 = new Vector3(0, width, 0);
        Vector3 p7 = new Vector3(0, width, height);

        Vector2 uv00 = new Vector2(0, 0);
        Vector2 uv01 = new Vector2(0, 1);
        Vector2 uv10 = new Vector2(1, 0);
        Vector2 uv11 = new Vector2(1, 1);

        Vector3[] vertices = new Vector3[4];
        Vector3[] normals = new Vector3[4];
        Vector2[] uv = new Vector2[4];

        switch (side)
        {
            case "bottom":
                vertices = new Vector3[] { p0, p1, p2, p3 };
                normals = new Vector3[] {-Vector3.up, -Vector3.up,
                                            -Vector3.up, -Vector3.up};
                //triangles = new int[] { 3, 1, 0, 3, 2, 1 };
                uv = new Vector2[] { uv11, uv01, uv10, uv00 };

                break;
            case "left":
                vertices = new Vector3[] { p3, p1, p5, p4};
                normals = new Vector3[] {Vector3.left, Vector3.left,
                                            Vector3.left, Vector3.left};
                //triangles = new int[] { 3, 1, 0, 3, 2, 1 };
                uv = new Vector2[] { uv00, uv10, uv01, uv11 };
                break;
            case "right":
                vertices = new Vector3[] { p0, p2, p6, p7 };
                normals = new Vector3[] {Vector3.right, Vector3.right,
                                            Vector3.right, Vector3.right};
                //triangles = new int[] { 3, 1, 0, 3, 2, 1 };
                uv = new Vector2[] { uv00, uv10, uv01, uv11 };
                break;
            case "top":
                vertices = new Vector3[] { p7, p5, p6, p4};
                normals = new Vector3[] {Vector3.down, Vector3.down,
                                            Vector3.down, Vector3.down};
                //triangles = new int[] { 3, 1, 0, 3, 2, 1 };
                uv = new Vector2[] { uv11, uv01, uv10, uv00 };
                break;
            case "center":
                vertices = new Vector3[] { p6, p4, p0, p1 };
                normals = new Vector3[] {Vector3.forward, Vector3.forward,
                                            Vector3.forward, Vector3.forward};
                //triangles = new int[] { 3, 1, 0, 3, 2, 1 };
                uv = new Vector2[] { uv11, uv01, uv10, uv00 };
                break;
        }

        int[] tris = new int[6]
        {
            // lower left triangle
            0, 2, 1,
            // upper right triangle
            2, 3, 1
        };

        mesh.vertices = vertices;
        mesh.triangles = tris;
        mesh.normals = normals;
        mesh.uv = uv;

        GameObject quad = new GameObject(side);

        MeshRenderer meshRenderer = quad.gameObject.AddComponent<MeshRenderer>();
        meshRenderer.sharedMaterial = new Material(Shader.Find("Standard"));

        MeshFilter meshFilter = quad.gameObject.AddComponent<MeshFilter>();

        meshFilter.mesh = mesh;

        Texture2D tex = null;
        byte[] fileData;
        string filepath = "";
        switch (side)
        {
            case "bottom":
                filepath = "C:/Users/REO_Razr_Blade/PycharmProjects/2DtoVR/tour_results/" + name + "/bottom_face.jpg";
                break;
            case "top":
                filepath = "C:/Users/REO_Razr_Blade/PycharmProjects/2DtoVR/tour_results/" + name + "/top_face.jpg";
                break;
            case "left":
                filepath = "C:/Users/REO_Razr_Blade/PycharmProjects/2DtoVR/tour_results/" + name + "/left_face.jpg";
                break;
            case "right":
                filepath = "C:/Users/REO_Razr_Blade/PycharmProjects/2DtoVR/tour_results/" + name + "/right_face.jpg";
                break;
            case "center":
                filepath = "C:/Users/REO_Razr_Blade/PycharmProjects/2DtoVR/tour_results/" + name + "/center_face.jpg";
                break;
        }

        Texture2D texture = LoadImage(filepath);
        quad.GetComponent<Renderer>().material.mainTexture = texture;

        var mc = quad.gameObject.AddComponent<MeshCollider>();

        mc.convex = true;




    }

    public static Texture2D LoadImage(string filePath)
    {

        Texture2D tex = null;
        byte[] fileData;

        if (File.Exists(filePath))
        {
            fileData = File.ReadAllBytes(filePath);
            tex = new Texture2D(2, 2);
            tex.LoadImage(fileData); //..this will auto-resize the texture dimensions.
        }
        return tex;
    }

}