//Making table rows clickable
document.addEventListener("DOMContentLoaded", () => {
    const rows = document.querySelectorAll("tr[data-href]");
    
    rows.forEach( row => {
        row.addEventListener("click", () => {
            window.location.href = row.dataset.href;
        });
    });
});

function clickEditOnAnnotationClass(id) {
    if(document.getElementById("pubsAnnotationTextArea_"+id).hasAttribute('readonly')){
        document.getElementById("pubsAnnotationTextArea_"+id).removeAttribute('readonly');
        document.getElementById("pubsMarkerSelect_"+id).removeAttribute('disabled');
        document.getElementById("pubsMarkerSelect_"+id).classList.remove('invisible');
        console.log("disable")
    } else{
        document.getElementById("pubsAnnotationTextArea_"+id).setAttribute('readonly',true);
        document.getElementById("pubsMarkerSelect_"+id).setAttribute('disabled', true);
        document.getElementById("pubsMarkerSelect_"+id).classList.add('invisible');
        console.log("true")
    }

    var save = document.getElementById("pubsAnnotation_btnSave_"+id);
    var cancel = document.getElementById("pubsAnnotation_btnCancel_"+id);
    var del = document.getElementById("pubsAnnotation_btnDelete_"+id);
    if (save.style.display === "none" && cancel.style.display === "none") {
      save.style.display = "inline";
      cancel.style.display = "inline";
    } else {
      save.style.display = "none";
      cancel.style.display = "none";
    }

    console.log("clicked");

    var edit = document.getElementById("pubsAnnotation_btnEdit_"+id);
    edit.style.display = "none";
    del.style.display = "none";
}

function clickSaveAnnotationClass(id){
    var edit = document.getElementById("pubsAnnotation_btnEdit_"+id);
    var save = document.getElementById("pubsAnnotation_btnSave_"+id);
    var cancel = document.getElementById("pubsAnnotation_btnCancel_"+id);
    var del = document.getElementById("pubsAnnotation_btnDelete_"+id);
    edit.style.display = "inline";
    del.style.display = "inline";
    save.style.display = "none";
    cancel.style.display = "none";
    document.getElementById("pubsAnnotationTextArea_"+id).setAttribute('readonly',true);
    document.getElementById("pubsMarkerSelect_"+id).classList.remove('invisible');
    document.getElementById("pubsMarkerSelect_"+id).classList.add('invisible');
}

function clickCancelAnnotationClass(id, body, marker){
    var edit = document.getElementById("pubsAnnotation_btnEdit_"+id);
    var save = document.getElementById("pubsAnnotation_btnSave_"+id);
    var cancel = document.getElementById("pubsAnnotation_btnCancel_"+id);
    var del = document.getElementById("pubsAnnotation_btnDelete_"+id);
    edit.style.display = "inline";
    del.style.display = "inline";
    save.style.display = "none";
    cancel.style.display = "none";
    document.getElementById("pubsAnnotationTextArea_"+id).setAttribute('readonly',true);
    document.getElementById("pubsMarkerSelect_"+id).setAttribute('disabled', true);
    document.getElementById("pubsMarkerSelect_"+id).classList.remove('invisible');
    document.getElementById("pubsMarkerSelect_"+id).classList.add('invisible');

    document.getElementById("pubsAnnotationTextArea_"+id).value = body;
    document.getElementById("pubsMarkerSelect_"+id).value = marker;

    console.log("clicked");
}

function checkIfFound(id){
    var found = document.getElementById("exist-modal-"+id);
    var addDiv = document.getElementById("add-modal-"+id);

    if (found == null){
        addDiv.style.display = "inline";
    }
    else {
        addDiv.style.display = "none";
    }
}