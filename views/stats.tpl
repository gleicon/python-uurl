<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{{base_url}}</title>
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le HTML5 shim, for IE6-8 support of HTML elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <!-- Le styles -->
    <link href="/static/bootstrap.min.css" rel="stylesheet">
    <style type="text/css">
      body {
        padding-top: 60px;
      }
    </style>

    <!-- Le fav and touch icons -->
    <link rel="shortcut icon" href="images/favicon.ico">
    <link rel="apple-touch-icon" href="images/apple-touch-icon.png">
    <link rel="apple-touch-icon" sizes="72x72" href="images/apple-touch-icon-72x72.png">
    <link rel="apple-touch-icon" sizes="114x114" href="images/apple-touch-icon-114x114.png">
    <script type="text/javascript" src="/static/jquery.min.js"></script>
    <script type="text/javascript" src="/static/jquery.sparkline.min.js"></script>
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
                + '<p>Shortened URL: <a href="{{base_url}}{{uurl}}">{{base_url}}{{uurl}}</a></p>' 
                + '<p>Stats URL (with ! in the end): <a href="{{base_url}}{{uurl}}!">{{base_url}}{{uurl}}!</a></p>' 
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

    <div class="topbar">
      <div class="fill">
        <div class="container">
          <a class="brand" href="#">chu.pe</a>
        </div>
      </div>
    </div>

    <div class="container">

      <!-- Example row of columns -->
      <div class="row">
        <div class="span5">
          <h2>URL Shortening</h2><br>
          <img src="/static/itsnothing.jpg"><br><br>
          <p>URL Shortening with the most charming domain name around.</p>
        </div>
        <div class="span11">
          <br><br><br>
	 <div id="content">
    		<span class="hourlyUsage"></span><br>
	</div>
	</div>
      </div>
      <footer>
        <p>&copy; 7co.cc 2011</p>
      </footer>

    </div> <!-- /container -->

  </body>
</html>
