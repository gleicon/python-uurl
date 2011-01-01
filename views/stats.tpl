<html lang="en"> 
 
<head> 
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> 
    <title>uURL</title> 
    <link rel="stylesheet" href="main.css" type="text/css" media="screen" charset="utf-8"> 
    <script type="text/javascript" src="jquery.min.js"></script>
    <script type="text/javascript" src="jquery.sparkline.min.js"></script>
    <style type="text/css">
        .hourlyUsage { width: 120px; height: 40px; padding-top: 15px; background: transparent ; }
        .hourlyUsage span { display: block; color: #0482AD; font-size: 9px; text-align: left; font-family: Sans-Serif; }
    </style>
    
    <script>
        $(function() {
            var usageData = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

            $.getJSON('/s/{{uurl}}?jsoncallback=?', function(data) {
                var dt = new Date();
                dt.setTime( data.date_creation * 1000 );
                date_creation = dt.toUTCString();
            
                $('#content').prepend('<p>Original URL: <a href="'+data.url+'">'+data.url+'</a></p>'
                + '<p>Shortened URL: <a href="http://7co.cc/{{uurl}}">http://7co.cc/{{uurl}}</a></p>' 
                + '<p>your stats URL (with ! in the end): <a href="http://7co.cc/{{uurl}}">http://7co.cc/{{uurl}}!</a></p>' 
	        + '<p>Clicks since '+date_creation+': '+data.clicks + '</p>'
	        + '<p>Visitors: '+data.visitors+'</p>'
                + '<p>Referers: '+data.referers+'</p>');
                if (data.cph) {
                  for (l in data.cph) {
                    a = l.split(".");
                    usageData[parseInt(a[3])]=data.cph[l];
                  }
                } 

               $('.hourlyUsage').sparkline(usageData, {
                            type: 'bar',
                            barColor: '#4D4D4D',
                            height: 25
                });
                $('<span>clicks per hour</span>').insertAfter($('.hourlyUsage').find("canvas"));

            });
			
       });
    </script>
</head>

<body> 
<div id='topbar'> 
    <h1 style="float: left">Python|Bottle|GEvent|Redis|URL Shortener</h1> 
</div> 
<div id='content'> 
    <span class="hourlyUsage"></span><br>
</div> 
<div id='footer'> 
        (c) gleicon 2010  
</div> 
 
</body> 
</html> 


