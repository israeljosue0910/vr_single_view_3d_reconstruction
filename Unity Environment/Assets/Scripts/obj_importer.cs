using UnityEngine;
using System.Collections;
using System.IO;

//https://web.archive.org/web/20210727020542/http://wiki.unity3d.com/index.php?title=ObjImporter
//https://stackoverflow.com/questions/31586186/loading-a-obj-into-unity-at-runtime
public class obj_importer : MonoBehaviour
{
    public string name = "";

    // Use this for initialization
    void Start()
    {
        Mesh holderMesh = new Mesh();
        ObjImporter newMesh = new ObjImporter();
        holderMesh = newMesh.ImportFile("C:/Users/REO_Razr_Blade/PycharmProjects/2DtoVR/appwin/popup_results/" + name + "/" + name + ".obj");

        MeshRenderer renderer = gameObject.AddComponent<MeshRenderer>();
        MeshFilter filter = gameObject.AddComponent<MeshFilter>();
        filter.mesh = holderMesh;

        string filepath = "C:/Users/REO_Razr_Blade/PycharmProjects/2DtoVR/appwin/popup_results/" + name + "/" + name + ".v.png";
        Texture2D texture = LoadImage(filepath);
        gameObject.GetComponent<Renderer>().material.mainTexture = texture;

        //var mc = gameObject.AddComponent<MeshCollider>();

        //mc.convex = true;
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