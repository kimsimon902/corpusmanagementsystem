function toggleAnnotationButton(){
    var card = document.getElementById("annotationCard");
    if (card.style.display === "inline"){
        card.style.display = "none";
        document.getElementById("annotationButton").setAttribute('class','far fa-clipboard');
    } else {
        card.style.display = "inline";
        document.getElementById("annotationButton").setAttribute('class','fas fa-clipboard');
    }
}