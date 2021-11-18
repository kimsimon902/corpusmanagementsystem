//Making table rows clickable
document.addEventListener("DOMContentLoaded", () => {
    const rows = document.querySelectorAll("tr[data-href]");
    
    rows.forEach( row => {
        row.addEventListener("click", () => {
            window.location.href = row.dataset.href;
        });
    });
});


function clickEditOnAnnotation() {
    if(document.getElementById("pubsAnnotationTextArea").hasAttribute('readonly'))
        document.getElementById("pubsAnnotationTextArea").removeAttribute('readonly');
    else
    document.getElementById("pubsAnnotationTextArea").setAttribute('readonly',true);

    var save = document.getElementById("pubsAnnotation_btnSave");
    var cancel = document.getElementById("pubsAnnotation_btnCancel");
    var del = document.getElementById("pubsAnnotation_btnDelete");
    if (save.style.display === "none" && cancel.style.display === "none") {
      save.style.display = "inline";
      cancel.style.display = "inline";
    } else {
      save.style.display = "none";
      cancel.style.display = "none";
    }

    var edit = document.getElementById("pubsAnnotation_btnEdit");
    edit.style.display = "none";
    del.style.display = "none";
}

function clickCancelAnnotation(){
    var edit = document.getElementById("pubsAnnotation_btnEdit");
    var save = document.getElementById("pubsAnnotation_btnSave");
    var cancel = document.getElementById("pubsAnnotation_btnCancel");
    var del = document.getElementById("pubsAnnotation_btnDelete");
    edit.style.display = "inline";
    del.style.display = "inline";
    save.style.display = "none";
    cancel.style.display = "none";
    document.getElementById("pubsAnnotationTextArea").setAttribute('readonly',true);
}

function clickEditOnAnnotationClass() {
    var save = document.getElementsByClassName("btnSave");
    var cancel = document.getElementsByClassName("btnCancel");
    var del = document.getElementsByClassName("btnDelete");
    if (save.style.display === "none" && cancel.style.display === "none") {
      save.style.display = "inline";
      cancel.style.display = "inline";
    } else {
      save.style.display = "none";
      cancel.style.display = "none";
    }

    var edit = document.getElementsByClassName("btn btn-link btnEdit");
    edit.style.display = "none";
    del.style.display = "none";
}

function clickCancelAnnotationClass(){
    var edit = document.getElementsByClassName("btn btn-link btnEdit");
    var save = document.getElementsByClassName("btn btn-link btnSave");
    var cancel = document.getElementsByClassName("btn btn-link btnCancel");
    var del = document.getElementsByClassName("btn btn-link btnDelete");
    edit.style.display = "inline";
    del.style.display = "inline";
    save.style.display = "none";
    cancel.style.display = "none";
}