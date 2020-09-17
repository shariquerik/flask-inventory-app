$(document).ready(function(){

    $('#gridButton').click(function(){
        $("#listButton").removeClass("active");
        $("#gridButton").addClass("active");
        $("#parentGrid").addClass("flex");

        $('.productsGrid').removeClass('hidden');
        $('.productsList').addClass('hidden');

        $('.locationsGrid').removeClass('hidden');
        $('.locationsList').addClass('hidden');
    })

    $('#listButton').click(function(){ 
        $("#listButton").addClass("active");
        $("#gridButton").removeClass("active");
        $("#parentGrid").removeClass("flex");
    
        $('.productsGrid').addClass('hidden');
        $('.productsList').removeClass('hidden');

        $('.locationsGrid').addClass('hidden');
        $('.locationsList').removeClass('hidden');
    })

    $('#product, #location, #qty').click(function(){
        sortedTable($(this).attr('data-id'));
    })

});
let direction = false;

function sortedTable(col) {
    let table = document.getElementById('dashboardTable');
    let rows = table.rows;
    let a = '';
    let b = '';
    let z = true;
    let stop = true;
    loop();
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