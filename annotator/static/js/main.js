var list_of_underlines = []

function getSelectionText(relation) {

    var text = "";
    if (window.getSelection) {
        text = window.getSelection().toString();
    } else if (document.selection && document.selection.type != "Control") {
        text = document.selection.createRange().text;
    }
    /* If nothing is highlighted, do nothing */
    let output_text = ''+document.getSelection().toString()

    if(text=''){return console.log('Nothing was highlighted')}
    

    displayed_paragraph = document.getElementById('text').children[1]
    underlined_paragraph = document.getElementById('text').children[2]
    underlined_paragraph.innerText = displayed_paragraph.innerText

    /* Appending the underline list */
    var start = document.getSelection().getRangeAt(0).startOffset 
    var end = document.getSelection().getRangeAt(0).endOffset 

    /* We need to check here wether it overlaps with parts that have been highlighted before */
    var found_overlap = false

    for (var i = 0; i <list_of_underlines.length ; i++) {
        var s2 = list_of_underlines[i][0]
        var e2 = list_of_underlines[i][1]

        console.log(s2, start, e2)
        console.log(s2, end, e2)
            if((s2<=start && start<=e2)||(s2<=end&&end<=e2)){found_overlap = true
            console.log('So this runs now?')}
        }    
    if(!found_overlap){list_of_underlines.push([start, end, relation])}
    
    /* Adding the spans */

    /* Need to code sorting algorithm by end and take care of overlaps */
    
    function sortFunction(a, b) {
        if (a[1] === b[1]) {
            return 1;
        }
        else {
            return (a[1] < b[1]) ? -1 : 1;
        }
    }
    

    list_of_underlines = list_of_underlines.sort(sortFunction);
    
    
    var end, start

    for (let i = list_of_underlines.length-1; i >=0 ; i--) {

        end = list_of_underlines[i][1]
        start = list_of_underlines[i][0]

        previous_start = start

        var relation = list_of_underlines[i][2]

        var start_paragraph = underlined_paragraph.innerHTML.slice(0, start)
        var highlited_section = underlined_paragraph.innerHTML.slice(start, end)
        var end_paragraph = underlined_paragraph.innerHTML.slice(end, underlined_paragraph.innerHTML.length)

        underlined_paragraph.innerHTML = start_paragraph +'<span class=' + relation+ '>' + highlited_section  +'</span>' + end_paragraph
    }
    


    text = text.replace(',', '').replace(',', '').replace(',', '').replace(',', '').replace(',', '')
    
    return output_text;
}

var tags = document.getElementById('tags').children




for (let i = 0; i < tags.length; i++) {
    tags[i].addEventListener("click", function () {

        /* Workboard State Management*/
        let workboard = document.getElementById("workboard")
        if (workboard.children.length == 3){
            return console.log('triplet is complete')
        }

        innerText = getSelectionText(this.id.split('_tag')[0])
        
        if (innerText == ''){return console.log('no text selected')}

        
        

        
        
        

        
        /* Specifying an entity */
            let new_entity = document.createElement('button')
            new_entity.type = 'button'
            new_entity.id = this.id
            new_entity.className = 'btn btn-primary'
            new_entity.innerText = innerText
            workboard.appendChild(new_entity)
            console.log(workboard.children.length)

            /* Specifying a relationship */
            if (workboard.children.length == 1){
                let new_relation = document.createElement('button')
                new_relation.type = 'button'
                new_relation.className = 'btn btn-primary'
                new_relation.id = 'relation_tag'
                new_relation.innerText = 'Add relation'
                
                
                new_relation.addEventListener("click", function () {
                    input = document.createElement('input')
                    input.type = "text"
                    input.placeholder = 'add relation type'
                    new_relation.innerText = ''
                    new_relation.appendChild(input) 
                    input.select()

                    input.addEventListener("keyup", function(event) {
                        if (event.keyCode === 32) {
                            event.preventDefault()
                        }
                        // Number 13 is the "Enter" key on the keyboard
                        if (event.keyCode === 13) {
                            var text = input.value
                          // Cancel the default action, if needed
                          event.preventDefault();
                          // Trigger the button element with a click
                          new_relation.removeChild(input)
                          new_relation.innerText = text
                        }

                        
                      });

                })
            
                workboard.appendChild(new_relation)

            }
        
    });;
}

/* Adding Triplet to List Logic */
document.getElementById('submit_triplet').addEventListener('click', function(){
    let workboard = document.getElementById("workboard")
    if (workboard.children.length != 3){return console.log('Triplet incomplete')}


    var triplet_element = document.createElement('li')

    var triplet_innerText = '('+ workboard.children[0].id.split('_tag')[0] +'_' + workboard.children[0].innerText  +'_'+ workboard.children[1].innerText  + '_' + workboard.children[2].id.split('_tag')[0]  +'_'+ workboard.children[2].innerText  + ')'

    triplet_element.innerText = triplet_innerText.replace(',', '').replace(',', '').replace(',', '').replace(',', '').replace(',', '')

    document.getElementById('triplet_list').append(triplet_element)
    workboard.innerHTML = ''
})


/* Sending Triplets to Server */
document.getElementById('submit_all_triplets').addEventListener('click', function(){
    triplet_list = document.getElementById('triplet_list').children
    
    triplet_list_formatted = []

    for (let i = 0; i < triplet_list.length; i++) {
        triplet_formatted = []
        for (let j = 0; j < triplet_list[i].innerText.split('_').length; j++) {
            triplet_list_formatted.push(triplet_list[i].innerText.split('_')[j])
        }
    }

    submit_triplets(triplet_list_formatted)

})


function submit_triplets(triplet_list){
    var identifier = document.getElementById('identifier').innerText
    var dataset = document.getElementById('dataset').innerText
    var params = 'triplet_list=' + triplet_list + '&identifier=' + identifier + '&dataset=' + dataset

    console.log(params)
    var xhttp_request = new XMLHttpRequest();
    xhttp_request.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log('success')
            location.reload()
        }
    }
    xhttp_request.open("POST", "/add_triplets", true);
    xhttp_request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp_request.send(params);
}


let delete_button = document.getElementById('delete_button')
delete_button.addEventListener('click', function(){
    submit_triplets('DELETE');
    setTimeout(function(){
        location.reload()
    }, 1000)
})