' Adapted from:
' http://gallery.technet.microsoft.com/scriptcenter/03f21031-07de-4a26-9a04-4871cd425870
On Error Resume Next
Dim fso
Set fso = WScript.CreateObject("Scripting.Filesystemobject")
Set f = fso.OpenTextFile("C:\windows\temp\bhpoutput.txt", 2)
strComputer = "." 
Set objWMIService = GetObject("winmgmts:" _ 
    & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2") 
 
Set colSettings = objWMIService.ExecQuery _ 
    ("Select * from Win32_OperatingSystem") 
 
For Each objOperatingSystem in colSettings  
    f.WriteLine "OS Name: " & objOperatingSystem.Name & vbCrLf
    f.WriteLine "Version: " & objOperatingSystem.Version & vbCrLf
    f.WriteLine "Service Pack: " & _ 
        objOperatingSystem.ServicePackMajorVersion _ 
            & "." & objOperatingSystem.ServicePackMinorVersion & vbCrLf
    f.WriteLine "OS Manufacturer: " & objOperatingSystem.Manufacturer & vbCrLf
    f.WriteLine "Windows Directory: " & _ 
        objOperatingSystem.WindowsDirectory & vbCrLf
    f.WriteLine "Locale: " & objOperatingSystem.Locale & vbCrLf
    f.WriteLine "Available Physical Memory: " & _ 
        objOperatingSystem.FreePhysicalMemory & vbCrLf
    f.WriteLine "Total Virtual Memory: " & _ 
        objOperatingSystem.TotalVirtualMemorySize & vbCrLf
    f.WriteLine "Available Virtual Memory: " & _ 
        objOperatingSystem.FreeVirtualMemory & vbCrLf
    f.WriteLine "Size stored in paging files: " & _ 
        objOperatingSystem.SizeStoredInPagingFiles & vbCrLf
Next 
 
Set colSettings = objWMIService.ExecQuery _ 
    ("Select * from Win32_ComputerSystem") 
 
For Each objComputer in colSettings  
    f.WriteLine "System Name: " & objComputer.Name & vbCrLf
    f.WriteLine "System Manufacturer: " & objComputer.Manufacturer & vbCrLf
    f.WriteLine "System Model: " & objComputer.Model & vbCrLf
    f.WriteLine "Time Zone: " & objComputer.CurrentTimeZone & vbCrLf
    f.WriteLine "Total Physical Memory: " & _ 
        objComputer.TotalPhysicalMemory & vbCrLf
Next 
 
Set colSettings = objWMIService.ExecQuery _ 
    ("Select * from Win32_Processor") 
 
For Each objProcessor in colSettings  
    f.WriteLine "System Type: " & objProcessor.Architecture & vbCrLf
    f.WriteLine "Processor: " & objProcessor.Description & vbCrLf
Next 
 
Set colSettings = objWMIService.ExecQuery _ 
    ("Select * from Win32_BIOS") 
 
For Each objBIOS in colSettings  
    f.WriteLine "BIOS Version: " & objBIOS.Version & vbCrLf
Next

f.Close
