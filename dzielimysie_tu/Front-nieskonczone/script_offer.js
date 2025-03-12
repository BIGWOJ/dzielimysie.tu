function changeImage() {
    let img = document.getElementById("dogImage");
    
    let newImage = "images/pies_click.jpg"; 

    // Jeśli obecny obraz to domyślny, zmień na nowy, inaczej wróć do starego
    if (img.src.includes("pies.jpg")) {
        img.src = newImage;
    } else {
        img.src = "images/pies.jpg"; 
    }
}
