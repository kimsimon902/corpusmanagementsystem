//Making table rows clickable


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