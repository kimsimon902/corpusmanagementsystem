function toggleAbstract(pubID){
    var x = document.getElementById("abstract-" + pubID);

    if (x.style.display === "none"){
        x.style.display = "block"
    }
    else {
        x.style.display = "none"
    }
}