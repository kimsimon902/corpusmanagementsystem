//Making table rows clickable
document.addEventListener("DOMContentLoaded", () => {
    const rows = document.querySelectorAll("tr[data-href]");
    
    rows.forEach( row => {
        row.addEventListener("click", () => {
            window.location.href = row.dataset.href;
        });
    });
});

$(document).ready(function(){

    var counter = 2;
		
    $("#addButton").click(function () {
				
	if(counter>10){
            alert("Only 10 textboxes allow");
            return false;
	}   
		
	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("id", 'TextBoxDiv' + counter);
                
	newTextBoxDiv.after().html('<label>Textbox #'+ counter + ' : </label>' +
	      '<input type="text" name="textbox' + counter + 
	      '" id="textbox' + counter + '" value="" >');
            
	newTextBoxDiv.appendTo("#TextBoxesGroup");

				
	counter++;
     });

     $("#removeButton").click(function () {
	if(counter==1){
          alert("No more textbox to remove");
          return false;
       }   
        
	counter--;
			
        $("#TextBoxDiv" + counter).remove();
			
     });
		
     $("#getButtonValue").click(function () {
		
	var msg = '';
	for(i=1; i<counter; i++){
   	  msg += "\n Textbox #" + i + " : " + $('#textbox' + i).val();
	}
    	  alert(msg);
     });
  });


function clickEditOnAnnotation() {
    if(document.getElementById("pubsAnnotationTextArea").hasAttribute('readonly'))
        document.getElementById("pubsAnnotationTextArea").removeAttribute('readonly');
    else
    document.getElementById("pubsAnnotationTextArea").setAttribute('readonly',true);

    var save = document.getElementById("pubsAnnotation_btnSave");
    var cancel = document.getElementById("pubsAnnotation_btnCancel");
    if (save.style.display === "none" && cancel.style.display === "none") {
      save.style.display = "inline";
      cancel.style.display = "inline";
    } else {
      save.style.display = "none";
      cancel.style.display = "none";
    }

    var edit = document.getElementById("pubsAnnotation_btnEdit");
    edit.style.display = "none";
}

function clickCancelAnnotation(){
    var edit = document.getElementById("pubsAnnotation_btnEdit");
    var save = document.getElementById("pubsAnnotation_btnSave");
    var cancel = document.getElementById("pubsAnnotation_btnCancel");
    edit.style.display = "inline";
    save.style.display = "none";
    cancel.style.display = "none";
    document.getElementById("pubsAnnotationTextArea").setAttribute('readonly',true);
}