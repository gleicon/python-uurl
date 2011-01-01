!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"> 
<html lang="en"> 
 
<head> 
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> 
        <title>uURL</title> 
    <link rel="stylesheet" href="main.css" type="text/css" media="screen" charset="utf-8"> 
        
</head>

<body> 
<div id='topbar'> 
    <h1 style="float: left">Python|Bottle|GEvent|Redis|URL Shortener</h1> 
</div> 
 
<div id='content'> 
 
    <p>URL: <a href={{base_url}}{{uurl}}>{{base_url}}{{uurl}}</a></p>
    <p>STATS: <a href={{base_url}}{{uurl}}!>{{base_url}}{{uurl}}! (with exclamation sign)</a></p><br>

</div> 
<div id='footer'> 
        (c) gleicon 2010  
</div> 
 
</body> 
</html> 


