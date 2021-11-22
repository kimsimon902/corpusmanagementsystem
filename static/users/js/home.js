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
    if(document.getElementById("pubsAnnotationTextArea_"+id).hasAttribute('readonly'))
        document.getElementById("pubsAnnotationTextArea_"+id).removeAttribute('readonly');
    else
    document.getElementById("pubsAnnotationTextArea_"+id).setAttribute('readonly',true);

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

    var edit = document.getElementById("pubsAnnotation_btnEdit_"+id);
    edit.style.display = "none";
    del.style.display = "none";
}

function clickCancelAnnotationClass(id){
    var edit = document.getElementById("pubsAnnotation_btnEdit_"+id);
    var save = document.getElementById("pubsAnnotation_btnSave_"+id);
    var cancel = document.getElementById("pubsAnnotation_btnCancel_"+id);
    var del = document.getElementById("pubsAnnotation_btnDelete_"+id);
    edit.style.display = "inline";
    del.style.display = "inline";
    save.style.display = "none";
    cancel.style.display = "none";
    document.getElementById("pubsAnnotationTextArea_"+id).setAttribute('readonly',true);
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