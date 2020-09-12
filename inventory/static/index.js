let direction = false;

let gridButton = document.getElementById('grid');
let listButton = document.getElementById('list');
let productsGrid = document.getElementsByClassName('productsGrid');
let productsList = document.getElementsByClassName('productsList');
let locationsGrid = document.getElementsByClassName('locationsGrid');
let locationsList = document.getElementsByClassName('locationsList');

function changeToGrid(){
    listButton.classList.remove("active");
    gridButton.classList.add("active");
    for(i=0; i<productsGrid.length; i++){
        productsGrid[i].classList.remove("hidden");
        productsList[i].classList.add("hidden");
    }
    for(i=0; i<locationsGrid.length; i++){
        locationsGrid[i].classList.remove("hidden");
        locationsList[i].classList.add("hidden");
    }
}
function changeToList(){
    gridButton.classList.remove("active");
    listButton.classList.add("active");
    for(i=0; i<productsGrid.length; i++){
        productsGrid[i].classList.add("hidden");
        productsList[i].classList.remove("hidden");
    }
    for(i=0; i<locationsGrid.length; i++){
        locationsGrid[i].classList.add("hidden");
        locationsList[i].classList.remove("hidden");
    }
}

function sortedTable(col) {
    let table = document.getElementById('dashboardTable');
    let rows = table.rows;
    let a = '';
    let b = '';
    let z = true;
    loop(col);
    function loop(){
        for(i=1; i<rows.length - 1; i++){
            a = rows[i].childNodes[col].innerText;
            b = rows[i+1].childNodes[col].innerText;
            if(col == 5){ 
                var m = a.match(/(\d+)/); 
                var n = b.match(/(\d+)/); 
                a = parseInt(m[0],10);
                b = parseInt(n[0],10);
            }

            if(direction){ z = a < b }
            else{ z = a > b }

            if(z){
                rows[i].parentNode.insertBefore(rows[i+1], rows[i]);
                stop = false;
                break;
            }            
        }
        if(!stop){ 
            stop = true;
            loop();
        }
    }
    direction = !direction;
}