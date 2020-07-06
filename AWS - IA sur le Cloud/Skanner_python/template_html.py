def html(init):
    if init != "" :
        if init == 1:
            texte = "You should visit a doctor"
        else:
            texte = "Your lesion seems to be fine"
        return """
        <!DOCTYPE html>
<html>
<title>W3.CSS Template</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
<style>
body,h1 {font-family: "Raleway", sans-serif}
body, html {height: 100%}
.bgimg {
  background-image: url('https://drive.google.com/uc?export=view&id=1pbCpaVQAEoSOJm4pTeBV-T7NjszKLkv2');
  min-height: 100%;
  background-position: center;
  background-size: cover;
}
</style>
<body>





<div class="bgimg w3-display-container w3-animate-opacity w3-text-white">
  <div class="w3-display-topleft w3-padding-large w3-xlarge">
  </div>
  <div class="w3-display-middle">
    <h1 class="w3-jumbo w3-animate-top", style="text-align:center">Skanner</h1>
    <hr class="w3-border-grey" style="margin:auto;width:40%">
    <p class="w3-large w3-center">Detect skin lesion</p>
    <br><br>
    <h3>Results : """+texte + """</h3><br>
    <form class="w3-large w3-center" method=post enctype=multipart/form-data> <input class="w3-large w3-center" type=file name=file><input class="w3-large w3-center" type=submit value=Upload></form>

</div>

</body>
</html>
"""

    if init == "":
        return """
    <!DOCTYPE html>
<html>
<title>W3.CSS Template</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
<style>
body,h1 {font-family: "Raleway", sans-serif}
body, html {height: 100%}
.bgimg {
  background-image: url('https://drive.google.com/uc?export=view&id=1pbCpaVQAEoSOJm4pTeBV-T7NjszKLkv2');
  min-height: 100%;
  background-position: center;
  background-size: cover;
}
</style>
<body>





<div class="bgimg w3-display-container w3-animate-opacity w3-text-white">
  <div class="w3-display-topleft w3-padding-large w3-xlarge">
  </div>
  <div class="w3-display-middle">
    <h1 class="w3-jumbo w3-animate-top", style="text-align:center">Skanner</h1>
    <hr class="w3-border-grey" style="margin:auto;width:40%">
    <p class="w3-large w3-center">Detect skin lesion</p>
    <br><br>
    <form class="w3-large w3-center" method=post enctype=multipart/form-data>  <input type=file name=file> 	<input class="w3-large w3-center" type=submit value=Upload></form>

</div>

</body>
</html>

    
    
    
    
    
    """