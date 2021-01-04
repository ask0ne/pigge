<?php 
session_start();
header("Content-Type: text/html; charset=ISO-8859-1");
?>

<!DOCTYPE html>
<HTML>
<BODY background="que.jpg">
<head><title>Assessment</title></head>

<FONT>
<H1>Questions : </H1>

<form method="post">

<H3>Q.  WHAT FOOLISHNESS WAS THE POOR BIRD THINKING OF?</H3>
<h3>
  <input type="radio" name="Q1" value="a"  required> The monkey should have not left his home.<br>
  <input type="radio" name="Q1" value="b"> Fools never value good advice. It is better not to Advice them.<br>
  <input type="radio" name="Q1" value="c"> The monkey should have prepared for the season like the birds.<br>
</h3>
<H3>Q.  DOES THE ABOVE QUOTE AND MORAL OF THE STORY RELATE WITH EACH OTHER?</H3>
<h3>
  <input type="radio" name="Q2" value="a"  required> Partially yes<br>
  <input type="radio" name="Q2" value="b"> Absolutely , so relatable<br>
  <input type="radio" name="Q2" value="c"> No<br>
</h3>

<H3>Q. WHAT IS SUITABLE MEANING FOR THE WORD ‘VIGOROUS’ IN THE STORY?</H3>

<h3>
  <input type="radio" name="Q3" value="a"  required> Strong<br>
  <input type="radio" name="Q3" value="b"> Physical strength, effort, or energy<br>
  <input type="radio" name="Q3" value="c"> Healthy<br>
</h3>

<H3>Q. WHY COULD THE BIRDS NOT HELP THE MONKEY?	</H3>

<h3>
  <input type="radio" name="Q4" value="a"  required> They wanted to see the monkey struggling in the harsh weather.<br>
  <input type="radio" name="Q4" value="b"> The monkeys didn’t have shelter for themselves.<br>
  <input type="radio" name="Q4" value="c"> Their nests were tiny to help the monkey with shelter.<br>
</h3>

<H3>Q. HOW DID THE MONKEY REACT TO THE BIRD’S ADVICE?</H3>

<h3>
  <input type="radio" name="Q5" value="a"  required> The monkey ran away to avoid irritating advises<br>
  <input type="radio" name="Q5" value="b"> The monkey angrily pounced on the bird’s nest, tore it and threw it on the ground.<br>
  <input type="radio" name="Q5" value="c"> The monkey listened to the bird’s advice and regretted his carelessness.<br>
</h3>

<br><br><br>

<button name="submit" style="margin-left:200px " > <img src="sub.jpg"  > </button>

</form>

<style>
input{
width:15px;
height:15px;
}
</style>


<?php

if(isset($_POST['submit'])){

$points=0;

if($_POST["Q1"]=="b")
$points=$points+1;

if($_POST["Q2"]=="c")
$points=$points+1;

if($_POST["Q3"]=="b")
$points=$points+1;

if($_POST["Q4"]=="c")
$points=$points+1;

if($_POST["Q5"]=="b")
$points=$points+1;


$time_elapsed=$_SESSION["readtime"];
$name=$_SESSION["uname"];
$_SESSION["score"]=$points;

$l = array ($name,$time_elapsed,$points );

$file = fopen("TempData.csv","w");

  fputcsv($file, $l);

fclose($file);

$x='C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python37-32\\python.exe';
$p='C:\\xampp\\htdocs\\final\\pycode.py';
    $cmd="$x $p";
   passthru($cmd);

header('Location:View.php');

}

?>

</BODY>
</FONT>
</HTML>