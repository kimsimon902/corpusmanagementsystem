function toggleAbstract(pubID){
    var x = document.getElementById("abstract-" + pubID);
    var y = document.getElementById("action-buttons-" + pubID);

    if (x.style.display === "none"){
        x.style.display = "table-row"
        y.style.borderBottomWidth = "0px"
    }
    else {
        x.style.display = "none"
        y.style.borderBottomWidth = "1px"
    }
}