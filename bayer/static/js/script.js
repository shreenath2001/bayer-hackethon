// getting all required elements

const searchWrapperProduct = document.querySelector(".search-input1");
const inputBoxProduct = searchWrapperProduct.querySelector("input");
const suggBoxProduct = searchWrapperProduct.querySelector(".autocom-box");

const searchWrapperCrop = document.querySelector(".search-input2");
const inputBoxCrop = searchWrapperCrop.querySelector("input");
const suggBoxCrop = searchWrapperCrop.querySelector(".autocom-box");

const searchWrapperPest = document.querySelector(".search-input3");
const inputBoxPest = searchWrapperPest.querySelector("input");
const suggBoxPest = searchWrapperPest.querySelector(".autocom-box");

// if user press any key and release

inputBoxProduct.onkeyup = (e)=>{
    let userData = e.target.value; //user enetered data
    let emptyArray = [];
    if(userData){
        emptyArray = product_suggestions.filter((data)=>{
            //filtering array value and user characters to lowercase and return only those words which are start with user enetered chars
            return data.toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        });
        emptyArray = emptyArray.map((data)=>{
            // passing return data inside li tag
            return data = `<li>${data}</li>`;
        });
        searchWrapperProduct.classList.add("active"); //show autocomplete box
        showSuggestionsProduct(emptyArray);
        let allList = suggBoxProduct.querySelectorAll("li");
        for (let i = 0; i < allList.length; i++) {
            //adding onclick attribute in all li tag
            allList[i].setAttribute("onclick", "selectProduct(this)");
        }
    }else{
        searchWrapperProduct.classList.remove("active"); //hide autocomplete box
    }
}

function selectProduct(element){
    let selectData = element.textContent;
    inputBoxProduct.value = selectData;
    searchWrapperProduct.classList.remove("active");
}
function showSuggestionsProduct(list){
    let listData;
    if(!list.length){
        userValue = "No Result Found...";
        listData = `<li>${''}</li>`;
    }else{
      listData = list.join('');
    }
    suggBoxProduct.innerHTML = listData;
}

inputBoxCrop.onkeyup = (e)=>{
    let userData = e.target.value; //user enetered data
    let emptyArray = [];
    if(userData){
        emptyArray = crop_suggestions.filter((data)=>{
            //filtering array value and user characters to lowercase and return only those words which are start with user enetered chars
            return data.toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        });
        emptyArray = emptyArray.map((data)=>{
            // passing return data inside li tag
            return data = `<li>${data}</li>`;
        });
        searchWrapperCrop.classList.add("active"); //show autocomplete box
        showSuggestionsCrop(emptyArray);
        let allList = suggBoxCrop.querySelectorAll("li");
        for (let i = 0; i < allList.length; i++) {
            //adding onclick attribute in all li tag
            allList[i].setAttribute("onclick", "selectCrop(this)");
        }
    }else{
        searchWrapperCrop.classList.remove("active"); //hide autocomplete box
    }
}

function selectCrop(element){
    let selectData = element.textContent;
    inputBoxCrop.value = selectData;
    searchWrapperCrop.classList.remove("active");
}
function showSuggestionsCrop(list){
    let listData;
    if(!list.length){
        userValue = "No Result Found...";
        listData = `<li>${''}</li>`;
    }else{
      listData = list.join('');
    }
    suggBoxCrop.innerHTML = listData;
}

inputBoxPest.onkeyup = (e)=>{
    let userData = e.target.value; //user enetered data
    let emptyArray = [];
    if(userData){
        emptyArray = pest_suggestions.filter((data)=>{
            //filtering array value and user characters to lowercase and return only those words which are start with user enetered chars
            return data.toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        });
        emptyArray = emptyArray.map((data)=>{
            // passing return data inside li tag
            return data = `<li>${data}</li>`;
        });
        searchWrapperPest.classList.add("active"); //show autocomplete box
        showSuggestionsPest(emptyArray);
        let allList = suggBoxPest.querySelectorAll("li");
        for (let i = 0; i < allList.length; i++) {
            //adding onclick attribute in all li tag
            allList[i].setAttribute("onclick", "selectPest(this)");
        }
    }else{
        searchWrapperPest.classList.remove("active"); //hide autocomplete box
    }
}

function selectPest(element){
    let selectData = element.textContent;
    inputBoxPest.value = selectData;
    searchWrapperPest.classList.remove("active");
}
function showSuggestionsPest(list){
    let listData;
    if(!list.length){
        userValue = "No Result Found...";
        listData = `<li>${''}</li>`;
    }else{
      listData = list.join('');
    }
    suggBoxPest.innerHTML = listData;
}

var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active1");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}