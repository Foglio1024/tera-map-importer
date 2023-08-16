// Decompiled with JetBrains decompiler
// Type: CLI_Exporter.Program
// Assembly: TeraHelperCLI, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null
// MVID: 21E19CDC-D61D-47DF-886C-4021BF745F9C
// Assembly location: E:\TERA_Export_Tools\tera-map-importer\TeraHelperCLI.exe

using GPK_RePack.IO;
using GPK_RePack.Model;
using GPK_RePack.Model.Interfaces;
using GPK_RePack.Model.Prop;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace CLI_Exporter
{
  internal class Program
  {
    private static void Main(string[] args)
    {
      if (!((IEnumerable<string>) args).Contains<string>("-tsv_export"))
        return;
      Program.ExportTSV(args);
    }

    private static void ExportTSV(string[] args)
    {
      string path1 = args[1];
      string output = args[2];
      GpkPackage gpkPackage = new Reader().ReadGpk(path1);
      output = Path.Combine(output, Path.GetFileNameWithoutExtension(gpkPackage.Path));
      if (!Directory.Exists(output))
        Directory.CreateDirectory(output);
      gpkPackage.ExportList.Values.ToList<GpkExport>().ForEach((Action<GpkExport>) (exp =>
      {
        if (exp.Properties.Count == 0)
          return;
        StringBuilder stringBuilder = new StringBuilder();
        string str1 = "";
        foreach (IProperty property in exp.Properties)
        {
          string name = ((GpkBaseProperty) property).name;
          string type = ((GpkBaseProperty) property).type;
          string str2 = ((GpkBaseProperty) property).size.ToString();
          switch (property)
          {
            case GpkObjectProperty gpkObjectProperty2:
              str1 = gpkObjectProperty2.objectName;
              break;
            case GpkArrayProperty gpkArrayProperty2:
              str1 = gpkArrayProperty2.GetValueHex();
              break;
            case GpkStructProperty gpkStructProperty2:
              str1 = gpkStructProperty2.GetValueHex();
              break;
            case GpkNameProperty gpkNameProperty2:
              str1 = gpkNameProperty2.name;
              break;
            case GpkByteProperty gpkByteProperty2:
              str1 = gpkByteProperty2.size == 8 ? gpkByteProperty2.nameValue : gpkByteProperty2.byteValue.ToString();
              break;
            case GpkFloatProperty gpkFloatProperty2:
              str1 = gpkFloatProperty2.value.ToString();
              break;
            case GpkIntProperty gpkIntProperty2:
              str1 = gpkIntProperty2.value.ToString();
              break;
            case GpkStringProperty gpkStringProperty2:
              str1 = gpkStringProperty2.value.ToString();
              break;
            case GpkBoolProperty gpkBoolProperty2:
              str1 = gpkBoolProperty2.value.ToString();
              break;
          }
          string str3 = name + "\t" + type + "\t" + str2 + "\t" + str1;
          stringBuilder.AppendLine(str3);
        }
        string path2 = Path.Combine(output, exp.UID + ".tsv");
        if (path2 == "")
          return;
        File.WriteAllText(path2, stringBuilder.ToString());
      }));
    }
  }
}
