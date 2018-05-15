var elem=document.getElementById("logoTxt");
var body=document.getElementById("Body");
var wid=body.offsetWidth;
if(wid<=550)elem.innerHTML="VHS";

var searching=false;
var search=document.getElementById("Search");
var searcher=document.getElementById("searcher");
var shadow=document.getElementById("Shad");
search.addEventListener('click',function(){
    if(searching)
    {
        shadow.style.display="none";
        searcher.style.display="none";
        searching=false;
    }
    else
    {
        shadow.style.display="block";
        searcher.style.display="block";
        searching=true;
    }
});

var holder=document.getElementById("mHolder");
var opned=false;
holder.addEventListener('click',function(){
    var els=document.getElementsByClassName("navMen");
    if(opned)
    {
        for(var i=0;i<els.length;i++)
            els[i].style.display="none";
        holder.style.backgroundColor="rgba(240, 203, 142,0)";
        opned=false;
    }
    else
    {
        for(var i=0;i<els.length;i++)
            els[i].style.display="block";
        holder.style.backgroundColor="rgba(240, 203, 142,0.4)";
        opned=true;
    }
});

function swit(e){
        var elem=e.currentTarget;
        if(elem.value)
        {
            elem.style.backgroundColor="rgba(0,0,0,0)";
            elem.style.fontWeight="normal";
            elem.style.color="grey";
            elem.value=0;
        }
        else
        {
            elem.style.backgroundColor="#f0cb8e";
            elem.style.fontWeight="bold";
            elem.style.color="black";
            elem.value=1;
        }
}

function getCurrentPage() {
    var url = window.location.href;
    var host = "http://"+window.location.host+"/";

    return url.substr(host.length);
}

var start=document.getElementById("startSearch");
var date=document.getElementById("Date");
var views=document.getElementById("byViews");
var key=document.getElementById("searchKey");
var pr_page=getCurrentPage();
var map_needed=false;

views.value=0;
date.value=0;
views.addEventListener('click',swit);
date.addEventListener('click',swit);


    start.addEventListener('click',function(){
        var val = key.value;
        var vw=views.value;
        var dt=date.value;
        if (pr_page == "" ) {
            map_needed=$('#show_video_map').prop('checked');
        }

        if(val=="") val=" ";
        $.ajax({
                       url:"/startSearch",
                       type:"GET",
                       dataType:"html",
                       data: {
                            ask:val,
                            view:vw,
                            dat:dt
                       },
                       success:function(response)
                       {
                            var placer="";
                            var plus=false;
                            for(var i=0;i<response.length;i++)
                            {
                                if(response[i]=='<' && response[i+1]=='m' && response[i+2]=='a' && response[i+3]=='i')plus=true;
                                if(plus)placer+=response[i];
                                if(response[i+2]=='/' && response[i+3]=='m' && plus)i=response.length;
                            }
                            placer=placer.substr(17);
                            var mn=document.getElementById("Main");
                            mn.innerHTML=placer;
                       },
                       error:function(){}
        });
        if (pr_page != "") {
            $.getScript("https://api-maps.yandex.ru/2.1/?lang=ru_RU", function () {$.getScript('/static/videos_map.js');});
        }
        else {
            $.getScript('/static/videos_map.js');
        }
        pr_page="";

    });
