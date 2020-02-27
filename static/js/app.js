var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
// editor.session.setMode("ace/mode/javascript");

// output functions are configurable.  This one just appends some text
// to a pre element.
function outf(text) { 
    var mypre = document.getElementById("output"); 
    mypre.innerHTML = mypre.innerHTML + text; 
} 
function builtinRead(x) {
    if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
            throw "File not found: '" + x + "'";
    return Sk.builtinFiles["files"][x];
}

// Here's everything you need to run a python program in skulpt
// grab the code from your textarea
// get a reference to your pre element for output
// configure the output function
// call Sk.importMainWithBody()

function print_demo() {
   var editor = ace.edit("editor");
   editor.setValue("print Hallo welkom bij Hedy");

}

function ask_demo() {
   var editor = ace.edit("editor");
   editor.setValue("ask Wat is je lievelingskleur");

}

function runit() {

   // var prog = document.getElementById("editor").value;

   var editor = ace.edit("editor");
   var prog = editor.getValue();

   console.log('Origineel programma:\n', prog);

   var url = "/parse/?code=" + encodeURIComponent(prog);
   var xhr = new XMLHttpRequest();
   xhr.open('GET', url, true);
   xhr.send();

   function processRequest(e) {
      if (xhr.readyState == 4 && xhr.status == 200) {
         var response = JSON.parse(xhr.responseText);
         var code = response["Code"];
         console.log('Veraald programma:\n', code);
         var mypre = document.getElementById("output");
         mypre.innerHTML = '';
         Sk.pre = "output";
         Sk.configure({ output: outf, read: builtinRead });
         var myPromise = Sk.misceval.asyncToPromise(function () {
            return Sk.importMainWithBody("<stdin>", false, code, true);
         });
         myPromise.then(function (mod) {
            console.log('success');
         },
            function (err) {
               console.log(err.toString());
            });
      }
   }

   xhr.onreadystatechange = processRequest;


} 
