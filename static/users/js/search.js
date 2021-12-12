function toggleAbstract(pubID){
    var x = document.getElementById("abstract-" + pubID);

    if (x.style.display === "none"){
        x.style.display = "table-row"
    }
    else {
        x.style.display = "none"
    }
}